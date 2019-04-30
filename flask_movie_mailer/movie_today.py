from datetime import datetime


def get_movie_today(city):
    path = r"flask_movie_mailer/static/today_message_{}.txt".format(city)

    with open(path, 'r') as f:
        movie_today = f.read()
    return movie_today
