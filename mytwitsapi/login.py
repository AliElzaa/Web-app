from flask import Flask, render_template
from flask import request, flash
import string

app = Flask(__name__)

USERNAME, PASSWORD = 'Ali', 'test'

@app.route("/", methods = ['GET','POST'])
def show_user():
    username, password ='',''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']


        if username == USERNAME and password == PASSWORD:
           flash('login successful!')
    list = [username, password]
    return render_template('mock_login.html', list=list)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8000)

