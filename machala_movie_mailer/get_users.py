import psycopg2
from machala_movie_mailer.private_variables import db_connection
from email.headerregistry import Address


def get_users():
    conn = psycopg2.connect(db_connection)
    print("connection established to DB")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM "user" WHERE location=\'Machala\'')
    users = cursor.fetchall()
    return users


def get_user_addresses():
    users = get_users()
    for user in users:
        email = user[2].split("@")
        yield Address(display_name=user[1],
                      username=email[0],
                      domain=email[1])