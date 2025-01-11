import pickle

from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class Configuration(models.Model):
    is_active = models.BooleanField(default=True, verbose_name=_("Is active"))
    app_name = models.CharField(verbose_name=_("App Name"), max_length=255)
    game_package_name = models.CharField(verbose_name=_("Game Package Name"), max_length=255)
    app_version = models.CharField(verbose_name=_("App Version"), max_length=100, default='1.0.0')
    app_version_bundle = models.PositiveIntegerField(verbose_name=_("app version bundle"), default=1)
    last_bundle_version = models.PositiveIntegerField(verbose_name=_("Last bundle version"), default=1)
    minimum_supported_bundle_version = models.PositiveIntegerField(verbose_name=_("minimum supported bundle version"),
                                                                   default=1)
    maintenance_mode = models.BooleanField(verbose_name=_('Maintenance mode'), default=False)

    @classmethod
    def get_cache_key(cls):
        return f'{cls.__name__.upper()}_CACHE_KEY'

    def save(self, *args, **kwargs):
        if Configuration.objects.filter(is_active=True).exists():
            raise ValidationError(_("There can only be one active configuration."))
        super(Configuration, self).save(*args, **kwargs)
        if self.is_active:
            cache.set(self.get_cache_key(), pickle.dumps(self))

    @classmethod
    def load(cls):
        return pickle.load(cache.get(cls.get_cache_key()))

    class Meta:
        verbose_name = _("Configuration")
        verbose_name_plural = _("Configurations")

    def __str__(self):
        return f'{self.app_key}_{self.version}'
