import random

from django.conf import settings
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import QuerySet
from django.template.loader import render_to_string
from django.utils import translation
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from user.choices import Gender
from user.exceptions import ReVerifyException
from user.managers import UserManager, NormalPlayerManager, GuestPlayerManager


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

    @classmethod
    def create(cls, device_id: str, password, **extra_fields):
        player = GuestPlayer.objects.create_user(device_id=device_id, password=password, **extra_fields)
        return player


class NormalPlayer(Player):
    is_verified = models.BooleanField(default=False, verbose_name=_("Is verified"))

    objects = NormalPlayerManager()

    class Meta:
        verbose_name = _("Normal player")
        verbose_name_plural = _("Normal players")

    def change_profile_name(self, new_profile_name: str):
        self.profile_name = new_profile_name

    def __str__(self):
        return self.email or ""

    def send_email_verification(self):
        if self.is_verified:
            raise ReVerifyException(message=_("Player is already verified."), )

        otp = ''.join([str(random.randint(0, 9)) for __ in range(6)])

        # Save the OTP to the user model (assuming you have a field for OTP)
        cache.set(f"{self.id}_EMAIL_VERIFY_OTP", otp, )

        subject = _(f"{settings.PROJECT_NAME} email verification.")

        # Create the HTML message
        html_message = render_to_string('email_verification.html', {
            'user': self,
            'otp': otp,
            'project_name': settings.PROJECT_NAME,
            'LANGUAGE_CODE': translation.get_language()
        })

        # Create a plain text version of the message
        plain_message = strip_tags(html_message)

        # Send the email
        self.email_user(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            html_message=html_message,
        )

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

        is_correct = user.check_password(raw_password=password)

        if not is_correct:
            return None, None, 'Invalid credentials.'

        return user, user.get_token(), None
