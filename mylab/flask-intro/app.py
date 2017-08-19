from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from functools import wraps

app = Flask(__name__)

#app.secret_key = "my key"
#app.database = "posts.db"
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'

### load config
import os
### please export APP_SETTINGS="config.DevelopmentConfig"
app.config.from_object(os.environ['APP_SETTINGS'])
#print os.environ['APP_SETTINGS']

### Create the sqlalchemy object
db = SQLAlchemy(app)
from models import *

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for("login"))
    return wrap

@app.route("/")
@login_required
def home():
    try:
        posts=[]
        posts = db.session.query(BlogPost).all()
    except exc.SQLAlchemyError:
        flash("You have no database")
    return render_template("index.html", posts=posts)

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "admin":
            session["logged_in"] = True
            flash("You were logged in")
            return redirect(url_for("home"))
        else:
            error = "Invalid Credentials. Please try again"
    return render_template("login.html", error=error)

@app.route("/logout")
@login_required
def logout():
    session.pop("logged_in", None)
    flash("You were logged out")
    return redirect(url_for("welcome"))

if __name__ == "__main__":
    app.run(host='0.0.0.0')
