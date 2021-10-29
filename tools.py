from flask import Blueprint, render_template, redirect, flash, session, request, url_for
from db_model import User,Post

def login_check():
    if 'userid' not in session:
        flash('로그인이 필요한 서비스입니다.')
        return redirect('/')
    else:
        return


def session_id_check():
    return User.query.filter(User.user_id == session['userid']).first()
