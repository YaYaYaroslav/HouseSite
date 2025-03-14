# Generated by Django 5.1.7 on 2025-03-11 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parser_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PropertyInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(unique=True)),
                ('images', models.TextField(blank=True)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('cost', models.CharField(blank=True, max_length=255)),
                ('details', models.TextField(blank=True)),
                ('wordwrap', models.TextField(blank=True)),
                ('highlights', models.TextField(blank=True)),
                ('address', models.TextField(blank=True)),
                ('location', models.TextField(blank=True)),
                ('about_place', models.TextField(blank=True)),
                ('nearby_places', models.TextField(blank=True)),
                ('seller_info', models.JSONField(blank=True, default=dict)),
                ('whatsapp', models.CharField(blank=True, max_length=255)),
                ('now_on_ad', models.CharField(blank=True, max_length=255)),
            ],
        ),
    ]
