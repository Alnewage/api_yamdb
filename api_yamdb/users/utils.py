import random
import string

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import render

User = get_user_model()


def get_confirmation_code():
    return ''.join(
        random.choices(string.ascii_letters + string.digits, k=32)
    )


def send_confirmation_code(email, username):
    try:
        confirmation_code = User.objects.get(
            username=username).confirmation_code
    except User.DoesNotExist:
        raise ValueError("Пользователь с таким именем не существует.")
    else:
        # Отправка письма с confirmation_code
        subject = 'Подтверждение регистрации'
        message = (f'username: {username}\n'
                   f'Ваш код подтверждения: {confirmation_code}')
        from_email = 'noreply@example.com'
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list,
                  fail_silently=False)

    # Вернуть confirmation_code для дальнейшей проверки
    return confirmation_code
