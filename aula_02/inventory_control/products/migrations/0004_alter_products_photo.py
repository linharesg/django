# Generated by Django 5.0.1 on 2024-01-24 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_products_expiration_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='products'),
        ),
    ]