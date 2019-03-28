import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
import_file = "books.csv"

def main():
    f = open(import_file)
    reader = csv.reader(f)
    next(reader)
    for isbn, title, author, year in reader:
        # print(isbn, title, author, year)
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                    {"isbn": isbn, "title": title, "author": author, "year": year})
        print("Added book", isbn, title)
    db.commit()

if __name__ == "__main__":
    main()
