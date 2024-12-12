# Generated by Django 5.1.3 on 2024-12-06 00:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_alter_student_bursary_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='LandlordImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='landlord_images/')),
                ('landlord', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='landlord_images', to='home.landlord')),
            ],
        ),
    ]
