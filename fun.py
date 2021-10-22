from flask import Blueprint, render_template, redirect, flash, session, request, url_for
from werkzeug.security import check_password_hash
from db_model import User, Post
from app import db
from datetime import datetime

app_fun = Blueprint('app_fun', __name__)


def login_check():
    return 'userid' not in session


def session_id_check():
    return User.query.filter(User.user_id == session['userid']).first()


@app_fun.route('/', methods=['GET', 'POST'])
def index():
    if not login_check():
        return redirect('main')
    return render_template('index.html')


@app_fun.route('/main')
def main():
    if login_check():
        flash('로그인이 필요한 서비스입니다.')
        return redirect('/')

    return render_template('main.html', userid=session_id_check().user_name)


@app_fun.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            pw = User.query.filter(User.user_id == request.form['id']).first().user_pw
        except:
            flash('ID가 등록되어있지 않습니다. 회원가입을 진행해주세요.')
            return render_template('login.html')
        if check_password_hash(pw, request.form['pwd']):
            session['userid'] = request.form['id']
            return redirect(url_for('main'))
        else:
            flash('로그인 정보가 다릅니다.')
            return render_template('login.html', id=request.form['id'])

    return render_template('login.html')


@app_fun.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if User.query.filter(User.user_id == request.form['id']).first():
            error = '사용중인 ID 입니다.'
            flash(error)
            return render_template('register.html', error=error, id=request.form['id'],
                                   name=request.form['name'], mailid=request.form['mailid'],
                                   email=request.form['email'])
        user = User(request.form['id'], request.form['name'], request.form['mailid'] + '@' + request.form['email'],
                    request.form['pwd'])
        db.session.add(user)
        db.session.commit()
        flash('회원가입이 완료되었습니다.')
        return redirect(url_for('index'))
    return render_template('register.html', objt={'data': User})


@app_fun.route('/post', methods=['GET', 'POST'])
def post():
    if login_check():
        flash('로그인이 필요한 서비스입니다.')
        return redirect('login')
    if request.method == 'POST':
        post = Post(title=request.form['title'], content=request.form['content'], author=session_id_check().user_id,
                    create_time=datetime.now())
        db.session.add(post)
        db.session.commit()
        return redirect('main')
    return render_template('post.html')


@app_fun.route('/board')
def board():
    return render_template('board.html', posts=Post.query.all())


@app_fun.route('/logout')
def logout():
    session.pop('userid')
    return redirect('/')
