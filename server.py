
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from dotenv import load_dotenv
from flask_socketio import SocketIO, emit
from flasgger import Swagger
import os
load_dotenv()

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQL_STRING")
db = SQLAlchemy(app)
socketio = SocketIO(app)

template = {
  "swagger": "2.0",
  "info": {
    "title": "JohnLiu's demo swagger",
    "description": "示範用的 API 文件",
    "version": "1.0.0"
  },
  "host": "localhost:443",
  "basePath": "",
  "schemes": [
    "http",
    "https"
  ],
  "tags":[
    {
      "name": "User",
      "description": "系統中的使用者資訊"
    },
    {
      "name": "Account",
      "description": "系統中的帳戶資訊"
    }
  ]
}
swagger = Swagger(app, template=template)


