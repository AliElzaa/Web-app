from flask import Flask, reques:wt
from flask import render_template
from flask import redirect, url_for
import pymysql
from vs_url_for import vs_url_for

class DBHelper:

    def __init__(self):
        self.db = pymysql.connect(host='localhost',
            user='mytwits_user',
            passwd='mytwits_password',
            db='mytwits')

    def get_all_twits(self):
        query = "select u.username, t.twit, t.created_at from twits t, users u where t.user_id=u.user_id order by t.created_at desc;"
        with self.db.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall() # The method fetches all (or all remaining) rows of a query result set and returns a list of tuples

    def add_twit(self,twit):
        query = "insert into twits (twit,user_id) values \
        ('{}','{}');".format(twit,1)
        print(query)
        with self.db.cursor() as cursor:
            cursor.execute(query)
            return self.db.commit()

app = Flask(__name__)
db = DBHelper()

@app.route('/')
def index():
    twits = db.get_all_twits()
    return render_template("mytwits_mysql_2.html", twits=twits)

@app.route('/add_twit', methods = ['GET', 'POST'])
def add_twit():
    if request.form.get('twit'):
        
        db.add_twit(request.form['twit'])
        return redirect(vs_url_for('index'))
       
    return render_template('add_twit_mysql_2.html')


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8000)
