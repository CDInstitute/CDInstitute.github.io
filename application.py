import os
import csv

# make sure to set DATABASE_URL=.... and set FLASK_DEBUG=1 and set FLASK_APP=name.py  FLASK_ENV=development on the CMD Terminal and not on Visual Studio Code
# CTRL+K+C note an entire code

from flask import render_template, request, Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
app.secret_key = "super secret key"

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
#Session(app) #this line create issues set up the key


# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template("index.html")
    # SELECT * FROM users WHERE ( username = username) AND (password = password)
    # SELECT * FROM users WHERE ( username = 'Alberto') AND (password = 'test')

@app.route("/hello", methods=["POST"])
def hello():
    name = request.form.get("name")
    return render_template("hello.html", name=name)

@app.route("/review", methods=["GET", "POST"])
def review():
    if session.get("reviews") is None:
        session["reviews"] = []
    if request.method == "POST":
        review = request.form.get("review")
        session["reviews"].append(review)
    return render_template("review.html", reviews=session["reviews"])

#select the list of all the books.
# def main():
#     books = db.execute("SELECT title, author, year FROM books").fetchall()
#     for book in books:
#         print(f"{book.title} by {book.author}, {book.year} year.")
# if __name__ == "__main__":
#      main()

@app.route("/search")
def search() :
    books = db.execute("SELECT * FROM books").fetchall()
    return render_template("search.html", books=books)

@app.route("/searchbook", methods=["POST"])
def searchbook():
    """Search a book."""

    # Get form information.
    name = request.form.get("name")
    try:
        book_isbn = int(request.form.get("book_isbn"))
    except ValueError:
        return render_template("error.html", message="Invalid book number.")

    # Make sure the flight exists. Complete the if statement with a positive end
    if db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": book_isbn}).rowcount == 0:
        return render_template("error.html", message="No such book with that id.")
    db.commit()
    return render_template("success.html")