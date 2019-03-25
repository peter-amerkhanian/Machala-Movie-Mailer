from machala_movie_mailer.private_variables import db_connection
from email.headerregistry import Address
import psycopg2


def get_users(city):
    conn = psycopg2.connect(db_connection)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM "user" WHERE location=\'{}\''.format(city))
    users = cursor.fetchall()
    return users


def get_user_addresses(city):
    users = get_users(city)
    for user in users:
        email = user[2].split("@")
        yield Address(display_name=user[1],
                      username=email[0],
                      domain=email[1])