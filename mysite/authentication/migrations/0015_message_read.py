# Generated by Django 5.0.6 on 2024-08-06 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0014_message_authenticat_sender__baba19_idx_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='read',
            field=models.BooleanField(default=False),
        ),
    ]