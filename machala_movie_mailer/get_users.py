import psycopg2
from machala_movie_mailer.private_variables import db_connection
from email.headerregistry import Address

conn = psycopg2.connect(db_connection)

cursor = conn.cursor()
cursor.execute('SELECT * FROM "user";')
rows = cursor.fetchall()


def make_users(users):
    for user in users:
        email = user[2].split("@")
        yield Address(display_name=user[1],
                      username=email[0],
                      domain=email[1])


print(list(make_users(rows)))
