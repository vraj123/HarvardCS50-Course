import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")   


@app.route("/login", methods=['GET', 'POST'])
def login():
    return "Project 1: TODO"

@app.route("/register", methods=['GET', 'POST'])
def register():
    message = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        db.execute("SELECT username AND password FROM users WHERE username = :username AND password = :password")
        if(db.fetchall() == []):
            db.execute("INSERT INTO users (username, password) VALUES (:username, :password)", {"username": username, "password": password})
            db.commit()
        else:
            message = "Sorry this username has been taken"

    return render_template("register.html", message=message)
    