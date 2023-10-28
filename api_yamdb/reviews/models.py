from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    """Класс модели для категории."""

    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Класс модели для жанра."""

    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Класс модели для произведения."""

    name = models.CharField(max_length=256)
    year = models.IntegerField()
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 default=None)
    description = models.TextField(blank=True)
    genre = models.ManyToManyField(Genre, through='TitleGenre')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-name',)
        default_related_name = 'titles'

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    """Класс промежуточной модели для связи Title и Genre."""

    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} - {self.title}'


class Review(models.Model):
    """Модель ревью (отзывы на произведения)"""

    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Автор')
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              verbose_name='Название произведения')
    text = models.TextField(verbose_name='текст ревью')
    score = models.PositiveIntegerField(
        verbose_name='Оценка',
        validators=(
            MaxValueValidator(10,
                              message='Оценка больше допустимой'),
            MinValueValidator(1,
                              message='Оценка меньше допустимой')))
    pub_date = models.DateTimeField(verbose_name='Дата публикации',
                                    auto_now_add=True,
                                    db_index=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        constraints = (models.UniqueConstraint(
            fields=('author', 'title'),
            name='unique_author'),)
        default_related_name = 'reviews'

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Класс модели для комментариев"""

    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Автор')
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               verbose_name='Отзыв')
    text = models.TextField(verbose_name='Текст комментария')
    pub_date = models.DateTimeField(verbose_name='Дата добавления',
                                    auto_now_add=True,
                                    db_index=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)
        default_related_name = 'comments'

    def __str__(self):
        return self.text
