# Generated by Django 5.0.6 on 2024-08-01 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_customuser_otp_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='password_reset_token',
            field=models.CharField(blank=True, max_length=36, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='token_created_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]