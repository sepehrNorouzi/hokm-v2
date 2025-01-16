from rest_framework.routers import DefaultRouter

from player_shop.views import PlayerWalletViewSet

router = DefaultRouter()

router.register('player_shop/wallet', PlayerWalletViewSet, basename='wallet')
