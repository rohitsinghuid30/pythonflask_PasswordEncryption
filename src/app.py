from flask import Flask
import os
from dotenv import load_dotenv
import pyodbc

# load enviroment
load_dotenv()

app = Flask(__name__,template_folder="templates", static_folder="static")
secret_key=os.getenv("SECRET_KEY")
SERVER=os.getenv("SERVER")
DB=os.getenv("DATABASE")
Driver=os.getenv("Driver")

# DB Connection
connection_string = f"DRIVER={Driver};SERVER={SERVER}; DATABASE={DB}; Trusted_Connection=True; MultipleActiveResultSets=True;"
db_conn = pyodbc.connect(connection_string)


@app.route("/", methods=["GET"])
def home():
    pass

