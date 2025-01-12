from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user.urls import router as user_router
from shop.urls import router as shop_router

router = DefaultRouter()

router.registry.extend(user_router.registry)
router.registry.extend(shop_router.registry)

urlpatterns = [
    path('', lambda request: redirect(to='admin/', permenant=True)),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]

