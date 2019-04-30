from email.message import EmailMessage


def create_email_text(film, english_times, ratings, theater):
    """
    Create the body of the email
    :param film: dict that contains title, director, trailer
    :param times: dict that contains language and times
    :param ratings: dict that contains rt and imdb ratings
    :param theater: string with theater name
    :return: string that contians body of the email
    """
    html_bar = '<hr size="1" width="100" align="left"> '
    showtimes = "<br/>".join(["{}: {}".format(time['Language'], time['Times']) for time in english_times])
    msg = '<p>Title: <b>{}</b><br/>Director: {}<br/>IMDB Score: {}/10<br/>Trailer: {}</p> {}'.format(film['title'],
                                                                                                     film['director'],
                                                                                                     ratings['imdb'],
                                                                                                     film['trailer'],
                                                                                                     html_bar)
    msg_part_2 = "<p>Show-times @ {} <br/>{}</p>".format(theater, showtimes)
    return msg+msg_part_2


def create_email_object(from_, to_, subject, body):
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
    msg.set_content(body, subtype='html')
    return msg
