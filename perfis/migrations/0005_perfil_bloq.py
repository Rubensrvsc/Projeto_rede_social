
# Generated by Django 2.1.3 on 2019-01-08 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfis', '0004_perfil_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='bloq',

            field=models.ManyToManyField(blank=True, null=True, related_name='bloqueado', to='perfis.Perfil'),
        ),
    ]
