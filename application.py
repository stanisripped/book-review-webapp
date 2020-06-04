import csv
import os

from flask import Flask, session, render_template
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


# login
username = []
password = []

@app.route("/", methods=["GET", "POST"])
def login():
    if session.get("username") is None:
        session["username"] = []
    if request.method == "POST":
        headline = "Hello, world!"
        return render_template("index.html", headline=headline)

@app.route("/<string:name>")
def hell(name):
    return f"<h1>Hello, {name}!</h1>"

@app.route("/bye")
def bye():
    headline = "Goodbye!"
    return render_template("index.html", headline=headline)

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                {"isbn": isbn, "title": title, "author": author, "year": year})
        print(f"Added {title} by {author} written in {year} with isbn: {isbn}")
    db.commit()
if __name__ == "main":
    main()
