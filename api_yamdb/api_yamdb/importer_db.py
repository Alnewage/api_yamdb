import csv
import sqlite3

def import_csv_to_sqlite(csv_filename, db_name, table_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    with open(csv_filename, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Пропускаем заголовок CSV

        for row in reader:
            placeholders = ', '.join(['?'] * len(row))
            cursor.execute(f"INSERT INTO {table_name}"
                           f" VALUES ({placeholders});",
                           row)

    conn.commit()
    conn.close()

# Пример использования функции для каждого CSV файла
import_csv_to_sqlite('static/data/category.csv',
                     'db.sqlite3',
                     'reviews_category')
import_csv_to_sqlite('static/data/comments.csv',
                     'db.sqlite3',
                     'reviews_comment')
import_csv_to_sqlite('static/data/genre.csv',
                     'db.sqlite3',
                     'reviews_genre')
import_csv_to_sqlite('static/data/genre_title.csv',
                     'db.sqlite3',
                     'reviews_titlegenre')
import_csv_to_sqlite('static/data/review.csv',
                     'db.sqlite3',
                     'reviews_review')
import_csv_to_sqlite('static/data/titles.csv',
                     'db.sqlite3',
                     'reviews_title')
import_csv_to_sqlite('static/data/users.csv',
                     'db.sqlite3',
                     'users_myuser')
