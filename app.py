import os

from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

#use URL and Key from the goodreads API
import requests
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "eKfkTI8uqlTrrogBz0qZw", "isbns": "9781632168146"})
print(res.json())


app = Flask(__name__)

# Check for environment variable (make sure to run => set FLASK_APP=app.py   )
if not os.getenv("postgres://wduatycfqnbmba:dbff1731be4824538b1f4d95fbd91f2f7b5bbc581bef419c62c5ee60e59b0339@ec2-34-192-30-15.compute-1.amazonaws.com:5432/dedpqat6p8mc6q"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("postgres://wduatycfqnbmba:dbff1731be4824538b1f4d95fbd91f2f7b5bbc581bef419c62c5ee60e59b0339@ec2-34-192-30-15.compute-1.amazonaws.com:5432/dedpqat6p8mc6q"))
db = scoped_session(sessionmaker(bind=engine))



@app.route("/")
def index():
    return "Project 1: TODO"

#Set up the Debug mode and the Env Variable
app.run(debug=True)

#In order to run the code ==> python -m flask run