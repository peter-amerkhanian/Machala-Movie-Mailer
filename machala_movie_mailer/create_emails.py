from machala_movie_mailer.retrieve_info import get_movie_info, get_show_times, get_ratings, get_theater_name
from machala_movie_mailer.private_variables import from_address, email_login_password, email_login_user
from machala_movie_mailer.email_tools import create_email_text, create_email_object
from machala_movie_mailer.get_users import get_user_addresses
import os


def make_email_body(theaters):
    """
    turn a list of html for the movies playing at a theater into the body
    of an email with just the english movies
    :param theaters: list of tuples, each containing a theater url, that theater's soup, and the movies at that theater
    :return: a string of today's movies, a string of html of today's movies, and how many movies
    """
    todays_movies = {}
    todays_movies_html = []
    for theater_tuple in theaters:
        movies, soup, url = theater_tuple
        theater, theater_url = get_theater_name(soup, url)
        theater_html = '<a href="{}"> {}</a>'.format(theater_url, theater)
        for movie in movies:
            times = get_show_times(movie)
            english_times = [time for time in times if "english" in time['Language'].lower()]
            film_info = get_movie_info(movie)
            film_title = film_info['title']
            ratings = get_ratings(film_info['title'])
            if film_title in todays_movies and len(english_times):
                show_time_list = ["{}: {}".format(time['Language'].replace(",", ", "),
                                                  time['Times']) for time in english_times]
                show_times_string = "<br/>".join(show_time_list)
                todays_movies[film_title] += "<p>Show-times @ {}<br/>{}</p>".format(theater_html, show_times_string)
                todays_movies_html.append('<p><b><a href="{}">{} </a>@ <a href="{}">{} </a></b></p>'.format(
                    film_info['trailer'],
                    film_info['title'],
                    theater_url,
                    theater))
            elif len(english_times):
                todays_movies_html.append('<p><b><a href="{}">{} </a>@ <a href="{}">{} </a></b></p>'.format(
                    film_info['trailer'],
                    film_info['title'],
                    theater_url,
                    theater))
                body = create_email_text(film_info, english_times, ratings, theater_html)
                todays_movies[film_info['title']] = body
    edit_account = '<p><br/><small><a href="https://machalamoviemailer.com/">*edit account*</a></small></p>'
    all_bodies = [v for k, v in todays_movies.items()]
    return ('<br/>***   ***<br/>'.join(all_bodies) + edit_account,
            "".join(sorted(todays_movies_html, key=lambda x: x.split('>')[3])),
            len(todays_movies))


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
    relative_path = os.path.join("Machala_Movie_Mailer",
                                 "flask_movie_mailer",
                                 "static",
                                 "today_message_{}.txt".format(city))
    with open(os.path.abspath(relative_path), "w") as file:
        file.write(mail)


def make_final_email_objects(num_movies_playing, plural, body, city):
    messages = []
    for to_address in get_user_addresses(city):
        messages.append(create_email_object(from_address,
                                            to_address,
                                            '{} English {} Playing Today'.format(num_movies_playing,
                                                                                 plural),
                                            body))
    return messages


def init_email(server):
    """
    initialize email server
    :param server: an SMTP object
    :return: void
    """
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(email_login_user, email_login_password)
