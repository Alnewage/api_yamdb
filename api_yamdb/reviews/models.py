from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)


class Title(models.Model):
    text = models.TextField()
    year = models.IntegerField()
    description = models.TextField()
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL, null=True, default=None
    )
    category = models.OneToOneField(
        Category, on_delete=models.SET_NULL, null=True, default=None
    )
    