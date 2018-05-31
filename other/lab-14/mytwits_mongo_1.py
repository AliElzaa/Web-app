from flask import Flask, request
from flask import render_template
from flask import redirect, url_for
import pymongo

class DBHelper:

    def __init__(self):
        client = pymongo.MongoClient()
        self.db = client['mytwits']

    def get_all_twits(self):
        return self.db.twits.find().sort('created_at',pymongo.ASCENDING)

app = Flask(__name__)
db = DBHelper()

@app.route('/')
def index():
    twits = db.get_all_twits()
    return render_template("mytwits_mongo_1.html", twits=twits)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8000)
