# Generated by Django 5.0.3 on 2024-03-27 15:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('korisnicki_racuni', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='KorisnickiProfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slika_profila', models.ImageField(blank=True, null=True, upload_to='korisnici/slike_profila')),
                ('naslovna_slika', models.ImageField(blank=True, null=True, upload_to='korisnici/naslovne_slike')),
                ('adresa_1', models.CharField(blank=True, max_length=100, null=True)),
                ('adresa_2', models.CharField(blank=True, max_length=100, null=True)),
                ('drzava', models.CharField(blank=True, max_length=100, null=True)),
                ('zupanija', models.CharField(blank=True, max_length=100, null=True)),
                ('grad', models.CharField(blank=True, max_length=100, null=True)),
                ('postanski_broj', models.CharField(blank=True, max_length=8, null=True)),
                ('latituda', models.CharField(blank=True, max_length=50, null=True)),
                ('longituda', models.CharField(blank=True, max_length=50, null=True)),
                ('kreirano', models.DateTimeField(auto_now_add=True)),
                ('izmijenjeno', models.DateTimeField(auto_now=True)),
                ('korisnik', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Korisnicki profili',
            },
        ),
    ]
