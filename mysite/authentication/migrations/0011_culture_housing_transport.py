# Generated by Django 5.0.6 on 2024-08-05 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0010_city_state_customuser_city_customuser_state_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Culture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(choices=[('USA', 'United States'), ('UK', 'United Kingdom'), ('Canada', 'Canada'), ('Australia', 'Australia'), ('Germany', 'Germany'), ('Netherlands', 'Netherlands')], max_length=100)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Housing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(choices=[('USA', 'United States'), ('UK', 'United Kingdom'), ('Canada', 'Canada'), ('Australia', 'Australia'), ('Germany', 'Germany'), ('Netherlands', 'Netherlands')], max_length=100)),
                ('title', models.CharField(max_length=200)),
                ('link', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Transport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(choices=[('USA', 'United States'), ('UK', 'United Kingdom'), ('Canada', 'Canada'), ('Australia', 'Australia'), ('Germany', 'Germany'), ('Netherlands', 'Netherlands')], max_length=100)),
                ('title', models.CharField(max_length=200)),
                ('link', models.URLField()),
            ],
        ),
    ]