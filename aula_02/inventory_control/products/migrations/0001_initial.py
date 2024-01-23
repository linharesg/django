# Generated by Django 5.0.1 on 2024-01-23 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('sale_price', models.DecimalField(decimal_places=2, max_digits=11)),
                ('is_perishable', models.BooleanField()),
                ('expiration_date', models.DateField()),
                ('photo', models.ImageField(blank=True, upload_to='uploads')),
                ('enabled', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
