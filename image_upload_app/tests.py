from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import AccountTier
from .serializers import CustomUserSerializer
from rest_framework.test import APIClient
from rest_framework import status

class ModelTests(TestCase):
    """
    Tests for database models.
    """

    def test_create_user(self):
        """
        Test creating a user with a username and password.
        """
        user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')

    def test_create_account_tier(self):
        """
        Test creating an account tier entry.
        """
        account_tier, created = AccountTier.objects.get_or_create(
            name='Basic'
        )
        self.assertEqual(account_tier.name, 'Basic')


class SerializerTests(TestCase):
    """
    Tests for data serialization.
    """

    def test_serialize_custom_user(self):
        """
        Test serializing a user object.
        """
        user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123'
        )
        serializer = CustomUserSerializer(user)
        self.assertEqual(serializer.data['username'], user.username)


class ViewTests(TestCase):
    """
    Tests for API views.
    """

    def setUp(self):
        """
        Setup method to run before each test case.
        """
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123',
            is_staff=True
        )
        self.client.force_authenticate(user=self.user)

    def test_retrieve_users(self):
        """
        Test retrieving a list of users via API.
        """
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Additional checks can be added here to validate the response data
