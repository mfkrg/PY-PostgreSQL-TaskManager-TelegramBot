import psycopg2
from config import host, user, password, db_name

try:
    # подключение к базе данных
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    connection.autocommit = True

    #методы для sql команл
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT version();"
        )

        print(f'Server version: {cursor.fetchone()}')

    #создание таблицы
    #with connection.cursor() as cursor:
    #   cursor.execute(
    #       """CREATE TABLE users(
    #       id serial PRIMARY KEY, first_name varchar(50) NOT NULL, nickname varchar(60) NOT NULL);"""
    #   )

    #   print("Table created successfully!")

    #заливаем данные
    with connection.cursor() as cursor:
        cursor.execute(
            """INSERT INTO users(first_name, nickname) VALUES ('Zahar', 'mfkrg1');"""
        )

        print("Data was successfully inserted!")


except Exception as _ex:
    print("Error while working with PostgreSQL!", _ex)
finally:
    if connection:
        # закрываем соединение
        connection.close()
        print("PostgreSQL connection closed!")