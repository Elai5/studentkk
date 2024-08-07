# Generated by Django 5.0.6 on 2024-08-05 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0012_culture_short_description_housing_short_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='culture',
            name='image',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='housing',
            name='image',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='transport',
            name='image',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='culture',
            name='country',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='culture',
            name='short_description',
            field=models.TextField(default='Default description'),
        ),
        migrations.AlterField(
            model_name='housing',
            name='country',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='housing',
            name='short_description',
            field=models.TextField(default='Default description'),
        ),
        migrations.AlterField(
            model_name='transport',
            name='country',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='transport',
            name='short_description',
            field=models.TextField(default='Default description'),
        ),
    ]
