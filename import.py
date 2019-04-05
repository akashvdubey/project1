from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import csv
#engine = create_engine("mysql://root:~sin|akash@localhost:3306/hive")

engine = create_engine("postgres://gfbbhklmbigcpt:aef99b41334f0d7e5d1e89bc87d8be92a34dd679d67d148cb6eef48716742818@ec2-54-225-95-183.compute-1.amazonaws.com:5432/d5fttg3bfrqigh")
db = scoped_session(sessionmaker(bind=engine))

file = open("books.csv")
reader = csv.reader(file)
for a,b,c,d in reader:
    db.execute("INSERT INTO books_details(isbn,title,author,year) values(:isbn,:title,:author,:year)",{"isbn":a+"book","title":b,"author":c,"year":d})
    print(f"book with isbn = {a} named {b} added succesfully")
print("added successfully")
