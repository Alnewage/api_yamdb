from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class MyUser(AbstractUser):
    """Класс модели для пользователя. Заменили базовую модель на свою."""

    class Role(models.TextChoices):
        USER = 'user', 'пользователь'
        MODERATOR = 'moderator', 'модератор'
        ADMIN = 'admin', 'админ'

    username = models.CharField('Имя пользователя',
                                max_length=150,
                                unique=True)
    email = models.EmailField('Email',
                              max_length=254,
                              unique=True)
    password = models.CharField('Пароль',
                                max_length=128,
                                blank=True,
                                null=True)
    role = models.CharField('Роль',
                            choices=Role.choices,
                            default=Role.USER,
                            max_length=9)
    bio = models.TextField('Биография', blank=True)
    confirmation_code = models.CharField(max_length=32, default=0)

    def save(self, *args, **kwargs):
        if self.username == "me":
            raise ValidationError(
                {"username": "Username 'me' is not allowed."})
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
