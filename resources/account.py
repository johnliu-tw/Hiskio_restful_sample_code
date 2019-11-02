from flask_restful import Resource, reqparse
from flask import jsonify
import pymysql
import json

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "password"
DB_SCHEMA = "flask_demo"


parser = reqparse.RequestParser()
parser.add_argument("balance")
parser.add_argument("account_number")
parser.add_argument("user_id")

response = {"code": 200, "msg": "success"}
class Account(Resource):
    def db_init(self):
        db = pymysql.connect(DB_HOST, DB_USER, DB_PASSWORD, DB_SCHEMA)
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor

    def get(self, id):
        db, cursor = self.db_init()
        sql = """Select * FROM flask_demo.accounts Where id = {} and deleted is not  True""".format(id)
        cursor.execute(sql)
        db.commit()
        account = cursor.fetchall()
        db.close()
        response["data"] = account
        return jsonify(response)

    def patch(self, id):
        db, cursor = self.db_init()
        arg = parser.parse_args()
        account = {
            "balance": arg["balance"],
            "account_number": arg["account_number"]
        }
        query = []
        for key, value in account.items():
            if value != None:
                query.append(key + " = " + " '{}' ".format(value))
        query = ",".join(query)

        sql = """Update flask_demo.accounts Set {} Where id = {} and deleted is not  True""".format(query, id)
        result = cursor.execute(sql)
        db.commit()
        db.close()

        response["result"] = True if result == 1 else False

        return jsonify(response)

    def delete(self, id):
        db, cursor = self.db_init()
        sql = """Update flask_demo.accounts Set deleted = True Where id = {}""".format(id)
        result = cursor.execute(sql)
        db.commit()
        db.close()

        response["result"] = True if result == 1 else False
        return jsonify(response)


class Accounts(Resource):
    def db_init(self):
        db = pymysql.connect(DB_HOST, DB_USER, DB_PASSWORD, DB_SCHEMA)
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor

    def get(self):
        db, cursor = self.db_init()
        sql = """Select * FROM flask_demo.accounts where deleted is not True"""
        cursor.execute(sql)
        db.commit()
        accounts = cursor.fetchall()
        db.close()

        response["data"] = accounts
        return jsonify(response)

    def post(self):
        db, cursor = self.db_init()
        arg = parser.parse_args()
        account = {
            "balance": arg["balance"],
            "account_number": arg["account_number"],
            "user_id": arg["user_id"]
        }
        sql = """Insert into flask_demo.accounts 
                (balance, account_number, user_id) 
                values('{}', '{}', '{}')""".format(
            account["balance"], account["account_number"], account["user_id"]
        )
        result = cursor.execute(sql)
        db.commit()
        db.close()
        response["result"] = True if result == 1 else False

        return jsonify(response)