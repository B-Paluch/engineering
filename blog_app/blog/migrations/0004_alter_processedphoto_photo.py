# Generated by Django 3.2.9 on 2022-01-09 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_processedphoto_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processedphoto',
            name='photo',
            field=models.ImageField(upload_to='data'),
        ),
    ]
