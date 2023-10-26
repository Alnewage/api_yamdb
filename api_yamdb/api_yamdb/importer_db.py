# import csv
# import sqlite3
#
#
# def import_csv_to_sqlite(csv_filename, db_name, table_name):
#     conn = sqlite3.connect(db_name)
#     cursor = conn.cursor()
#
#     with open(csv_filename, 'r') as file:
#         reader = csv.reader(file)
#         next(reader)
#
#         for row in reader:
#             cursor.execute(
#                 f"INSERT INTO {table_name} VALUES ({', '.join(['?' for _ in row])});", row
#             )
#
#     conn.commit()
#     conn.close()
#
# import_csv_to_sqlite(
#     'static/data/genre.csv', 'db.sqlite3', 'reviews_genre'
# )
# import_csv_to_sqlite(
#     'static/data/category.csv', 'db.sqlite3', 'reviews_category'
# )
# import_csv_to_sqlite(
#     'static/data/titles.csv', 'db.sqlite3', 'reviews_title'
# )
# import_csv_to_sqlite(
#     'static/data/genre_title.csv', 'db.sqlite3', 'reviews_title_genre'
# )
