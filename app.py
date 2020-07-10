import os

from flask import Flask, url_for, redirect, request, session, render_template, make_response
from flask_session import Session
from services import get_friends_list, get_profile, get_user_id
from models import VkSignIn


app = Flask(__name__)
sess = Session()
app.config['SECRET_KEY'] = os.urandom(20)


@app.route('/')
def index():
    if 'access_token' not in session:
        return redirect(url_for("auth"))
    access_token = session['access_token']
    user_id = get_user_id(access_token)
    me = get_profile(user_id, access_token)
    friends_list_id = get_friends_list(user_id, access_token)
    friends = []
    for friend_id in friends_list_id:
        friends.append(get_profile(friend_id, access_token))
    return render_template('index.html', me=me, friends=friends)


@app.route('/auth')
def auth():
    if 'access_token' in session:
        return redirect(url_for("index"))
    return render_template('authorize.html')


@app.route('/authorize')
def oauth_authorize():
    if 'access_token' in session:
        return redirect(url_for("index"))
    oauth = VkSignIn()
    return oauth.authorize()


@app.route('/callback')
def oauth_callback():
    if 'access_token' in session:
        return redirect(url_for("index"))
    oauth = VkSignIn()
    access_token = oauth.callback()
    session['access_token'] = access_token
    return redirect(url_for("save_session"))


@app.route('/logout')
def logout():
    session.pop('access_token')
    return redirect(url_for('auth'))


@app.route('/save-session')
def save_session():
    if request.cookies.get('session'):
        resp = make_response(redirect(url_for('index')))
        resp.set_cookie('session', request.cookies.get('session'), max_age=60*60*24*365*2)
        return resp
    return redirect(url_for('auth'))


if __name__ == "__main__":
    sess.init_app(app)
    app.run()
