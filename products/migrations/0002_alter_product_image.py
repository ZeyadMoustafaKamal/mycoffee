# Generated by Django 4.2.4 on 2023-09-15 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(max_length=500, upload_to='product_images'),
        ),
    ]
