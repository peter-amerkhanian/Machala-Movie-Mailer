from machala_movie_mailer.retrieve_info import movies, get_movie_info, get_show_times, get_ratings
from machala_movie_mailer import private_variables, emailer
import smtplib
from datetime import datetime
# All information from this module is private:


# Create the email's body
bodies = []
movies_html = ""
for movie in movies:
    film = get_movie_info(movie)
    times = get_show_times(movie)
    ratings = get_ratings(film['title'])
    eng = len([time for time in times if 'english' in time['Language'].lower()])
    if eng:
        body = emailer.make_message(film, times, ratings)
        movies_html += '<p><a href="{}"><b>{}</b></a> {}</p>'.format(film['trailer'], film['title'], times[-1]['Times'])
        bodies.append(body)
# Check if the subject line should have Movie or Movies
if len(bodies) >= 1:
    plural = "Movie"
    if len(bodies) > 1:
        plural = "Movies"
    body = "\n\n***\t***\n".join(bodies)
    # Create an HTML string for the webapp
    mail = "<h5><cite>{} English {} Playing Today: </cite></h5> <p>{}</p> <p></p>".format(
        len(bodies),
        plural,
        movies_html)
    with open(r"../flask_movie_mailer/static/{}_message.txt".format(datetime.today().strftime('%Y-%m-%d')), "w") as file:
        file.write(mail)
    # Create Messages
    if __name__ == "__main__":
        msgs = []
        for to_address in private_variables.to_addresses:
            msgs.append(emailer.create_email_message(private_variables.from_address,
                                                     to_address,
                                                     '{} English {} Playing Today'.format(len(bodies), plural),
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

