from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import AccountTier
from .serializers import CustomUserSerializer
from rest_framework.test import APIClient
from rest_framework import status


class ModelTests(TestCase):
    def test_create_user(self):
        user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')

    def test_create_account_tier(self):
        account_tier, created = AccountTier.objects.get_or_create(
            name='Basic'
        )
        self.assertEqual(account_tier.name, 'Basic')


class SerializerTests(TestCase):
    def test_serialize_custom_user(self):
        user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123'
        )
        serializer = CustomUserSerializer(user)
        self.assertEqual(serializer.data['username'], user.username)


class ViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123',
            is_staff=True
        )
        self.client.force_authenticate(user=self.user)

    def test_retrieve_users(self):
        """Test retrieving a list of users"""
        response = self.client.get('/api/users/')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
