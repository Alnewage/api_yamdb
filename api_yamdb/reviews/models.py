from django.db import models


class Category(models.Model):
    name = models.CharField(unique=True, max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    name = models.CharField(unique=True, max_length=256,)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, default=None,
        related_name='categiry',
    )
    description = models.TextField(null=True, blank=True)
    genre = models.ManyToManyField(Genre, related_name='genre')

    def __str__(self) -> str:
        return self.name
