from rest_framework import serializers
from .models import CustomUser, Image, AccountTier, ExpiringLink
from django.shortcuts import get_object_or_404
from django.utils import timezone


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'account_tier']


class AccountTierSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountTier
        fields = ['id', 'name']


class ImageSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Image
        fields = ['id', 'user', 'image', 'uploaded_at']

    def create(self, validated_data):
        print(self.data)
        # user = self.context['request'].user
        user = CustomUser.objects.first()
        print(validated_data)
        validated_data.pop('user', None)  # If using curl
        print(validated_data)
        image_instance = Image.objects.create(user=user, **validated_data)
        return image_instance


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
