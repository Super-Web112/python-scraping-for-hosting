# Generated by Django 3.1.4 on 2021-01-06 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20210106_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='aboutMe',
            field=models.TextField(),
        ),
    ]
