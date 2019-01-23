from email.message import EmailMessage


def make_message(film, times, ratings):
    showtimes = "\n".join(["{}: {}".format(time['Language'], time['Times']) for time in times])
    msg = "Title: {}\nDirector: {}\nRotten Tomato Score: {}\nTrailer: {}\n".format(film['title'],
                                                                                   film['director'],
                                                                                   ratings['rt'],
                                                                                   film['trailer'])
    msg_part_2 = "\nShow-times \n{}".format(showtimes)
    return msg+msg_part_2


def create_email_message(from_, to_, subject, body):
    msg = EmailMessage()
    msg['From'] = from_
    msg['To'] = to_
    msg['Subject'] = subject
    msg.set_content(body)
    return msg
