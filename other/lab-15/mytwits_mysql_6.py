from flask import Flask, request
from flask import render_template
from flask import redirect, url_for
import pymysql
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import HiddenField
from wtforms import SubmitField
from wtforms import validators
from vs_url_for import vs_url_for

class addTwitForm(FlaskForm):
    twit = StringField('twit', validators = [validators.DataRequired()])
    submit = SubmitField('submit', [validators.DataRequired()])

class editTwitForm(FlaskForm):
    twit = StringField('twit', validators = [validators.DataRequired()])
    twit_id = HiddenField('twit_id')
    submit = SubmitField('submit', [validators.DataRequired()])

class DBHelper:

    def __init__(self):
        self.db = pymysql.connect(host='localhost',
            user='root',
            passwd='lol1649',
            db='mytwits')

    def get_all_twits(self):
        query = "select u.username, t.twit_id, t.twit, t.created_at from twits t, users u where t.user_id=u.user_id order by t.created_at desc;"
        with self.db.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall() # The method fetches all (or all remaining) rows of a query result set and returns a list of tuples

    def get_twit(self,twit_id):
        query = "select twit from twits where twit_id=%s"
        with self.db.cursor() as cursor:
            cursor.execute(query, twit_id)
            return cursor.fetchone()  
            # more detals about cursor.fetchone at
            # https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-fetchone.html

    def add_twit(self,twit):
        query = "insert into twits (twit,user_id) values \
        (%s,%s);"
        with self.db.cursor() as cursor:
            cursor.execute(query, (twit,1))
            return self.db.commit()

    def update_twit(self,twit,twit_id):
        query = "update twits set twit=%s where twit_id=%s"
        with self.db.cursor() as cursor:
            cursor.execute(query,(twit,twit_id))
            return self.db.commit()

    def delete_twit(self,twit_id):
        query = "delete from twits where twit_id=%s"
        with self.db.cursor() as cursor:
            cursor.execute(query, twit_id)
            return self.db.commit()

app = Flask(__name__)
db = DBHelper()
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/')
def index():
    twits = db.get_all_twits()
    return render_template("mytwits_mysql_6.html", twits=twits)

@app.route('/add_twit', methods = ['GET', 'POST'])
def add_twit():
    form = addTwitForm()
    if form.validate_on_submit():
        twit = form.twit.data
        db.add_twit(twit)
        return redirect(vs_url_for('index'))
    return render_template('add_twit_mysql_6.html',form=form)

@app.route('/edit_twit', methods = ['GET', 'POST'])
def edit_twit():
    form = editTwitForm()
    if request.args.get('id'):
        twit_id = request.args.get('id')
        twit = db.get_twit(twit_id)
        form.twit.data = twit[0]
        form.twit_id.data = twit_id
        return render_template('edit_twit_mysql_6.html',form=form,twit=twit)
    if form.validate_on_submit():
        twit = form.twit.data
        twit_id = form.twit_id.data
        db.update_twit(twit,twit_id)
        return redirect(vs_url_for('index'))
    return render_template('edit_twit_mysql_6.html',form=form)

@app.route('/delete_twit', methods = ['GET', 'POST'])
def delete_twit():
    if request.args.get('id'):
        twit_id = request.args.get('id')
        twit = db.delete_twit(twit_id)
    return redirect(vs_url_for('index'))
   
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8000)
