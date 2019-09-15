from resources.user import User, Users
from flask import jsonify, request, Blueprint
from flask_restful import Api, Resource
import pymysql
import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True

api = Api(app)

api.add_resource(User, "/user/<id>")
api.add_resource(Users, "/users")

@app.errorhandler(Exception)
def handle_unexpected_error(error):
    status_code = 500
    if type(error).__name__ == "NotFound":
        status_code = 404
    elif type(error).__name__ == "TypeError":
        status_code = 500
    return {
        'code': status_code,
        'msg': type(error).__name__
    }

@app.before_request
def auth():
    token = request.headers.get('auth')
    print(token)
    if token == '567':
        pass
    else:
        return {
            'code': 401,
            'msg': 'invalid token'
        }

@app.route("/", methods=["GET"])
def home():
    return "Hello World"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
