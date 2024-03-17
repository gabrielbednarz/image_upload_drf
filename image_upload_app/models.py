from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from datetime import timedelta
from image_upload_app.validators import validate_image_file_type
from django.utils import timezone


class CustomUser(AbstractUser):
    account_tier = models.ForeignKey('AccountTier', on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        if self.account_tier is None:
            basic_tier, created = AccountTier.objects.get_or_create(
                name='Basic',
                defaults={
                    'thumbnail_sizes': [200],
                    'has_original_link': False,
                    'can_generate_expiring_link': False,
                    'is_builtin': True,
                }
            )
            self.account_tier = basic_tier
        super().save(*args, **kwargs)


class Image(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='images/uploads/', validators=[validate_image_file_type])
    uploaded_at = models.DateTimeField(auto_now_add=True)


class AccountTier(models.Model):
    BASIC = 'Basic'
    PREMIUM = 'Premium'
    ENTERPRISE = 'Enterprise'

    ACCOUNT_TIER_CHOICES = [
        (BASIC, 'Basic'),
        (PREMIUM, 'Premium'),
        (ENTERPRISE, 'Enterprise'),
    ]

    name = models.CharField(max_length=255, unique=True, choices=ACCOUNT_TIER_CHOICES)

    def __str__(self):
        return self.name


class ExpiringLink(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    expiration_date = models.DateTimeField(default=timezone.now)  # Default to current time

    def is_expired(self):
        return timezone.now() >= self.expiration_date

    def save(self, *args, **kwargs):
        if not self.pk:
            self.expiration_date = timezone.now() + timedelta(seconds=300)  # Fixed expiration time
        super().save(*args, **kwargs)
