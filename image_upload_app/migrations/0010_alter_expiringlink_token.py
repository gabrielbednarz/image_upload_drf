# Generated by Django 4.2.5 on 2024-03-23 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image_upload_app', '0009_remove_image_token_alter_customuser_account_tier_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expiringlink',
            name='token',
            field=models.CharField(editable=False, max_length=255),
        ),
    ]
