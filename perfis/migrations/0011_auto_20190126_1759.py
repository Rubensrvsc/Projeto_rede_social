# Generated by Django 2.1.3 on 2019-01-26 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfis', '0010_auto_20190126_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='photo_post',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
