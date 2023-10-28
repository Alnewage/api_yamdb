"""
Для импорта всех данных в БД из CSV-файлов запустите команду:
python import_all_data_to_db.py
"""
import subprocess

base_text = "python manage.py "


def run_django_commands(commands):
    for command in commands:
        subprocess.run(base_text + command, shell=True)


django_commands = [
    "migrate",
    "import_data static/data/users.csv users.MyUser",
    "import_data static/data/category.csv reviews.Category",
    "import_data static/data/genre.csv reviews.Genre",
    "import_data static/data/titles.csv reviews.Title",
    "import_data static/data/review.csv reviews.Review",
    "import_data static/data/comments.csv reviews.Comment",
    "import_data static/data/genre_title.csv reviews.TitleGenre",
]

run_django_commands(django_commands)
print("Все команды выполнены")
