# Generated by Django 2.1.3 on 2019-01-08 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfis', '0005_perfil_bloq'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='bloq',
            field=models.ManyToManyField(blank=True, null=True, related_name='bloqueado', to='perfis.Perfil'),
        ),
    ]