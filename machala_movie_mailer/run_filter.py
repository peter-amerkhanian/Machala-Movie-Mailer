from machala_movie_mailer.retrieve_info import movies, get_movie_info, get_show_times, get_ratings
from machala_movie_mailer import private_variables, email_tools, get_users
import smtplib
from datetime import datetime


def make_email_body(_movies):
    todays_movies = []
    todays_movies_html = ""
    for movie in _movies:
        film = get_movie_info(movie)
        times = get_show_times(movie)
        ratings = get_ratings(film['title'])
        english_times = [time["Times"] for time in times if 'english' in time['Language'].lower()]
        english_bool = len(english_times)
        if english_bool:
            body = email_tools.create_email_text(film, times, ratings)
            english_time = english_times[0]
            todays_movies_html += '<p><a href="{}"><b>{}</b></a> {}</p>'.format(film['trailer'],
                                                                                film['title'],
                                                                                english_time)
            todays_movies.append(body)
    return "\n\n***\t***\n".join(todays_movies), todays_movies_html, len(todays_movies)


def make_html_file(num_movies, _plural, _todays_movies_html):
    mail = "<h5><cite>{} English {} Playing Today: </cite></h5> <p>{}</p> <p></p>".format(
        num_movies, _plural, _todays_movies_html)
    with open(r"../flask_movie_mailer/static/today_message.txt", "w") as file:
        file.write(mail)


def check_for_plural(num_movies):
    if num_movies > 1:
        return "Movies"
    return "Movie"


def make_final_email_objects():
    messages = []
    for to_address in get_users.get_user_addresses():
        messages.append(email_tools.create_email_object(private_variables.from_address,
                                                        to_address,
                                                        '{} English {} Playing Today'.format(num_movies_playing,
                                                                                             plural),
                                                        body))
    return messages


def init_email(srvr):
    srvr.ehlo()
    srvr.starttls()
    srvr.ehlo()
    srvr.login(private_variables.email_login_user, private_variables.email_login_password)


if __name__ == "__main__":
    body, movies_html, num_movies_playing = make_email_body(movies)
    if num_movies_playing:
        plural = check_for_plural(num_movies_playing)
        msgs = make_final_email_objects()
        with smtplib.SMTP('smtp.gmail.com', port=587) as server:
            init_email(server)
            for msg in msgs:
                server.send_message(msg)
        print("Email sent successfully!\n", "-"*10, "\n", body, "\n", "-"*10)
        make_html_file(num_movies_playing, plural, movies_html)
    else:
        print('No email sent today: {}\n'.format(datetime.today().strftime('%Y-%m-%d')))

