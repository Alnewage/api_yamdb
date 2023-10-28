import csv
import os

from django.apps import apps
from django.core.exceptions import FieldDoesNotExist
from django.core.management.base import BaseCommand
from django.db import models


class Command(BaseCommand):
    help = 'Команда для загрузки данных из CSV в указанную модель'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Путь к CSV-файлу')
        parser.add_argument('model_name', type=str,
                            help='Имя модели (например: app_name.ModelName)')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        model_name = kwargs['model_name']

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'Файл {file_path} не найден'))
            return  # Прерываем выполнение, так как файл не существует

        try:
            # Получаем класс модели по имени
            model_class = apps.get_model(model_name)
        except LookupError:
            self.stdout.write(self.style.ERROR(
                f'Модель {model_name} не найдена'))
            return  # Прерываем выполнение, так как модель не найдена

        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows_to_create = []

            for row in reader:
                processed_row = {}
                for key, value in row.items():
                    try:
                        field_instance = model_class._meta.get_field(key)
                    except FieldDoesNotExist:
                        pass
                    if not isinstance(field_instance, models.ForeignKey):
                        processed_row[key] = value
                    else:
                        if not key.endswith("_id"):
                            key_id = f'{key}_id'
                            processed_row[key_id] = int(value)
                        else:
                            processed_row[key] = int(value)

                rows_to_create.append(model_class(**processed_row))

            # Используем bulk_create для создания объектов модели
            model_class.objects.bulk_create(rows_to_create)

        self.stdout.write(self.style.SUCCESS(
            f'Данные из {file_path} успешно импортированы'
            f' в модель {model_name}'))
