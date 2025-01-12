from rest_framework.routers import DefaultRouter

from shop.views import ShopViewSet, MarketViewSet

router = DefaultRouter()

router.register('shop', ShopViewSet, basename='shop')
router.register('market', MarketViewSet, basename='market')
