from flask import Flask, render_template, request, abort, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Coding/flask/noend-insight/app.db"

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


@app.route("/")
def index():
    all_insights = Insight.query.all()
    return render_template("index.html", insights=all_insights)


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


@app.route("/hello")
def hello():
    name = request.args.get("name", "world")
    name = name.capitalize()
    return f"Hello, {name}!"


if __name__ == "__main__":
    app.run(debug=True)
