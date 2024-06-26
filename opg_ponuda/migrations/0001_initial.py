# Generated by Django 5.0.3 on 2024-05-27 19:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('opg', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='KategorijeProizvoda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naziv_kategorije', models.CharField(unique=True, verbose_name=100)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('opis_kategorije', models.TextField(blank=True, max_length=300)),
                ('kreirano', models.DateTimeField(auto_now_add=True)),
                ('izmijenjeno', models.DateTimeField(auto_now=True)),
                ('opg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='opg.opg')),
            ],
        ),
        migrations.CreateModel(
            name='Proizvodi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naziv_proizvoda', models.CharField(max_length=80)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('opis_proizvoda', models.TextField(blank=True, max_length=300)),
                ('cijena_proizvoda', models.DecimalField(decimal_places=2, max_digits=10)),
                ('slika_proizvoda', models.ImageField(upload_to='slike_proizvoda')),
                ('proizvod_dostupan', models.BooleanField(default=True)),
                ('kreirano', models.DateTimeField(auto_now_add=True)),
                ('izmijenjeno', models.DateTimeField(auto_now=True)),
                ('kategorija_proizvoda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='opg_ponuda.kategorijeproizvoda')),
                ('opg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='opg.opg')),
            ],
        ),
    ]
