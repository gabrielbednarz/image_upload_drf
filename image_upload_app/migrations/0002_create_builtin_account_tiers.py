from django.db import migrations


def create_builtin_account_tiers(apps, schema_editor):
    AccountTier = apps.get_model('image_upload_app', 'AccountTier')
    # Create Basic tier if it doesn't exist
    AccountTier.objects.get_or_create(
        name='Basic',
        defaults={
            'thumbnail_sizes': [200],
            'has_original_link': False,
            'can_generate_expiring_link': False,
            'is_builtin': True,
        }
    )
    # Create Premium tier if it doesn't exist
    AccountTier.objects.get_or_create(
        name='Premium',
        defaults={
            'thumbnail_sizes': [200, 400],
            'has_original_link': True,
            'can_generate_expiring_link': False,
            'is_builtin': True,
        }
    )
    # Create Enterprise tier if it doesn't exist
    AccountTier.objects.get_or_create(
        name='Enterprise',
        defaults={
            'thumbnail_sizes': [200, 400],
            'has_original_link': True,
            'can_generate_expiring_link': True,
            'is_builtin': True,
        }
    )


class Migration(migrations.Migration):
    dependencies = [
        ('image_upload_app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_builtin_account_tiers),
    ]
