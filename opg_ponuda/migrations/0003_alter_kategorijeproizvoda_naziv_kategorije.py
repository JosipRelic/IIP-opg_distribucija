# Generated by Django 5.0.3 on 2024-05-27 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opg_ponuda', '0002_alter_kategorijeproizvoda_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kategorijeproizvoda',
            name='naziv_kategorije',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
