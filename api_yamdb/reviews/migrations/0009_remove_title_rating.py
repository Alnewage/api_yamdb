# Generated by Django 3.2 on 2023-10-25 15:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0008_auto_20231025_0641'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='title',
            name='rating',
        ),
    ]