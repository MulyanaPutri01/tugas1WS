from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import os
import datetime
from functools import wraps
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
api = Api(app)
CORS(app)

filename = os.path.dirname(os.path.abspath(__file__))
database = 'sqlite:///' + os.path.join(filename, 'db_VSbigpro.db')
app.config['SECRET_KEY']='semangat45'
app.config['SQLALCHEMY_DATABASE_URI']=database
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class Users(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     username = db.Column(db.String(50))
     password = db.Column(db.String(10))

from app import db
db.create_all()

DATABASE_NAME = "db_VSbigpro.db"

def get_db():
    conn = sqlite3.connect(DATABASE_NAME)
    return conn


class RegisterUser(Resource):
    def post(self):
        dataUsername = request.form.get('username')
        dataPassword = request.form.get('password')

        if dataUsername and dataPassword:
            dataModel = Users(username=dataUsername, password=dataPassword)
            db.session.add(dataModel)
            db.session.commit()
            return make_response(jsonify({"msg":"registered successfully"}), 200)
        return jsonify({"msg":"Username/Password cannot be empty"})

class LoginUser(Resource):
    def post(self):
        dataUsername = request.form.get('username')
        dataPassword = request.form.get('password')

        queryUsername = [data.username for data in Users.query.all()]
        queryPassword = [data.password for data in Users.query.all()]
        if dataUsername in queryUsername and dataPassword in queryPassword:

            token = jwt.encode(
                {
                    "username":queryUsername, 
                    "exp":datetime.datetime.utcnow() + datetime.timedelta(minutes=120)
                }, app.config['SECRET_KEY'], algorithm="HS256"
            )
            return make_response(jsonify({"msg":"Login Succesfull", "token":token}), 200)
        return jsonify({"msg":"Login Gagal"})

api.add_resource(RegisterUser, "/register", methods=["POST"])
api.add_resource(LoginUser, "/api/v1/login", methods=["POST"])



if  __name__ == '__main__':  
     app.run(debug=True)