from machala_movie_mailer.retrieve_info import get_movie_info, get_show_times, get_ratings, get_theater_name
from machala_movie_mailer.private_variables import from_address, email_login_password, email_login_user
from machala_movie_mailer.email_tools import create_email_text, create_email_object
from machala_movie_mailer.get_users import get_user_addresses


def make_email_body(theaters):
    """
    turn a list of html for the movies playing at a theater into the body
    of an email with just the english movies
    :param _movies: list of BeautifulSoup objects
    :return: a string of today's movies, a string of html of today's movies, and how many movies
    """
    todays_movies = {}
    todays_movies_html = ""
    for theater_tuple in theaters:
        movies, soup, url = theater_tuple
        theater, theater_url = get_theater_name(soup, url)
        theater_html = '<a href="{}"> {}</a>'.format(theater_url, theater)
        for movie in movies:
            times = get_show_times(movie)
            english_times = [time for time in times if "english" in time['Language'].lower()]
            film = get_movie_info(movie)
            ratings = get_ratings(film['title'])
            if film['title'] in todays_movies and len(english_times):
                showtimes = "<br/>".join(["{}: {}".format(time['Language'], time['Times']) for time in english_times])
                todays_movies[film['title']] += "<p>Show-times @ {}<br/>{}</p>".format(theater_html, showtimes)
                todays_movies_html += '<p><b><a href="{}">{} </a>@ <a href="{}">{} </a></b></p>'.format(
                    film['trailer'],
                    film['title'],
                    theater_url,
                    theater)
            elif len(english_times):
                english_time = english_times[0]['Times']
                todays_movies_html += '<p><b><a href="{}">{} </a>@ <a href="{}">{} </a></b></p>'.format(
                    film['trailer'],
                    film['title'],
                    theater_url,
                    theater)
                body = create_email_text(film, english_times, ratings, theater_html)
                todays_movies[film['title']] = body
    edit_account = '<p><br/><small><a href="https://machalamoviemailer.com/">*edit account*</a></small></p>'
    all_bodies = [v for k, v in todays_movies.items()]
    return '<br/>***   ***<br/>'.join(all_bodies) + edit_account, todays_movies_html, len(todays_movies)


def make_html_file(num_movies, _plural, _todays_movies_html, city):
    """
    write a text file with the html of today's movies
    :param num_movies: int, how many movies are playing today
    :param _plural: 'Movie' or 'Movies' depending on how many movies are playing
    :param _todays_movies_html: string with html of today's movies
    :return: void
    """
    mail = "<h5><cite>{} English {} Playing Today: </cite></h5> <p>{}</p> <p></p>".format(
        num_movies, _plural, _todays_movies_html)
    with open(r"flask_movie_mailer/static/today_message_{}.txt".format(city), "w") as file:
        file.write(mail)


def check_for_plural(num_movies):
    """
    check for whether messages should have 'Movie' or 'Movies' in it
    :param num_movies: int of how many movies are playing
    :return: string, 'Movie' or 'Movies' depending on how many movies are playing
    """
    if num_movies > 1:
        return "Movies"
    return "Movie"


def make_final_email_objects(num_movies_playing, plural, body, city):
    messages = []
    for to_address in get_user_addresses(city):
        messages.append(create_email_object(from_address,
                                            to_address,
                                            '{} English {} Playing Today'.format(num_movies_playing,
                                                                                 plural),
                                            body))
    return messages


def init_email(srvr):
    """
    initialize email server
    :param srvr: an SMTP object
    :return: void
    """
    srvr.ehlo()
    srvr.starttls()
    srvr.ehlo()
    srvr.login(email_login_user, email_login_password)
