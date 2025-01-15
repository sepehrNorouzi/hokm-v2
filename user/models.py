import random

from django.conf import settings
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import QuerySet
from django.db.transaction import atomic
from django.template.loader import render_to_string
from django.utils import translation, timezone
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from common.models import BaseModel
from exceptions.user import ReVerifyException
from user.choices import Gender
from user.managers import UserManager, NormalPlayerManager, GuestPlayerManager
from utils.cryptography import encrypt_string, decrypt_string
from utils.random_functions import generate_random_string


class User(AbstractUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True, blank=True, verbose_name=_("Email"))
    device_id = models.CharField(max_length=255, unique=True, null=True, blank=True, verbose_name=_("Device ID"))
    is_staff = models.BooleanField(default=False, verbose_name=_("Staff status"))
    first_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("First name"))
    last_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Last name"))

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.email or self.device_id or ""

    def get_full_name(self):
        return f"{self.first_name or ""} {self.last_name or ""}"

    @property
    def player(self):
        if self.email:
            return NormalPlayer.objects.get(pk=self.pk)
        return GuestPlayer.objects.get(pk=self.pk)


class Player(User):
    profile_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Profile name"))
    gender = models.IntegerField(verbose_name=_('Gender'), default=Gender.UNKNOWN, choices=Gender.choices)
    birth_date = models.DateField(verbose_name=_('Birth date'), null=True, blank=True)
    is_blocked = models.BooleanField(verbose_name=_('Is blocked'), default=False)
    score = models.PositiveIntegerField(verbose_name=_("Score"), default=0)
    xp = models.PositiveIntegerField(verbose_name=_("Xp"), default=0, editable=False)
    cup = models.PositiveIntegerField(verbose_name=_("Cup"), default=0)

    class Meta:
        abstract = True

    def change_profile_name(self, new_profile_name: str):
        raise NotImplemented

    def get_token(self):
        if self.is_authenticated:
            refresh = RefreshToken.for_user(self)
            access_token = AccessToken.for_user(self)
            token = {
                'access': str(access_token),
                'refresh': str(refresh),
            }
            return token
        else:
            return {}

    @staticmethod
    def refresh_token(refresh):
        refresh = RefreshToken(token=refresh)
        user = Player.objects.filter(id=refresh.access_token.payload['id']).first()
        return user.get_token(refresh)

    @classmethod
    def attempt_login(cls, **kwargs):
        raise NotImplementedError


class GuestPlayer(Player):
    recovery_string = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Recovery string"))

    objects = GuestPlayerManager()

    class Meta:
        verbose_name = _("Guest player")
        verbose_name_plural = _("Guest players")

    def change_profile_name(self, new_profile_name: str):
        raise ValidationError("Guest player can't change profile name")

    def __str__(self):
        return self.device_id or ""

    def _check_recovery_string(self, recovery_string):
        return recovery_string == self.recovery_string

    @classmethod
    def create(cls, device_id: str, password, **extra_fields):
        player = GuestPlayer.objects.create_user(device_id=device_id, password=password, **extra_fields)
        return player

    @classmethod
    def attempt_login(cls, device_id: str, password: str):
        user: QuerySet = cls.objects.filter(device_id=device_id)
        if not user.exists():
            return None, None, 'Invalid credentials.'
        user: GuestPlayer = user.first()

        is_correct = user.check_password(raw_password=password)

        if not is_correct:
            return None, None, 'Invalid credentials.'

        return user, user.get_token(), None

    @classmethod
    def attempt_recovery(cls, device_id, recovery_string: str, new_password: str):
        user: QuerySet = cls.objects.filter(device_id=device_id)
        if not user.exists():
            return None, None, 'Invalid credentials.'
        user: GuestPlayer = user.first()

        is_correct = user._check_recovery_string(recovery_string=recovery_string)

        if not is_correct:
            return None, None, 'Invalid credentials.'
        user.set_password(new_password)
        user.save()
        return user, user.get_token(), None

    def save(self, *args, **kwargs):
        if not self.pk:
            self.profile_name = f'guest-{generate_random_string(length=10)}'
        super(GuestPlayer, self).save(*args, **kwargs)

    @atomic()
    def convert_to_normal_player(self, email: str, password: str, profile_name: str = None):
        user = self.user_ptr
        device_id = self.device_id
        normal_player = NormalPlayer(
            user_ptr=user,
            profile_name=profile_name or self.profile_name,
            gender=self.gender,
            birth_date=self.birth_date,
            is_blocked=self.is_blocked,
            score=self.score,
            xp=self.xp,
            cup=self.cup,
            email=email,
            is_verified=False,
            username=email,
            device_id=None
        )

        self.delete(keep_parents=True)
        normal_player.set_password(password)
        normal_player.save()
        normal_player.send_email_verification()
        DeviceIdBlackList.objects.create(device_id=device_id)
        return normal_player


class NormalPlayer(Player):
    is_verified = models.BooleanField(default=False, verbose_name=_("Is verified"))

    objects = NormalPlayerManager()

    class Meta:
        verbose_name = _("Normal player")
        verbose_name_plural = _("Normal players")

    def change_profile_name(self, new_profile_name: str):
        self.profile_name = new_profile_name
        self.save()

    def __str__(self):
        return self.email or ""

    def _construct_otp(self):
        otp_expt = settings.CACHE_EXPT['otp']
        otp = ''.join([str(random.randint(0, 9)) for __ in range(6)])
        cache.set(f"{self.id}_EMAIL_VERIFY_OTP", otp, otp_expt)
        return otp

    def _get_otp(self):
        return cache.get(f"{self.id}_EMAIL_VERIFY_OTP")

    def send_email_verification(self):
        if self.is_verified:
            raise ReVerifyException(message=_("Player is already verified."), )

        otp = self._construct_otp()

        subject = _(f"{settings.PROJECT_NAME} email verification.")

        html_message = render_to_string('email_verification.html', {
            'user': self,
            'otp': otp,
            'project_name': settings.PROJECT_NAME,
            'LANGUAGE_CODE': translation.get_language()
        })

        plain_message = strip_tags(html_message)

        self.email_user(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            html_message=html_message,
        )

    def resend_email_verification(self) -> bool:
        last_otp = self._get_otp
        if last_otp:
            return False
        self.send_email_verification()
        return True

    def _forget_password_attempt(self) -> tuple:
        previous_password_forget = cache.get(f"{self.id}_FORGET_PASSWORD_TOKEN")
        if previous_password_forget:
            return False, ''
        otp_expt = settings.CACHE_EXPT['otp']
        forget_password_token = f'{self.email}{timezone.now().timestamp()}'
        forget_password_token_encrypt = encrypt_string(forget_password_token)
        cache.set(f"{self.id}_FORGET_PASSWORD_TOKEN", forget_password_token, otp_expt)
        return True, forget_password_token_encrypt

    def forget_password(self, deep_link: str = ''):
        success, token = self._forget_password_attempt()
        if not success:
            return False
        reset_link = deep_link.format(token=token)
        html_message = render_to_string('password_reset.html', {
            'user': self,
            'reset_link': reset_link,
            'project_name': settings.PROJECT_NAME,
            'LANGUAGE_CODE': translation.get_language(),
        })

        plain_message = strip_tags(html_message)

        self.email_user(
            subject=_("Password Reset Request"),
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            html_message=html_message,
        )
        return True

    @classmethod
    def reset_password(cls, email: str, token: str, new_password: str) -> bool:
        player: QuerySet = cls.objects.filter(email=email)
        if not player.exists():
            raise cls.DoesNotExist
        player: NormalPlayer = player.first()
        forget_password_token = cache.get(f"{player.id}_FORGET_PASSWORD_TOKEN")
        token_decrypt = decrypt_string(token)
        if token_decrypt == forget_password_token:
            player.set_password(new_password)
            player.save()
            return True
        cache.delete(f"{player.id}_FORGET_PASSWORD_TOKEN")
        return False

    def verify_email(self, otp: str) -> bool:
        if self.is_verified:
            return True
        cached_otp = cache.get(f"{self.id}_EMAIL_VERIFY_OTP")
        if cached_otp:
            cache.delete(f"{self.id}_EMAIL_VERIFY_OTP")
            if cached_otp == otp:
                self.is_verified = True
                self.save()
                return True

        return False

    @classmethod
    def create(cls, email: str, password: str, **extra_fields):
        player = cls.objects.create_user(email=email, password=password, **extra_fields)
        return player

    @classmethod
    def attempt_login(cls, email: str, password: str):
        user: QuerySet = cls.objects.filter(email=email)
        if not user.exists():
            return None, None, 'Invalid credentials.'

        user: NormalPlayer = user.first()

        if not user.is_verified:
            return None, None, 'User is not verified.'

        is_correct = user.check_password(raw_password=password)

        if not is_correct:
            return None, None, 'Invalid credentials.'

        return user, user.get_token(), None

    @classmethod
    def attempt_password_recovery(cls, email: str, deep_link: str):
        player: QuerySet = cls.objects.filter(email=email)
        if not player.exists():
            raise cls.DoesNotExist
        player: NormalPlayer = player.first()
        return player.forget_password(deep_link=deep_link)


class DeviceIdBlackList(BaseModel):
    device_id = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = _("Device Id Black list")
        verbose_name_plural = _("Device Id Black list")


class SupporterPlayerInfo(BaseModel):
    player = models.ForeignKey(to='user.User', verbose_name=_("Player"), on_delete=models.CASCADE,
                               related_name='supports')
    visible = models.BooleanField(default=False, verbose_name=_("Is visible"))
    used = models.BooleanField(default=False, verbose_name=_("Is used"))
    reason = models.CharField(max_length=10, verbose_name=_("Reason"), )

    approved = models.BooleanField(default=False, verbose_name=_("Approved"))
    approval_date = models.DateTimeField(verbose_name=_("Approval date"), null=True, blank=True)

    # Body
    message = models.CharField(max_length=100, verbose_name=_("Message"), null=True, blank=True)
    instagram_link = models.CharField(max_length=255, verbose_name=_("Instagram"), null=True, blank=True)
    telegram_link = models.CharField(max_length=255, verbose_name=_("Telegram"), null=True, blank=True)
    rubika_link = models.CharField(max_length=255, verbose_name=_("Rubika"), null=True, blank=True)

    class Meta:
        verbose_name = _("Player Support info")
        verbose_name_plural = _("Player Support info")
        ordering = ('-created_time',)

    def approve(self):
        self.approved = True
        self.approval_date = timezone.now()
        self.save()

    def disapprove(self):
        self.approved = False
        self.approval_date = None
        self.save()

    def use(self, data: dict):
        if self.used:
            return
        self.used = True
        self.visible = data.get("visible", False)
        self.message = data.get('message')
        self.instagram_link = data.get('instagram_link')
        self.telegram_link = data.get('telegram_link')
        self.rubika_link = data.get('rubika_link')
        self.save()

    def __str__(self):
        return f'{self.player} - {self.id}'


class VipPlayer(BaseModel):
    player = models.ForeignKey(to='user.User', verbose_name=_("Player"), on_delete=models.CASCADE, related_name='vip')
    expiration_date = models.DateTimeField(verbose_name=_("Expiration date"), )

    def __str__(self):
        return f'{self.player.username} VIP info.'

    class Meta:
        verbose_name = _("VIP player")
        verbose_name_plural = _("VIP players")

    def is_expired(self):
        return self.expiration_date > timezone.now()
