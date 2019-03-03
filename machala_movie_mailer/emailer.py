from email.message import EmailMessage


def make_message(film, times, ratings):
    """
    Create the body of the email
    :param film: dict that contains title, director, trailer
    :param times: dict that contains language and times
    :param ratings: dict that contains rt and imdb ratings
    :return: string that contians body of the email
    """
    showtimes = "\n".join(["{}: {}".format(time['Language'], time['Times']) for time in times])
    msg = "Title: {}\nDirector: {}\nRotten Tomato Score: {}\nTrailer: {}\n".format(film['title'],
                                                                                   film['director'],
                                                                                   ratings['rt'],
                                                                                   film['trailer'])
    msg_part_2 = "\nShow-times \n{}".format(showtimes)
    return msg+msg_part_2


def create_email_message(from_, to_, subject, body):
    """
    Create an email message object
    :param from_: Address object
    :param to_: Address object
    :param subject: string
    :param body: string
    :return: EmailMessage object containing a complete email
    """
    msg = EmailMessage()
    msg['From'] = from_
    msg['To'] = to_
    msg['Subject'] = subject
    msg.set_content(body)
    return msg
