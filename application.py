import os
from flask import Flask,session,render_template,request,jsonify,redirect,url_for
#from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
app = Flask(__name__)

# Check for environment variable
#if not os.getenv("DATABASE_URL"):
    #raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

storedNotes=[]

# Set up database
engine = create_engine("postgres://gfbbhklmbigcpt:aef99b41334f0d7e5d1e89bc87d8be92a34dd679d67d148cb6eef48716742818@ec2-54-225-95-183.compute-1.amazonaws.com:5432/d5fttg3bfrqigh")
db = scoped_session(sessionmaker(bind=engine))

@app.route("/", methods=["GET","POST"])
def index():
    if 'username' in session:
        return render_template("index.html",heading=f"welcome mr {session['username']} to book rating website")
    data=jsonify({"success":"false","error":{"code":101,"type":"missing_access_key","info":"You have not supplied an API Access Key. [Required format: access_key=YOUR_ACCESS_KEY]"}})
    print(data)
    #books=db.execute("SELECT * from books_details LIMIT 20").fetchall()
    #return render_template("index.html",books=books)
    return render_template("index.html",heading="you need to login or sign up first")


@app.route("/signup",methods=["GET","POST"])
def signup():
    username = request.form.get("username")
    password = request.form.get("password")
    #jsonify({"username":username,"password":password})
    if len(username)<8 or len(password)<8:
        return render_template("index.html",heading="length of username or password is less than 8")
    try:
        db.execute("INSERT INTO users_information(username,password) values('{}','{}')".format(username,password))
        db.commit()
    except Exception as exp:
        return render_template("index.html",heading=type(exp))
    #db.commit()
    userdetails=db.execute("SELECT * FROM users_information where username='{}'".format(username)).fetchall()
    return render_template("index.html",user=userdetails,heading="successful")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == 'POST':
        details_of_user=db.execute("SELECT * FROM users_information WHERE username=:username and password=:password",{"username":request.form['username'],"password":request.form['password']}).fetchall()
        if(details_of_user):
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        else:
            return render_template("index.html",heading="incorrect username or password")

@app.route("/logout",methods=["GET","POST"])
def logout():
    session.pop('username',None)
    return redirect(url_for('index'))

@app.route("/search",methods=["GET","POST"])
def search():
    keyword=request.form.get("keyword")
    if(keyword is not None):
        result=db.execute("SELECT * FROM books_details where title LIKE '%{}%'".format(keyword)).fetchall()
        return render_template("search.html",keyword=keyword,books=result,count=len(result))
    else:
        return render_template("search.html",keyword=keyword)

@app.route("/notes",methods=["GET"])
def notes():
    if request.method=="GET":
        note=request.form.get("note")
        storedNotes.append(note)
    return render_template("notes.html",notes=storedNotes)


app.run(debug=True)
