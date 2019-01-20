from email.headerregistry import Address
from email.message import EmailMessage
# All information from this module is private:
import private_variables


from_address = (
    Address(display_name=private_variables.from_address['User'],
            username=private_variables.from_address['Email'],
            domain=private_variables.from_address['Domain'])
)

to_address = (
    Address(display_name=private_variables.to_address['User'],
            username=private_variables.to_address['Email'],
            domain=private_variables.to_address['Domain'])
)


def make_message(film, times, ratings):
    showtimes = "\n".join(["{}: {}".format(time['Language'], time['Times']) for time in times])
    msg = f"""
Title: {film['title']}
Director: {film['director']}
Rotten Tomato Score: {ratings['rt']}
Trailer: {film['trailer']}
    """
    msg_part_2 = f"\nShow-times \n{showtimes}"
    return msg+msg_part_2


def create_email_message(from_, to_, subject, body):
    msg = EmailMessage()
    msg['From'] = from_
    msg['To'] = to_
    msg['Subject'] = subject
    msg.set_content(body)
    return msg
