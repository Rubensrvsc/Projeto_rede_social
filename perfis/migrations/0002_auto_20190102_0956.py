# Generated by Django 2.1.3 on 2019-01-02 12:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('perfis', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.CharField(max_length=140)),
                ('data', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Timeline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('perfil', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='timeline', to='perfis.Perfil')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='timeline',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_timeline', to='perfis.Timeline'),
        ),
    ]
