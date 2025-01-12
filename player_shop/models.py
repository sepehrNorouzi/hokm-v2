from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel
from shop.models import Currency, Asset, Market
from user.models import Player, User


class PlayerCurrency(BaseModel):
    currency = models.ForeignKey(to=Currency, on_delete=models.CASCADE, verbose_name=_("Currency"))
    amount = models.PositiveIntegerField(default=0, verbose_name=_("Amount"))

    def __str__(self):
        return f"{self.amount} X {self.currency}"


class PlayerShopInfo(BaseModel):
    player_market = models.ForeignKey(to=Market, on_delete=models.SET_NULL, verbose_name=_("Market"), null=True,
                                      blank=True)
    player = models.OneToOneField(to=User, on_delete=models.RESTRICT, verbose_name=_("Player"),
                                  related_name="shop_info")
    currencies = models.ManyToManyField(to=PlayerCurrency, verbose_name=_("Player Currencies"), blank=True, )
    assets = models.ManyToManyField(to=Asset, verbose_name=_("Assets"), blank=True,)

    def __str__(self):
        return f"{self.player} Shop info"

    class Meta:
        verbose_name = _("Player Shop Info")
        verbose_name_plural = _("Players Shop Info")

    def get_player_currency(self, currency: Currency) -> PlayerCurrency:
        return self.currencies.filter(currency=currency).first()

    def has_enough_credit(self, currency: Currency, amount: int) -> bool:
        if not isinstance(currency, Currency):
            raise ValueError(f"{currency} must be of type Currency")
        player_currency: PlayerCurrency = self.get_player_currency(currency)
        return player_currency.amount >= amount

    def get_player_asset(self, asset: Asset) -> bool:
        return self.assets.filter(asset=asset).first()


class PlayerWalletLog(BaseModel):
    class TransactionType(models.TextChoices):
        SPEND = 'spend', _('Spend')
        EARN = 'earn', _('Earn')

    player = models.ForeignKey(to=User, on_delete=models.RESTRICT, verbose_name=_("Player"),
                               related_name="transactions")
    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)
    transaction_type = models.CharField(max_length=10, choices=TransactionType.choices, default=TransactionType.EARN)
    transaction_id = models.CharField(max_length=255, verbose_name=_("Transaction ID"), null=True, blank=True)
    currency = models.ForeignKey(to=Currency, on_delete=models.SET_NULL, verbose_name=_("Currency"), null=True,
                                 blank=True)
    amount = models.PositiveIntegerField(verbose_name=_("Amount"), null=True, blank=True)
    asset = models.ForeignKey(to=Asset, on_delete=models.SET_NULL, verbose_name=_("Asset"), null=True, blank=True)

    def __str__(self):
        return f"{self.player} - {self.description[5:] if self.description else ''} - {self.created_time}"

    class Meta:
        verbose_name = _("Player Wallet Log")
        verbose_name_plural = _("Player Wallet Logs")
