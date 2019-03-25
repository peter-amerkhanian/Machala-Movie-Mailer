import smtplib
from datetime import datetime
from machala_movie_mailer import \
    movies, make_email_body, check_for_plural, make_final_email_objects, init_email, make_html_file


if __name__ == "__main__":
    body, movies_html, num_movies_playing = make_email_body(movies)
    if num_movies_playing:
        plural = check_for_plural(num_movies_playing)
        msgs = make_final_email_objects(num_movies_playing, plural, body, city='Machala')
        # with smtplib.SMTP('smtp.gmail.com', port=587) as server:
        #     init_email(server)
        #     for msg in msgs:
        #         server.send_message(msg)
        print("-"*10, "\n",
              "Email sent successfully today: {}\n".format(datetime.today().strftime('%Y-%m-%d')),
              "\n", body, "\n",
              "-"*10, "\n")
        make_html_file(num_movies_playing, plural, movies_html)
    else:
        print('No email sent today: {}\n'.format(datetime.today().strftime('%Y-%m-%d')))