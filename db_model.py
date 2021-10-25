from datetime import datetime
from main import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __table_name__ = 'user'

    user_id = db.Column(db.String(30),primary_key = True, unique = True)
    user_name = db.Column(db.String(30),nullable=False)
    user_email = db.Column(db.String(120),nullable=False)
    user_pw = db.Column(db.String(100),nullable=False)
    created = db.Column(db.DateTime)
    post = db.relationship('Post',backref = 'author')

    def __init__(self,user_id,user_name,user_email,user_pw,**kwargs):
        self.user_email =user_email
        self.user_name = user_name
        self.user_id = user_id
        self.set_password(user_pw)
        self.created = datetime.now()

    def set_password(self, user_pw):
        self.user_pw = generate_password_hash(user_pw)

    def check_password(self,hash_pw,input_pw):
        return check_password_hash(hash_pw,input_pw)

class Post(db.Model):
    __table_name__ = 'post'
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.user_id'))
    title = db.Column(db.String(500), nullable = False)
    content = db.Column(db.Text ,nullable = False)
    create_time = db.Column(db.DateTime)
