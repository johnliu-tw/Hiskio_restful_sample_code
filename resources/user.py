from flask_restful import Resource
from flask_restful import reqparse
from flask import jsonify
import pymysql
import json

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "password"
DB_SCHEMA = "flask_demo"


parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('gender')
parser.add_argument('birth')
parser.add_argument('note')

response = {
    'code': 200,
    'msg': 'success'
}

class User (Resource):

    def db_init(self):
        db = pymysql.connect(DB_HOST,DB_USER,DB_PASSWORD,DB_SCHEMA)
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor 

    def get(self, id):    
        db, cursor = self.db_init()
        sql = '''Select * FROM flask_demo.users Where id = {}'''.format(id)
        cursor.execute(sql)
        db.commit()
        user = cursor.fetchall()
        db.close()
        response['data'] = user
        return response

    def put(self, id):
        db, cursor = self.db_init()
        arg = parser.parse_args()
        user = {
            'name': arg['name'],
            'gender': arg['gender'],
            'birth': arg['birth'],
            'note': arg['note']
        }
        query = []
        for key, value in user.items():
            print(key)
            print(value)
            if value != None:
                query.append(key + ' = ' + ' \'{}\' '.format(value))
        query = ','.join(query)
        

        sql = '''Update flask_demo.users Set {} Where id = {}'''.format(query, id)
        result = cursor.execute(sql)
        db.commit()
        db.close()

        response['result'] = True if result == 1 else False

        return response

    def delete(self, id):
        db, cursor = self.db_init()
        sql = '''Delete FROM flask_demo.users Where id = {}'''.format(id)
        result = cursor.execute(sql)
        db.commit()
        db.close()

        response['result'] = True if result == 1 else False
        return response

class Users (Resource):

    def db_init(self):
        db = pymysql.connect(DB_HOST,DB_USER,DB_PASSWORD,DB_SCHEMA)
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor        

    def get(self): 
        db, cursor = self.db_init()
        sql = '''Select * FROM flask_demo.users '''
        cursor.execute(sql)
        db.commit()
        users = cursor.fetchall()
        db.close()
        for user in users:
            user['birth'] = user['birth'].strftime("%Y-%m-%d")

        response['data'] = users
        return response

    def post(self): 
        db, cursor = self.db_init()
        arg = parser.parse_args()
        user = {
            'name': arg['name'],
            'gender': arg['gender'],
            'birth': arg['birth'] or '1900-01-01',
            'note': arg['note']
        }
        sql = '''Insert into flask_demo.users 
                (name, gender, birth, note) 
                values('{}', '{}', '{}', '{}')'''.format(user['name'], user['gender'], user['birth'], user['note'])
        result = cursor.execute(sql)
        db.commit()
        db.close()
        response['result'] = True if result == 1 else False

        return response
        