from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


from user.choices import Gender
from user.managers import UserManager


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

    class Meta:
        verbose_name = _("Guest player")
        verbose_name_plural = _("Guest players")

    def change_profile_name(self, new_profile_name: str):
        raise ValidationError("Guest player can't change profile name")

    def __str__(self):
        return self.device_id or ""


class NormalPlayer(Player):

    class Meta:
        verbose_name = _("Normal player")
        verbose_name_plural = _("Normal players")

    def change_profile_name(self, new_profile_name: str):
        self.profile_name = new_profile_name

    def __str__(self):
        return self.email or ""
