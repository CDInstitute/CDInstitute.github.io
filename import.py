from flask import request

# import requests
# res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "eKfkTI8uqlTrrogBz0qZw", "isbns": "9781632168146"})
# print(res.json())

#install psql 
# psql DATABASE_URL

import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                    {"isbn": isbn, "title": title, "author": author, "year": year})
        print(f"Added book with this {title} from this {author} in this {year}.")
    db.commit()

if __name__ == "__main__":
    main()
