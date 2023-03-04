import os
from flask import Flask, session, flash, get_flashed_messages, render_template, request, abort, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')


db = SQLAlchemy(app)


# Models


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    bio = db.Column(db.String(300))
    insights = db.relationship("Insight", backref="author")


class Insight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))


# Routes


@app.route("/")
def index():
    auth_user = User.query.get(session.get('user_id'))

    # Go straight to feed if logged in
    if auth_user:
        all_insights = Insight.query.order_by(Insight.date.desc()).all()
        return render_template("feed.html", auth_user=auth_user, insights=all_insights)
    
    # Otherwise show login
    messages = get_flashed_messages()
    return render_template("login.html", auth_user=auth_user, messages=messages)


@app.route("/profile")
@app.route("/profile/<string:username>")
def profile(username=None):
    auth_user = User.query.get(session.get('user_id'))
    # Give a 401 unauthorized error if not signed in
    if not auth_user:
        abort(401)

    # Attempt to access specific profile if username provided (otherwise it'll go to the logged in user's profile)
    view_user = auth_user
    if username:
        view_user = User.query.filter_by(username=username).first() # User whose profile you're attempting to view
        # Give a 404 not found error if they try to access an unknown username
        if not view_user:
            abort(404)
    
    return render_template("profile.html", auth_user=auth_user, view_user=view_user)


@app.route("/post")
def post():
    auth_user = User.query.get(session.get('user_id'))
    # Give a 401 unauthorized error if not signed in
    if not auth_user:
        abort(401)
    
    return render_template("post.html", auth_user=auth_user)


# Backend-only POST API Endpoints


@app.route("/api/login", methods=['POST'])
def api_login():
    username = request.form['username']
    password = request.form['password']

    matching_user = User.query.filter_by(username=username, password=password).first()

    if matching_user:
        session['user_id'] = matching_user.id
    else:
        flash('Invalid username or password. Try again.', 'error')
    return redirect(url_for('index'))
    

@app.route("/api/logout")
def api_logout():
    session['user_id'] = None # Nullify user's session id
    return redirect(url_for('index'))


@app.route("/api/post", methods=['POST'])
def api_post():
    auth_user = User.query.get(session.get('user_id'))
    # Give a 401 unauthorized error if not signed in
    if not auth_user:
        abort(401)
    
    title = request.form["insight-title"]
    body = request.form["insight-body"]
    author = auth_user

    if title and body and author:
        insight = Insight(title=title, body=body, author_id=author.id)
        db.session.add(insight)
        db.session.commit()
    # Go back to home screen
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
