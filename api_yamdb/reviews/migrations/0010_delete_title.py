# Generated by Django 3.2 on 2023-10-25 17:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0009_remove_title_rating'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Title',
        ),
    ]
