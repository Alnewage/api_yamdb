# Generated by Django 3.2 on 2023-10-24 04:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('year', models.IntegerField()),
                ('description', models.TextField()),
                ('category', models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='reviews.category')),
                ('genre', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='reviews.genre')),
            ],
        ),
    ]
