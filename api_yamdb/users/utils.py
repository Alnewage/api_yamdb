import random
import string

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

User = get_user_model()


def get_confirmation_code():
    """Функция для генерации кода подтверждения."""

    # Генерируем confirmation_code для эксплуатации в продуктовой среде
    # иначе устанавливаем значение 0.
    return ''.join(
        random.choices(string.ascii_letters + string.digits, k=32)
    ) if not settings.DEBUG else 0


def send_confirmation_code(email, username):
    """Функция для отправки кода подтверждения."""

    try:
        confirmation_code = User.objects.get(
            username=username).confirmation_code
    except User.DoesNotExist:
        raise ValueError("Пользователь с таким именем не существует.")
    else:
        subject = 'Подтверждение регистрации'
        message = (f'username: {username}\n'
                   f'Ваш код подтверждения: {confirmation_code}')
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list,
                  fail_silently=False)

    return confirmation_code
