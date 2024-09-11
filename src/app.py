from flask import Flask, render_template, flash, redirect, request, url_for
import os
from dotenv import load_dotenv
import pyodbc

# load enviroment
load_dotenv()

app = Flask(__name__,template_folder="templates", static_folder="static")
# app.secret_key=os.getenv("SECRET_KEY")
app.secret_key=os.urandom(12)
SERVER=os.getenv("SERVER")
DB=os.getenv("DATABASE")
Driver=os.getenv("Driver")

# DB Connection
connection_string = f"DRIVER={Driver};SERVER={SERVER}; DATABASE={DB}; Trusted_Connection=True; MultipleActiveResultSets=True;"
db_conn = pyodbc.connect(connection_string)


# Plain text/Encrypted/Decrypted Password
@app.route("/", methods=["GET"])
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
        ptp.append({"username":username, "password":password, "created_At":created_At})
    
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

    return render_template("home.html", ptp=ptp, EPS=EPS)

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
    return redirect("/")


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
    return redirect("/")