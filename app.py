import os
from flask import Flask, session, flash, render_template, request, abort, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')


db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    insights = db.relationship("Insight", backref="author")


class Insight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))


HARD_CODED_CURR_USER = User.query.get(2)  # guest

# Login Page
@app.route("/")
def index():
    return render_template("index.html")


# Login Function
@app.route("/login", methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username, password=password).first()
    print(user.username)
    if user:
        session['user_id'] = user.id  # store user's ID in the session
        return redirect(url_for('feed'))
    else:
        flash('Invalid username or password', 'error')


@app.route("/feed")
def feed():
    all_insights = Insight.query.order_by(Insight.date.desc()).all()
    return render_template("feed.html", insights=all_insights)


@app.route("/author")
@app.route("/author/<string:username>")
def profile(username=None):
    # if no username specified, take them to logged in route
    if username is None:
        return redirect(url_for("profile", username=HARD_CODED_CURR_USER.username))
    else:
        user = User.query.filter_by(username=username).first()
        if user is None:
            abort(404)
        return render_template("profile.html", user=user)


# Create Page
@app.route("/create")
def create():
    return render_template("create.html")


# Share Function
@app.route("/share", methods=['POST'])
def share():
    title = request.form["insight-title"]
    body = request.form["insight-body"]
    author = HARD_CODED_CURR_USER
    if title and body and author:
        insight = Insight(title=title, body=body, author_id=author.id)
        db.session.add(insight)
        db.session.commit()
    # Go back to home screen
    return redirect(url_for("feed"))


if __name__ == "__main__":
    app.run(debug=True)
