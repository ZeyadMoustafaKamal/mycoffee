# Generated by Django 4.2.4 on 2023-09-16 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_product_image'),
        ('accounts', '0002_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='favourites',
            field=models.ManyToManyField(to='products.product'),
        ),
    ]
