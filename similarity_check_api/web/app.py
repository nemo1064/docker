from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt as bc
import spacy

app=Flask(__name__)
api=Api(app)

client =MongoClient("mongodb://db:27017")

db = client.similarityDB
users= db["Users"]

def UserExists(username):
    if users.find({"Username":username}).count() > 0:
        return True
    else:
        return False

def VerifyPw(username,password):
    if not UserExists(username):
        return False
    else:
        hased_pw=users.find({
            "Username":username
        })[0]["Password"]

        if bc.hashpw(password.encode("utf8"), hased_pw)==hased_pw:
            return True
        else:
            return False

def countToken(username):
    tokens = users.find({
        "Username":username
    })[0]["Tokens"]

    return tokens

class Registration(Resource):
    def post(self):

        pdata = request.get_json()

        username = pdata["username"]
        password = pdata["password"]

        if UserExists(username):
            retjson = {
                "Status":301,
                "Msg":"Username already exists"
            }

            return jsonify(retjson)

        salt = bc.gensalt()
        hashed_pw = bc.hashpw(password.encode("utf8"), salt)
        users.insert_one({
            "Username":username,
            "Password":hashed_pw,
            "Tokens":6
        })

        retjson = {
            "Status":200,
            "Msg":"Sucessfully Registered"
        }

        return jsonify(retjson)

class Detect(Resource):
    def post(self):

        pdata = request.get_json()

        username = pdata["username"]
        password = pdata["password"]
        text1 = pdata["text1"]
        text2 = pdata["text2"]

        if not VerifyPw(username, password):
            retjson = {
                "Status":302,
                "Msg":"Incorect Username or Password"
            }

            return jsonify(retjson)

        Tcount = countToken(username)

        if Tcount <=0:
            retjson = {
                "Status":303,
                "Msg":"Out of Tokens"
            }

            return jsonify(retjson)

        
        nlp = spacy.load('en_core_web_sm')

        text1 = nlp(text1)
        text2 = nlp(text2)

        ratio = text1.similarity(text2)

        retjson = {
            "Status":200,
            "Similarity":ratio,
            "Msg":"Similarity score calculation sucessful"
        }

        users.update({
            "Username":username
        },{
            "$set":
            {"Tokens":Tcount-1}
        })

        return jsonify(retjson)

class refillTokens(Resource):
    def post(self):
        aPW="abc123"
        
        pdata = request.get_json()

        username = pdata["username"]
        adminPW = pdata["adminPassword"]
        refill = pdata["tokens"]

        if not UserExists(username):
            retjson = {
                "Status":303,
                "Msg":"Invalid Username"
            }

            return jsonify(retjson)

        if adminPW != aPW:
            retjson = {
                "Status":304,
                "Msg":"Invalid Admin Password"
            } 
            return jsonify(retjson)

        tokens = countToken(username)

        users.update({
            "Username":username
        },{
            "$set":{
                "Tokens":tokens+refill
            }
        })

        retjson = {
            "Status":200,
            "Msg":"Tokens refilled"
        }

        return jsonify(retjson)

api.add_resource(Registration ,"/register")
api.add_resource(Detect, "/check")
api.add_resource(refillTokens, "/refill")

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)