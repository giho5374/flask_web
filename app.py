from flask import Flask,session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db?check_same_thread=False'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = '12345'
db = SQLAlchemy(app)
db.create_all()

@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)

if __name__ == '__main__':
    from fun import app_fun
    app.register_blueprint(app_fun)
    app.run(debug=True)
