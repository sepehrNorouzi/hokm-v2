from user.views import NormalPlayerAuthView, GuestPlayerAuthView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('user/auth/player', NormalPlayerAuthView, basename='auth-player')
router.register('user/auth/player', GuestPlayerAuthView, basename='auth-guest')
