from flask import Flask, request
from flask import render_template
from flask import redirect, url_for
from flask import session,flash,abort
from vs_url_for import vs_url_for
from forms import addTwitForm, editTwitForm, loginForm
from helper import DBHelper
from flask_login import LoginManager, login_required
from flask_login import login_user, logout_user
from user import User
from flask import jsonify
from flask_restful import Resource, Api
from flask_restful import fields, marshal_with
from flask_restful import reqparse

login_manager = LoginManager()

app = Flask(__name__)
db = DBHelper()
login_manager.init_app(app)
api = Api(app)

app.secret_key = 'G90DAjg0/gdajoi!Kjmg9i,!2k0'

resource_fields = {
    'twit_id': fields.Integer,
    'twit': fields.String,
    'user_id': fields.Integer,
    'created_at': fields.DateTime(dt_format='rfc822')
}



parser = reqparse.RequestParser()
parser.add_argument('twit', type=str, help='the text of the twit; must be a string')
parser.add_argument('twit_id', type=int, help='the id of the twit; must be an integer')
parser.add_argument('user_id', type=int, help='the id of the twit; must be an integer')

class TwitsApi(Resource):
    @marshal_with(resource_fields)
    def get(self):
        return db.get_all_twits()

    @marshal_with(resource_fields)
    def post(self):
        args = parser.parse_args()
        twit = args['twit']
        user_id = args['user_id']
        db.add_twit(twit,user_id)
        return db.get_all_twits()


class TwitsIdApi(Resource):

    @marshal_with(resource_fields)
    def get(self, twit_id):
        if  db.get_twit(twit_id):
            return db.get_twit(twit_id)
        abort(404)

    @marshal_with(resource_fields)
    def put(self,twit_id):
        args = parser.parse_args()
        twit = args['twit']
        db.update_twit(twit,twit_id)
        return  db.get_all_twits()

    @marshal_with(resource_fields)
    def delete(self, twit_id):
        db.delete_twit(twit_id)
        return  db.get_all_twits()

api.add_resource(TwitsApi, '/api')
api.add_resource(TwitsIdApi, '/api/<int:twit_id>')



@app.route('/api/<username>')
def api(username=None):
    if username:
        twits = db.get_user_twits(username)
        return jsonify({'twits':twits})
    else:
         twits = db.get_all_twits()
         return jsonify({'twits':twits})


@login_manager.user_loader
def load_user(user_id):
    result = db.get_user(user_id)
    if result:
        return User(user_id)

@app.route('/')
def index():
    twits = db.get_all_twits()
    return render_template("mytwits.html", twits=twits)

@app.route('/add_twit', methods = ['GET', 'POST'])
def add_twit():
      form = addTwitForm()
      if form.validate_on_submit():
        twit = form.twit.data
        db.add_twit(twit,session['user_id'])
        return redirect(vs_url_for('index'))
      return render_template('add_twits.html',form=form)



@app.route('/edit_twit', methods = ['GET', 'POST'])
@login_required
def edit_twit():
    form = editTwitForm()
    if request.args.get('id'):
        twit_id = request.args.get('id')
        twit = db.get_twit(twit_id)
        print(str(twit_id) + " " + str(twit))
        form.twit.data = twit[0]
        form.twit_id.data = twit_id
        return render_template('edits_twits.html',form=form,twit=twit)
    if form.validate_on_submit():
        twit = form.twit.data
        twit_id = form.twit_id.data
        db.update_twit(twit,twit_id)
        return redirect(vs_url_for('index'))
    return render_template('edits_twits.html',form=form)

 

@app.route('/delete_twit', methods = ['GET','POST'])
@login_required
def delete_twit():
    if request.args.get('id'):
        twit_id = request.args.get('id')
        twit = db.delete_twit(twit_id)
    return redirect(vs_url_for('index'))

@app.route('/login', methods = ['GET','POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        password = form.password.data
        username = form.username.data
        user_id = db.check_password(username,password)
        if user_id:
            user = User(user_id)
            login_user(user)
            flash('login successful!')
            return redirect(vs_url_for('index'))
        else:
            flash('login unsuccessful!')
    return render_template('login.html',form=form)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    logout_user()
    return redirect(vs_url_for('index'))



 
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8000)
