# Generated by Django 3.1.4 on 2021-01-06 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20210106_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(upload_to='static/assets/img/'),
        ),
    ]
