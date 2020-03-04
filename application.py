import os
import csv

# make sure to set DATABASE_URL=.... and set FLASK_DEBUG=1 and set FLASK_APP=name.py  FLASK_ENV=development on the CMD Terminal and not on Visual Studio Code
# CTRL+K+C note an entire code

from flask import render_template, request, Flask, session, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *

app = Flask(__name__)
app.secret_key = "super secret key"

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
#Session(app) #this line create issues set up the key

###########SQL Alchemy ##############################
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


####################################################
################# DEFINING THE ROUTES ##############
####################################################

@app.route("/")
def index():
    # login = db.execute("SELECT username, password FROM users").fetchone()
    # if login is None:
    #    return render_template("error.html", message="login or password doesn't match")
    return render_template("index.html")
    # SELECT * FROM users WHERE ( username = username) AND (password = password)
    # SELECT * FROM users WHERE ( username = 'Alberto') AND (password = 'test')


##################################  REGISTER ########################################

@app.route("/registration")
def registration():
    # register = db.execute("INSERT INTO users (username, password) VALUES (:username, :password) ")
    return render_template("registration.html")
#INSERT INTO THE DATABASE username and password
# @app.route("/registration", method= ['POST'])
# def registration():
#     if 'username' in session:
#         return redirect("/")
#     username = request.form.get("username")
#     password = request.form.get("password")
#     if db.execute("SELECT * FROM users WHERE username = :username AND password = :password, {"username": username, "password": password}")
#         return render_template("index.html", message = "User Already Exist", failed= True, success=False, ready=True)
#     db.execute("INSERT INTO users (username, password) VALUES (:username, :password)", {"username": username, "password": password})
#     db.commit()
#     return render_template("index.html", message = "Account Created, Please log-in now", failed= False, success=True, ready=True)

@app.route("/hello", methods=["POST"])
def hello():
    name = request.form.get("name")
    return render_template("hello.html", name=name)
#SELECT FROM THE DATABASE users

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


######################  SEARCH ############################

@app.route("/search")
def search() :
    books = db.execute("SELECT * FROM books").fetchall()
    return render_template("search.html", books=books)

@app.route("/search/<int:book_isbn>")
def book(book_isbn):
    """Lists details about a single book."""
# Make sure book exists.
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": book_isbn}).fetchone()
    if book is None:
        return render_template("error.html", message="No such book.")
    return render_template("book.html", book=book)

# Get all reviews.
    reviews = db.execute("SELECT name FROM reviews WHERE book_isbn = :book_isbn",
                            {"book_isbn": book_isbn}).fetchall()
    return render_template("book.html", book=book, reviews=reviews)


# Get Success or Error while searching for the book

@app.route("/searchbook", methods=["POST"])
def searchbook():
    """Search a book."""

    # Get form information and set up Error Message
    name = request.form.get("name")
    try:
        book_isbn = int(request.form.get("book_isbn"))
    except ValueError:
        return render_template("error.html", message="Invalisbn book number.")

    # Make sure the book exists. Complete the if statement with a positive end
    if db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": book_isbn}).rowcount == 0:
        return render_template("error.html", message="No such book with that isbn.")
    # db.execute("SELECT * FROM books (name, book_isbn) VALUES (:name, :book_isbn)",
    #         {"name": name, "book_isbn": book_isbn})
    db.commit()
    return render_template("success.html")


############ OLD CODE ###############################


# @app.route("/books")
# def books():
#     """Lists all books."""
#     books = db.execute("SELECT * FROM books").fetchall()
#     return render_template("books.html", books=books)

# @app.route("/books/<int:book_isbn>")
# def book(book_isbn):
#     """Lists details about a single book."""
# Make sure book exists.
    # book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": book_isbn}).fetchone()
    # if book is None:
    #     return render_template("error.html", message="No such book.")
    # return render_template("book.html", book=book)

# Get all reviews.
    # reviews = db.execute("SELECT name FROM reviews WHERE book_isbn = :book_isbn", {"book_isbn": book_isbn}).fetchall()
    # return render_template("book.html", book=book, reviews=reviews)

#####################################################
####################           ######################
###########             API               ###########
####################           ######################
#####################################################


@app.route("/api/books/<int:book_isbn>")
def book_api(book_isbn):
    """Return details about a single book."""

    # Make sure book exists.
    book = Book.query.get(book_isbn)
    if books is None:
        return jsonify({"error": "Invalid book_isbn"}), 422

    # Get all reviews.
    reviews = book.reviews
    comments = []
    for review in reviews:
        comments.append(review.comment)
    return jsonify({
            "title": book.title,
            "author": book.author,
            "year": book.duration,
            "isbn": book.isbn,
            "review_count": review.count,  #establish and create these parameters
            "average_score": review.score  #establish and create these parameters
        })

