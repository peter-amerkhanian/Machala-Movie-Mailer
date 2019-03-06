import json
import random

path = r"flask_movie_mailer/static/goodbye_quotes.json"

with open(path, 'r') as f:
    quotes = json.load(f)


def generate_random_quote():
    quote = quotes[random.randint(0, len(quotes)-1)]
    return quote