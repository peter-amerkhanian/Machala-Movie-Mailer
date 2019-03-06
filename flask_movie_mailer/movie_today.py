from datetime import datetime

path = r"flask_movie_mailer/static/{}_message.txt".format(datetime.today().strftime('%Y-%m-%d'))

with open(path, 'r') as f:
    movie_today = f.read()
