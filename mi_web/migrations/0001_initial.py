# Generated by Django 5.0.7 on 2024-09-19 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('rut', models.CharField(max_length=12)),
                ('cargo', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=50, verbose_name='usuario')),
                ('nombre', models.CharField(max_length=50, verbose_name='nombre')),
                ('email', models.EmailField(max_length=50, verbose_name='email')),
                ('password', models.CharField(max_length=50, verbose_name='password')),
            ],
        ),
    ]
