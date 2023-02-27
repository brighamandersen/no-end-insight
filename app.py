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
    user = session['user_id'] # Get user's id from the session
    # Go straight to feed if logged in
    if user:
        return render_template("feed.html")
    # Otherwise show login
    messages = get_flashed_messages()
    return render_template("index.html", messages=messages)

@app.route("/logout")
def logout():
    session['user_id'] = None # Nullify user's session id
    return redirect(url_for('index'))


@app.route("/feed")
def feed():
    all_insights = Insight.query.order_by(Insight.date.desc()).all()
    return render_template("feed.html", insights=all_insights)


@app.route("/profile")
@app.route("/profile/<string:username>")
def profile(username=None):
    # If no username provided, insert the username of who's currently logged in
    user = session['user_id'] # Get user's id from the session
    if username:
        user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template("profile.html", user=user)


@app.route("/create")
def create():
    return render_template("create.html")


# Backend-only POST Endpoints


@app.route("/login", methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        print('succeeded', user.id)
        session['user_id'] = user.id  # Store user's id in the session
    else:
        print('failed')
        flash('Invalid username or password. Try again.', 'error')
    return redirect(url_for('index'))
    

@app.route("/share", methods=['POST'])
def share():
    title = request.form["insight-title"]
    body = request.form["insight-body"]
    if title and body and author:
        insight = Insight(title=title, body=body, author_id=author.id)
        db.session.add(insight)
        db.session.commit()
    # Go back to home screen
    return redirect(url_for("feed"))


if __name__ == "__main__":
    app.run(debug=True)
