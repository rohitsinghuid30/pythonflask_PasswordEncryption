from flask import Flask, render_template, flash, redirect, request, url_for
import os
from dotenv import load_dotenv
import pyodbc
from datetime import datetime

# load enviroment
load_dotenv()

app = Flask(__name__,template_folder="templates", static_folder="static")
# app.secret_key=os.getenv("SECRET_KEY")
app.secret_key=os.urandom(12)
SERVER=os.getenv("SERVER")
DB=os.getenv("DATABASE")
Driver=os.getenv("Driver")
Key=os.getenv("KEY")

# DB Connection
connection_string = f"DRIVER={Driver};SERVER={SERVER}; DATABASE={DB}; Trusted_Connection=True; MultipleActiveResultSets=True;"
db_conn = pyodbc.connect(connection_string)


# Function to mask 2-3 characters of password
def mask_password(password):
    #  if len(password) <= 3:
    #     # If password is very short, mask all characters
    #     return '*' * len(password)
    
    # Otherwise, mask the last 2-3 characters
    masked_password = password[:-4:2] + '*' * min(3, len(password))
    return masked_password


@app.route("/", methods=["GET", "POST"])
def welcome():
    return "Welcome to Pasword Encryption and Decryption Page."
# Plain text/Encrypted/Decrypted Password
@app.route("/users", methods=["GET"])
def home():
    # Plain text password
    ptp=[]
    cursor=db_conn.cursor()
    cursor.execute("SELECT username, password, created_At from test")
    rows=cursor.fetchall()
    for row in rows:
        username=row[0]
        password=row[1]
        created_At=row[2]
        ptp.append({"username":username, "password":mask_password(password), "created_At":created_At})
    
    # Encrypted Password
    EPS=[]
    cursor=db_conn.cursor()
    cursor.execute("SELECT username, encrypted_password, created_At from testlogin")
    rows=cursor.fetchall()
    for row in rows:
        user_name=row[0]
        enc_pass=row[1]
        added_date=row[2]
        EPS.append({"username":user_name,"encpass":enc_pass,"created_At":added_date})
    
    # Decrypted Password
    DCP=[]
    cursor=db_conn.cursor()
    cursor.execute(f"EXEC DecryptPass")
    rows=cursor.fetchall()
    for row in rows:
        id=row[0]
        username=row[1]
        dpass=row[2]
        current_date=datetime.now()
        DCP.append({"id":id,"username":username, "password":dpass, "current_date":current_date})
    return render_template("home.html", ptp=ptp, EPS=EPS,DCP=DCP)



# Add user
@app.route("/adduser", methods=["GET","POST"])
def Add_User():
    if request.method == "POST":
        username=request.form["username"]
        password=request.form["password"]
        cursor=db_conn.cursor()
        query = f"EXEC EncryptDecrytpPswd @username = {username}, @password = {password}"
        cursor.execute(query)
        cursor.commit()
        cursor.close()
        
        flash("User Added Successfully.")
    return redirect("/users")


# delete User
@app.route("/delete/<int:id>", methods=["GET", "POST"])
def delete_user(id):
    if request.method=="GET":
        cursor=db_conn.cursor()
        query = f"EXEC Deletetestntestloginuser @username={id}"
        cursor.execute(query)
        cursor.commit()
        cursor.close()
        flash("User Deleted successfully.")
    return redirect("/users")



# login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username=request.form["username"]
        password=request.form["password"]
        if (username=="test" and password=="test@123"):
            return render_template("dash_login.html")
        else:
            return "User not Active."
    return render_template("login.html")


# logout
@app.route("/logout", methods=["GET", "POST"])
def logout():
    return redirect("/login")

# login welcome page
@app.route("/home", methods=["GET", "POST"])
def login_home():
    return render_template("welcome.html")


