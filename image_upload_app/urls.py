"""
api/users/, api/images/, api/account-tiers/, and api/expiring-links/
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ImageViewSet, AccountTierViewSet, ExpiringLinkViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'images', ImageViewSet, basename='image')
router.register(r'account-tiers', AccountTierViewSet, basename='accounttier')
router.register(r'expiring-links', ExpiringLinkViewSet, basename='expiringlink')

urlpatterns = [
    path('', include(router.urls)),
]
