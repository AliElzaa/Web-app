from flask_sqlalchemy import SQLAlchemy
import datetime

# we are using the second of flask-sqlalchemy's configuration options
# which is to create the sqlalchemy object here and bind it to the app once the
# app is initialised
# for more on this see http://flask-sqlalchemy.pocoo.org/2.3/api/#configuration
db = SQLAlchemy()

# the description of our data models follows those in the flask-sqlalchemy
# quickstart
# http://flask-sqlalchemy.pocoo.org/2.3/quickstart/
# for more detail see the doc section on declaring models
# http://flask-sqlalchemy.pocoo.org/2.3/models/
class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50))
    hashed = db.Column(db.String(150))
    salt = db.Column(db.String(150))
    twits = db.relationship('Twits',backref='user', lazy=True)

    # these are the user model attributes required by Flask-Login
    # see
    # https://flask-login.readthedocs.io/en/latest/#configuring-your-application
    def get_id(self):
        return self.user_id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

class Twits(db.Model):

   twit_id = db.Column(db.Integer, primary_key = True)
   twit = db.Column(db.String(140))
   user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
   created_at = db.Column(db.DateTime, default=datetime.datetime.now)

   def __repr__(self):
        return self.twit

