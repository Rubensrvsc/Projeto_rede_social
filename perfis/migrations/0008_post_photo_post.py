# Generated by Django 2.1.3 on 2019-01-26 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfis', '0007_auto_20190121_2057'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='photo_post',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
