# Generated by Django 3.2 on 2023-10-26 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0011_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=256, unique=True),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(max_length=256, unique=True),
        ),
    ]
