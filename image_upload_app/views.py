from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import CustomUser, Image, ExpiringLink, AccountTier
from .serializers import *
from rest_framework.permissions import AllowAny
from .constants import TEMP_TOKEN_USER_MAPPING

VALID_TOKENS = {
    'token123': 'User1',
    'token456': 'User2',
    'token789': 'User3',
}


# This is a simple, in-memory mapping. For demonstration purposes only.
# TEMP_TOKEN_USER_MAPPING = {}

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_staff:
            return CustomUser.objects.all()
        return CustomUser.objects.filter(id=self.request.user.id)


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        token = request.data.get('token')
        user_name = VALID_TOKENS.get(token)

        if not user_name:
            return Response({"error": "Invalid or missing token"}, status=status.HTTP_403_FORBIDDEN)

        # Update the temporary mapping with the image ID and user name.
        # You'll save the image first to get its ID.
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        image = serializer.save()  # This now contains the image instance, including its ID.
        TEMP_TOKEN_USER_MAPPING[image.id] = user_name  # Map image ID to user_name.

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AccountTierViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AccountTier.objects.all()
    serializer_class = AccountTierSerializer
    permission_classes = [AllowAny]


class ExpiringLinkViewSet(viewsets.ModelViewSet):
    serializer_class = ExpiringLinkSerializer
    permission_classes = []  # Empty, matching your requirement to not use Django's built-in permissions

    def get_queryset(self):
        # Simply return all ExpiringLink objects.
        return ExpiringLink.objects.all()

    # @action(detail=False, methods=['get'])
    # def list_links(self, request):
    #     # This custom action isn't necessary unless you want to customize
    #     # the response further than what the default 'list' action provides.
    #     # For simplicity, you could rely on the default 'list' implementation.
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)
