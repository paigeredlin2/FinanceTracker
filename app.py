from flask import Flask, render_template
from livereload import Server
from dotenv import load_dotenv
import os

load_dotenv(override=True) #load our own env file, override disallows caching

from models import db, Users, Earnings, Expenses
from utilities import initialize_db

environment = os.getenv("ENV", "production")

app = Flask(__name__)
app.config["DEBUG"] = environment == "development"
#database connections
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app) #bind db and app

@app.route('/')
def index():
	return render_template("index.html")

if __name__ == "__main__":
	server = Server(app.wsgi_app)
	server.watch("static/*")
	server.watch("templates/*")
	server.serve(port=5000)