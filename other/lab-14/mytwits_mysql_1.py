from flask import Flask, request
from flask import render_template
from flask import redirect, url_for
import pymysql

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

app = Flask(__name__)
db = DBHelper()

@app.route('/')
def index():
    twits = db.get_all_twits()
    return render_template("mytwits_mysql_1.html", twits=twits)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8000)
