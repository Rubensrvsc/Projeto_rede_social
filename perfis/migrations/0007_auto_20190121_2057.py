# Generated by Django 2.1.3 on 2019-01-21 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfis', '0006_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='status',
            name='is_ativo',
        ),
        migrations.AddField(
            model_name='perfil',
            name='is_ativo',
            field=models.BooleanField(default=True),
        ),
    ]
