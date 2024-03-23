from rest_framework import serializers
from .models import CustomUser, Image, AccountTier, ExpiringLink
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .constants import TEMP_TOKEN_USER_MAPPING
# TEMP_TOKEN_USER_MAPPING = {}



class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'account_tier']


class AccountTierSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountTier
        fields = ['id', 'name']


class ImageSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ['id', 'user', 'image', 'uploaded_at', 'image_url']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

    # def get_user(self, obj):
    #     return obj.user.username if obj.user else None
    #
    #     # return self.context['request'].data.get('user_name', None)

    def get_user(self, obj):
        # Use the temporary mapping to get the user name based on the image ID.
        return TEMP_TOKEN_USER_MAPPING.get(obj.id)
    def create(self, validated_data):
        validated_data.pop('user_name', None)
        return super().create(validated_data)

class ExpiringLinkSerializer(serializers.ModelSerializer):
    image = ImageSerializer(read_only=True)
    is_expired = serializers.SerializerMethodField()

    class Meta:
        model = ExpiringLink
        fields = ['id', 'image', 'token', 'is_expired']

    def get_is_expired(self, obj):
        return obj.is_expired()

    def create(self, validated_data):
        user = self.context['request'].user
        if not user.account_tier.can_generate_expiring_link:
            raise serializers.ValidationError("The user's account tier does not allow generating expiring links.")
        image_id = self.context['view'].kwargs['image_id']
        image = get_object_or_404(Image, id=image_id, user=user)
        expiring_link_instance = ExpiringLink.objects.create(image=image, **validated_data)
        return expiring_link_instance
