from .retrieve_info import movies, get_movie_info, get_show_times, get_ratings
from . import private_variables, email_tools
import smtplib
from datetime import datetime
# All information from this module is private:


def make_html_file(_todays_movies, _plural, _todays_movies_html):
    mail = "<h5><cite>{} English {} Playing Today: </cite></h5> <p>{}</p> <p></p>".format(
        len(_todays_movies), _plural, _todays_movies_html)
    with open(r"../flask_movie_mailer/static/today_message.txt", "w") as file:
        file.write(mail)


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
    return todays_movies, todays_movies_html


# Create the email's body
todays_movies, todays_movies_html = make_email_body(movies)
# Check if the subject line should have Movie or Movies
if len(todays_movies) >= 1:
    plural = "Movie"
    if len(todays_movies) > 1:
        plural = "Movies"
    body = "\n\n***\t***\n".join(todays_movies)
    # Create an HTML string for the webapp
    make_html_file(todays_movies, plural, todays_movies_html)
    # Create & send messages
    if __name__ == "__main__":
        msgs = []
        for to_address in private_variables.to_addresses:
            msgs.append(email_tools.create_email_object(private_variables.from_address,
                                                        to_address,
                                                     '{} English {} Playing Today'.format(len(todays_movies), plural),
                                                        body))
        with smtplib.SMTP('smtp.gmail.com', port=587) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(private_variables.email_login_user, private_variables.email_login_password)
            for msg in msgs:
                server.send_message(msg)
        print("Email sent successfully!\n", "-"*10, "\n", body, "\n", "-"*10)
else:
    print('No email sent today: {}\n'.format(datetime.today().strftime('%Y-%m-%d')))

