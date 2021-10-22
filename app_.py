from datetime import datetime

from flask import Flask,blueprints,render_template,request,make_response,redirect,escape,url_for,session,abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'aaaaaaaaa'
app.config['DEBUG'] = True
app.config["SESSION_COOKIE_SECURE"]= False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db?check_same_thread=False'

db = SQLAlchemy(app)


class User(db.Model):
    __table_name__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    profile_image = db.Column(db.String(100), default='default.png')

    posts = db.relationship('Post', backref='author', lazy=True)


    def __init__(self, username, email, password, **kwargs):
        self.username = username
        self.email = email

        self.set_password(password)


    def __repr__(self):
        return f"<User('{self.id}', '{self.username}', '{self.email}')>"


def set_password(self, password):
    self.password = generate_password_hash(password)


def check_password(self, password):
    return check_password_hash(self.password, password)


class Post(db.Model):
    __table_name__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"<Post('{self.id}', '{self.title}')>"

@app.route('/index')
def index():
    post = Post.query.all()

    return render_template('board.html',posts = post)

@app.route('/')
def main():
    if 'userID' in session:
        userid = session['userID']
        return f'Logged in as {userid}<br><b><a href="/logout">click here to log out</a><b><br>' \
               f'Click To check Cookie<br><a href="/getcookie">here</a><b>'

    return  f'You are not logged in <br><a href="/login">click here to log in</b></a>'

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method=='POST':
        if request.form['username'] == 'admin':
            return redirect(url_for('success'))
        else:
            abort(401)
    else:
        return redirect(url_for('index'))
    return '''
        <form action="" method = "post">
            <p><input type = text name = name></input></p>
            <p><input type = submit value = Login></input></p>
        </form>
    '''

@app.route('/success')
def success():
    return 'logged in successfully'

@app.route('/logout')
def logout():
    session.pop('userID',None)
    return redirect(url_for('main'))

@app.route('/setcookie',methods = ['GET','POST'])
def setcookie():
    if request.method == 'POST':
        user = request.form['name']
        res = make_response('Create Cookie~!')
        res.set_cookie('userID',user)
        return res
    return redirect('/index')

@app.route('/getcookie')
def getcookie():
    name = request.cookies.get('userID')
    return name

if __name__ == '__main__':

    app.run('0.0.0.0',debug=True)