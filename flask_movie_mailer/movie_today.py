from datetime import datetime

path = r"flask_movie_mailer/static/today_message.txt"

with open(path, 'r') as f:
    movie_today = f.read()
