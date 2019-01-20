from retrieve_info import movies, get_movie_info, get_show_times, get_ratings
import emailer
import smtplib
from datetime import datetime
# All information from this module is private:
import private_variables

if __name__ == "__main__":
    bodies = []
    for movie in movies:
        film = get_movie_info(movie)
        times = get_show_times(movie)
        ratings = get_ratings(film['title'])
        eng = len([time for time in times if 'english' in time['Language'].lower()])
        if eng:
            body = emailer.make_message(film, times, ratings)
            bodies.append(body)
    if len(bodies) >= 1:
        if len(bodies) == 1:
            plural = "Movie"
        if len(bodies) > 1:
            plural = "Movies"
        body = "\n\n***\t***\n".join(bodies)
        msg = emailer.create_email_message(emailer.from_address,
                                           emailer.to_address,
                                           '{} English {} Playing Today'.format(len(bodies), plural),
                                           body)
        with smtplib.SMTP('smtp.gmail.com', port=587) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(private_variables.from_address['Email'], private_variables.email_password)
            server.send_message(msg)
        print("Email sent successfully!\n...\n", msg.get_content())
    else:
        print('No email sent today: {}\n'.format(datetime.today().strftime('%Y-%m-%d')))