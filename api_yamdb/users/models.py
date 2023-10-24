from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


def username_validator(value):
    if value == "me":
        raise ValidationError(
            {"username": "Username 'me' is not allowed."})


class MyUser(AbstractUser):
    username = models.CharField(
        'Имя пользователя', max_length=150, unique=True, validators=[
            username_validator
        ]
    )
    email = models.EmailField('Email', max_length=254, unique=True, )
    password = models.CharField('Пароль', max_length=128, blank=True,
                                null=True)
    role = models.CharField(
        'Роль', choices=settings.ROLE_CHOICES, default='user', max_length=9, )
    bio = models.TextField('Биография', blank=True)
    confirmation_code = models.CharField(max_length=32)

    def __str__(self):
        return self.username
