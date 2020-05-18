from flask_restful import Resource, reqparse
from flask import jsonify
import pymysql
import json
import os
from dotenv import load_dotenv
from server import db
from models import UserModel
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_SCHEMA = os.getenv("DB_SCHEMA")


parser = reqparse.RequestParser()
parser.add_argument("name")
parser.add_argument("gender")
parser.add_argument("birth")
parser.add_argument("note")

response = {"code": 200, "msg": "success"}
class User(Resource):
    def db_init(self):
        db = pymysql.connect(DB_HOST, DB_USER, DB_PASSWORD, DB_SCHEMA)
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor

    def get(self, id):
        # db, cursor = self.db_init()
        # sql = """Select * FROM flask_demo.users Where id = {} and deleted is not True""".format(id)
        # cursor.execute(sql)
        # db.commit()
        # user = cursor.fetchall()
        # db.close()
        user = UserModel.query.get(id)
        return jsonify({'data': user.serialize()})

    def patch(self, id):
        arg = parser.parse_args()
        # user = {
        #     "name": arg["name"],
        #     "gender": arg["gender"],
        #     "birth": arg["birth"],
        #     "note": arg["note"],
        # }
        # query = []
        # for key, value in user.items():
        #     if value != None:
        #         query.append(key + " = " + "'{}'".format(value))
        # query = ", ".join(query)

        user = UserModel.query.filter_by(id=id, deleted=None).first()
        if arg['name'] is not None:
            user.name = arg['name']
        db.session.commit()

        response["result"] = True

        return jsonify(response)

    def delete(self, id):
        # db, cursor = self.db_init()
        user = UserModel.query.filter_by(id=id, deleted=None).first()
        db.session.delete(user)
        db.session.commit()

        response["result"] = True
        return jsonify(response)


class Users(Resource):
    def db_init(self):
        db = pymysql.connect(DB_HOST, DB_USER, DB_PASSWORD, DB_SCHEMA)
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor

    def get(self):
        users = UserModel.query.filter(UserModel.deleted.isnot(True)).all()
        return jsonify({'data': list(map(lambda user: user.serialize(), users))})

    def post(self):
        arg = parser.parse_args()
        user = {
            "name": arg["name"],
            "gender": arg["gender"],
            "birth": arg["birth"] or "1900-01-01",
            "note": arg["note"],
        }

        new_user = UserModel(name=user["name"], 
        gender=user["gender"], birth=user["birth"], note=user["note"])
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'msg': 'success'})