from resources.user import User, Users
import flask
from flask import request
from flask import jsonify
from flask_restful import Api
from flask_restful import Resource
import pymysql

app = flask.Flask(__name__)
app.config["DEBUG"] = True

api = Api(app)

api.add_resource(User, "/user/<id>")
api.add_resource(Users, "/users")


@app.route("/", methods=["GET"])
def home():
    return "Hello World"



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
