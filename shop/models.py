from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Currency(models.Model):
    class CurrencyType(models.TextChoices):
        IN_APP = 'in_app', 'In App'
        REAL = 'real', 'Real'

    name = models.CharField(verbose_name=_("Currency Name"), max_length=100, unique=True)
    icon = models.ImageField(upload_to='currencies', null=True, blank=True, verbose_name=_("Currency Icon"))
    config = models.JSONField(null=True, blank=True, verbose_name=_("Currency Config"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Currency")
        verbose_name_plural = _("Currencies")

    def save(self, *args, **kwargs):
        if not self.pk and self.icon:
            self.icon.name = f'{self.name}.{self.icon.name.split('.')[-1]}'
        super(Currency, self).save(*args, **kwargs)


class Asset(models.Model):
    class AssetType(models.TextChoices):
        AVATAR = 'avatar', _('Avatar')
        STICKER = 'sticker', _('Sticker')

    name = models.CharField(verbose_name=_("Asset Name"), max_length=100, unique=True)
    config = models.JSONField(null=True, blank=True, verbose_name=_("Asset Config"))
    type = models.CharField(verbose_name=_("Asset Type"), max_length=100, choices=AssetType.choices,
                            default=AssetType.AVATAR)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Asset")
        verbose_name_plural = _("Assets")


class Cost(models.Model):
    currency = models.ForeignKey(to=Currency, verbose_name=_("Currency"), on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(verbose_name=_("Amount"), default=0)

    def __str__(self):
        return f'{self.amount} X {self.currency}'

    class Meta:
        verbose_name = _("Cost")
        verbose_name_plural = _("Costs")
        unique_together = (("currency", "amount"),)


class CurrencyPackageItem(models.Model):
    currency = models.ForeignKey(to=Currency, verbose_name=_("Currency"), on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(verbose_name=_("Amount"), default=0)
    config = models.JSONField(null=True, blank=True, verbose_name=_("Config"))

    def __str__(self):
        return f'{self.amount} X {self.currency}'

    class Meta:
        verbose_name = _("Currency Package Item")
        verbose_name_plural = _("Currency Package Items")


class Package(models.Model):
    start_time = models.DateTimeField(verbose_name=_("Start Time"), null=True, blank=True, )
    name = models.CharField(verbose_name=_("Name"), unique=True, max_length=255)
    priority = models.PositiveIntegerField(verbose_name=_("Priority"), help_text=_("1 is More important"))
    expiration_date = models.DateTimeField(verbose_name=_("Expired time"), null=True, blank=True, )
    image = models.ImageField(upload_to='package', null=True, blank=True, verbose_name=_("Image"))

    def _has_started(self):
        return self.start_time and self.start_time > timezone.now()

    def _has_expired(self):
        return not self.expiration_date or self.expiration_date > timezone.now()

    def is_pacakge_available(self):
        return self._has_started() and not self._has_expired()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Package")
        verbose_name_plural = _("Packages")
        abstract = True


class ShopPackage(Package):
    price_currency = models.ForeignKey(to=Currency, verbose_name=_("Price"), on_delete=models.CASCADE)
    price_amount = models.PositiveIntegerField(verbose_name=_("Price Amount"), default=0)
    discount = models.FloatField(verbose_name=_("Discount"), default=0.0, null=True, blank=True,
                                 validators=[MinValueValidator(0), MaxValueValidator(1)])
    discount_start = models.DateTimeField(verbose_name=_("Discount Start Time"), null=True, blank=True, )
    discount_end = models.DateTimeField(verbose_name=_("Discount End Time"), null=True, blank=True, )

    def is_in_discount(self):
        pass
