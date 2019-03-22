import os

from flask import Flask,session,render_template,request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
app = Flask(__name__)

# Check for environment variable
#if not os.getenv("DATABASE_URL"):
    #raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
storedNotes=[]

# Set up database
engine = create_engine("postgres://gfbbhklmbigcpt:aef99b41334f0d7e5d1e89bc87d8be92a34dd679d67d148cb6eef48716742818@ec2-54-225-95-183.compute-1.amazonaws.com:5432/d5fttg3bfrqigh")
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    books=db.execute("SELECT * from books_details LIMIT 20").fetchall()
    return render_template("index.html",books=books)

@app.route("/search",methods=["GET"])
def search():
    keyword=request.form.get("keyword")
    result=db.execute("SELECT * FROM books_details where title LIKE '%{}%'".format(keyword)).fetchall()
    return render_template("search.html",keyword=keyword,books=result,count=len(result))

@app.route("/notes",methods=["GET"])
def notes():
    if request.method=="GET":
        note=request.form.get("note")
        storedNotes.append(note)
    return render_template("notes.html",notes=storedNotes)


app.run(debug=True)
