from django.core.management.base import BaseCommand
from django.apps import apps
import csv
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

        try:
            # Получаем класс модели по имени
            model_class = apps.get_model(model_name)

            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                rows_to_create = []
                for row in reader:
                    processed_row = {}
                    for key, value in row.items():
                        try:
                            field_instance = model_class._meta.get_field(key)
                            if isinstance(field_instance, models.ForeignKey):
                                # Если поле - ForeignKey, записываем значение
                                # в поле_id в новом словаре.
                                related_model_id = f'{key}_id'
                                processed_row[related_model_id] = int(value)
                            else:
                                processed_row[key] = value
                        except:
                            pass

                    rows_to_create.append(processed_row)

                # Создаём объекты модели и сохраняем их в базу данных.
                for row in rows_to_create:
                    model_class.objects.create(**row)

            self.stdout.write(self.style.SUCCESS(
                f'Данные из {file_path} успешно импортированы'
                f' в модель {model_name}'))
        except LookupError:
            self.stdout.write(self.style.ERROR(
                f'Модель {model_name} не найдена'))
