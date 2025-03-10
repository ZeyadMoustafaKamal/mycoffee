# Generated by Django 4.2.7 on 2023-11-28 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='pdf_file',
            field=models.FileField(blank=True, max_length=200, null=True, upload_to='reports'),
        ),
        migrations.AlterField(
            model_name='report',
            name='stage',
            field=models.CharField(choices=[('Preparing', 'Preparing'), ('Done', 'Done')], default='Preparing', max_length=100),
        ),
    ]
