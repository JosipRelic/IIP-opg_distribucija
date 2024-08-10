# Generated by Django 5.0.3 on 2024-08-03 17:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('opg_ponuda', '0004_alter_proizvodi_kategorija_proizvoda'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Kosarica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kolicina', models.PositiveIntegerField()),
                ('kreirano', models.DateTimeField(auto_now_add=True)),
                ('izmijenjeno', models.DateTimeField(auto_now=True)),
                ('korisnik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('proizvod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='opg_ponuda.proizvodi')),
            ],
        ),
    ]