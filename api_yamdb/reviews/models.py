from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, default=None
    )
    description = models.TextField(null=True, blank=True)
    genre = models.ManyToManyField(Genre, through='TitleGenre')

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE,)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} - {self.title}'
