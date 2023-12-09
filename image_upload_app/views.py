from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import CustomUser, Image, ExpiringLink, AccountTier
from .serializers import CustomUserSerializer, ImageSerializer, ExpiringLinkSerializer, AccountTierSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_staff:
            return CustomUser.objects.all()
        return CustomUser.objects.filter(id=self.request.user.id)


class ImageViewSet(viewsets.ModelViewSet):
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AccountTierViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AccountTier.objects.all()
    serializer_class = AccountTierSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ExpiringLinkViewSet(viewsets.ModelViewSet):
    serializer_class = ExpiringLinkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ExpiringLink.objects.filter(image__user=self.request.user)

    @action(detail=True, methods=['get'])
    def fetch_link(self, request, pk=None):
        expiring_link = self.get_object()
        if expiring_link.is_expired():
            return Response({'detail': 'Link has expired'}, status=status.HTTP_410_GONE)
        return Response({'image_url': expiring_link.image.image.url})
