# Generated by Django 5.1.3 on 2024-12-12 13:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_accommodation_remove_application_landlord_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accommodation',
            name='images',
        ),
        migrations.CreateModel(
            name='AccommodationImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='accommodation_images/')),
                ('accommodation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='home.accommodation')),
            ],
        ),
        migrations.DeleteModel(
            name='LandlordImage',
        ),
    ]
