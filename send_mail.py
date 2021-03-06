from machala_movie_mailer import get_movies, make_email_body, make_final_email_objects, init_email, make_html_file
import os
import smtplib
from datetime import datetime


if __name__ == "__main__":
    for city in ['Machala', 'Cuenca', 'La Libertad', 'Latacunga', 'Riobamba', 'Ibarra', 'Guayaquil', 'Quito']:
        all_theaters = list(get_movies(city))
        body, movies_html, num_movies_playing = make_email_body(all_theaters)
        if num_movies_playing:
            plural = "Movies" if num_movies_playing > 1 else "Movie"
            msgs = make_final_email_objects(num_movies_playing, plural, body, city=city)
            with smtplib.SMTP('smtp.gmail.com', port=587) as server:
                init_email(server)
                for msg in msgs:
                    server.send_message(msg)
            print("-"*10, "\n",
                  "{} email built successfully today: {}\n".format(city, datetime.today().strftime('%Y-%m-%d')),
                  "\n", body, "\n",
                  "-"*10, "\n")
            make_html_file(num_movies_playing, plural, movies_html, city)
        else:
            print('No email sent today in {}: {}\n'.format(city, datetime.today().strftime('%Y-%m-%d')))
            relative_path = os.path.join("Machala_Movie_Mailer",
                                         "flask_movie_mailer",
                                         "static",
                                         "today_message_{}.txt".format(city))
            with open(os.path.abspath(relative_path), "w") as file:
                file.write("<h5><cite>No English movies today, but you'll get an email when there are!</cite></h5>")
