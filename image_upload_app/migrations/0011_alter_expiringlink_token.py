# Generated by Django 4.2.5 on 2024-03-23 22:49

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('image_upload_app', '0010_alter_expiringlink_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expiringlink',
            name='token',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
