"""
api/users/, api/images/, api/account-tiers/, and api/expiring-links/
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ImageViewSet, AccountTierViewSet, ExpiringLinkViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'images', ImageViewSet)
router.register(r'account-tiers', AccountTierViewSet)
router.register(r'expiring-links', ExpiringLinkViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
