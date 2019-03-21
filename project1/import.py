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
    print(reader)
    # for origin, destination, duration in reader:
    #     db.execute("INSERT INTO flights (origin, destination, duration) VALUES (:origin, :destination, :duration)",
    #                 {"origin": origin, "destination": destination, "duration": duration})
    #     print(f"Added flight from {origin} to {destination} lasting {duration} minutes.")
    # db.commit()

if __name__ == "__main__":
    main()
