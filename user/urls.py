from django.urls import path
from user.views import UserAuthView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('user/auth', UserAuthView, basename='auth')

