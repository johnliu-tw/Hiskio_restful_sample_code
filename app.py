from resources.user import User, Users
from resources.account import Account, Accounts
from flask import jsonify, request, render_template
from flask_restful import Api, Resource
import pymysql
import flask
import os
import jwt
from server import app
from dotenv import load_dotenv
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_SCHEMA = os.getenv("DB_SCHEMA")

api = Api(app)

api.add_resource(User, "/user/<id>")
api.add_resource(Users, "/users")
api.add_resource(Account, "/account/<id>")
api.add_resource(Accounts, "/accounts")

response = {"code": 200, "msg": "success"}

# # 管理所有的錯誤，讓回傳的錯誤訊息不包含程式碼和提示
# @app.errorhandler(Exception)
# def handle_unexpected_error(error):
#     status_code = 500
#     if type(error).__name__ == "NotFound":
#         status_code = 404
#     elif type(error).__name__ == "TypeError":
#         status_code = 500
#     return {
#         'code': status_code,
#         'msg': type(error).__name__
#     }

# 簡單的驗證授權機制
# @app.before_request
# def auth():
#     token = request.headers.get('auth')
#     user_id = request.get_json()['user_id']
#     # user_id = request.args.get('user_id', None)
#     valid_token = jwt.encode({'user_id': user_id}, 'password', algorithm='HS256').decode('utf-8')
#     if token == valid_token:
#         pass
#     else:
#         return {
#             'code': 401,
#             'msg': 'invalid token'
#         }

@app.route("/", methods=["GET"])
def home():
    return "Hello World"

# 客製化的 route 路由 endpoint 
@app.route('/account/<account_number>/deposit', methods=["POST"])
def deposit(account_number):
    db, cursor, account = get_account(account_number)
    money = request.values['money']
    balance = account['balance'] + int(money)

    sql = """Update flask_demo.accounts Set balance = {} Where account_number = {} and deleted is not True""".format(balance, account_number)
    result = cursor.execute(sql)
    db.commit()
    db.close()
    response["result"] = True if result == 1 else False

    return jsonify(response)

@app.route('/account/<account_number>/withdraw', methods=["POST"])
def withdraw(account_number):
    db, cursor, account = get_account(account_number)
    money = request.values['money']
    balance = account['balance'] - int(money)
    if balance < 0:
        response["msg"] = 'money not enough'
        response["code"] = 400
        return jsonify(response)
    else:
        sql = """Update flask_demo.accounts Set balance = {} Where account_number = {} and deleted is not True""".format(balance, account_number)
        result = cursor.execute(sql)
        db.commit()
        db.close()
        response["result"] = True if result == 1 else False

    return jsonify(response)

@app.route('/login', methods=['GET'])
def login():
    return render_template("login.html")

def get_account(account_number):
    db = pymysql.connect(DB_HOST, DB_USER, DB_PASSWORD, DB_SCHEMA)
    cursor = db.cursor(pymysql.cursors.DictCursor)

    sql = """Select * FROM flask_demo.accounts Where account_number = {} and deleted is not True""".format(account_number)
    cursor.execute(sql)
    db.commit()
    return db, cursor, cursor.fetchone()    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3333)
