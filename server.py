
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from dotenv import load_dotenv
from flask_socketio import SocketIO, emit
import os
load_dotenv()

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQL_STRING")
db = SQLAlchemy(app)
socketio = SocketIO(app)
