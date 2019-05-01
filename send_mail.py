import smtplib
from datetime import datetime
from machala_movie_mailer import \
    get_movies, make_email_body, check_for_plural_movie_count, make_final_email_objects, init_email, make_html_file


if __name__ == "__main__":
    for city in ['Machala', 'Cuenca', 'Ibarra', 'Guayaquil']:
        all_theaters = list(get_movies(city))
        body, movies_html, num_movies_playing = make_email_body(all_theaters)
        if num_movies_playing:
            plural = check_for_plural_movie_count(num_movies_playing)
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
            with open(r"flask_movie_mailer/static/today_message_{}.txt".format(city), "w") as file:
                file.write("<h5><cite>No English movies today, but you'll get an email when there are!</cite></h5>")
