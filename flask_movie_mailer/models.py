from flask_movie_mailer import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    location = db.Column(db.String(40), unique=False, nullable=False)
    frequency = db.Column(db.String(40), unique=False, nullable=False)

    def __repr__(self):
        return "User('{}', '{}', '{}', '{}')".format(self.name, self.email, self.location, self.frequency)