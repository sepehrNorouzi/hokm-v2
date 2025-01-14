from django.contrib import admin

from player_shop.models import PlayerWallet, PlayerWalletLog, CurrencyBalance, AssetOwnership


class PlayerCurrencyAdminInline(admin.TabularInline):
    model = CurrencyBalance
    extra = 1


class PlayerAssetAdminInline(admin.TabularInline):
    model = AssetOwnership
    extra = 1


@admin.register(PlayerWallet)
class PlayerWalletAdmin(admin.ModelAdmin):
    inlines = [PlayerCurrencyAdminInline, PlayerAssetAdminInline]


@admin.register(PlayerWalletLog)
class PlayerWalletLogAdmin(admin.ModelAdmin):
    pass


