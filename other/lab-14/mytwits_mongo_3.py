from flask import Flask, request
from flask import render_template
from flask import redirect, url_for
import pymongo
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms import validators
from vs_url_for import vs_url_for

class addTwitForm(FlaskForm):
    twit = StringField('twit', validators = [validators.DataRequired()])
    submit = SubmitField('submit', [validators.DataRequired()])

class DBHelper:

    def __init__(self):
        client = pymongo.MongoClient()
        self.db = client['mytwits']

    def get_all_twits(self):
        return self.db.twits.find().sort('created_at',pymongo.DESCENDING)

    def add_twit(self,twit):
        return self.db.twits.insert({'twit':twit,'username':'dan1','created_at': datetime.datetime.utcnow()})

app = Flask(__name__)
db = DBHelper()
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/')
def index():
    twits = db.get_all_twits()
    return render_template("mytwits_mongo_3.html", twits=twits)

@app.route('/add_twit', methods = ['GET', 'POST'])
def add_twit():
    form = addTwitForm()
    if form.validate_on_submit():
        twit = form.twit.data
        db.add_twit(twit)
        return redirect(vs_url_for('index'))
    return render_template('add_twit_mongo_3.html',form=form)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8000)
