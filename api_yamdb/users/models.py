from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class MyUser(AbstractUser):
    email = models.EmailField('Email', max_length=128, unique=True, )
    password = models.CharField('Пароль', max_length=128, blank=True,
                                null=True)
    role = models.CharField(
        'Роль', choices=settings.ROLE_CHOICES, default='user', max_length=9, )
    bio = models.TextField('Биография', blank=True)
    confirmation_code = models.CharField(max_length=32)

    # objects = CustomUserManager()

    def clean(self):
        super().clean()  # Вызываем базовую валидацию

        # Дополнительная валидация
        if self.username == "me":
            raise ValidationError(
                {"username": "Username 'me' is not allowed."})

    def save(self, *args, **kwargs):
        self.full_clean()  # Вызываем валидацию перед сохранением
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username