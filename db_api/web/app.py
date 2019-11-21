from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SentencesDatabase
user= db["user"]


#User Registrations
class Register(Resource):
    def post(self):

    # Reading the data recieved via POST
        pdata=request.get_json()

        username = pdata["username"]
        password = pdata["password"]

        salt = bcrypt.gensalt()
        hashed_pwd=bcrypt.hashpw(password.encode("utf8"), salt)

    # Insert User details
        user.insert_one({
            'Username':username,
            'Password':hashed_pwd,
            'Sentences':"",
            "Tokens":10
        })

        retjson = {
            "Status":200,
            "Msg":"Sucessfully resgistered for api"
        }

        return jsonify(retjson)


# Func to validate user
def validateUser(username , password):
    hashed_pw=user.find({
        "Username":username
        })[0]["Password"]

    if bcrypt.hashpw(password.encode("utf8"), hashed_pw)==hashed_pw:
        return True
    else:
        return False

#Func to keep count of Tokens
def countTokens(username):
    tokens=user.find({
        "Username":username
        })[0]["Tokens"]
    return tokens

#Storing Sentences
class Store(Resource):
    def post(self):
        pdata=request.get_json()

        username = pdata["username"]
        password = pdata["password"]
        sentence = pdata["sentence"]

        # Validate User
        cpass=validateUser(username, password)

        if not cpass:
            retjson={
                "Status":302,
                "Msg":"Wrong Username or Password"
            }
            return jsonify(retjson)
        # Token Validation
        count_Tokens = countTokens(username)

        if count_Tokens <= 0:
            retjson= {
                "Status":301,
                "Msg":"Not enough tokens"
            }
            return jsonify(retjson)
        # Store Sentence

        user.update({
            "Username":username
            },{
                "$set": {
                    "Sentence":str(sentence),
                    "Tokens":count_Tokens-1
                } 
        })
        retjson = {
            "Status":200,
            "Msg":"Sentence saved sucessfully"
        }

        return jsonify(retjson)

# Get the sentence
class Get(Resource):
    def post(self):
    
        pdata = request.get_json()

        username = pdata["username"]
        password = pdata["password"]

         # Validate User
        cpass=validateUser(username, password)

        if not cpass:
            retjson={
                "Status":302,
                "Msg":"Wrong Username or Password"
            }
            return jsonify(retjson)

        # Token Validation
        count_Tokens = countTokens(username)

        if count_Tokens <= 0:
            retjson= {
                "Status":301,
                "Msg":"Not enough tokens"
            }
            return jsonify(retjson)

        user.update({
            "Username":username
            } , {
                "$set": {
                    "Tokens":count_Tokens-1
                }
            })

        sentence = user.find({
            "Username": username
        })[0]["Sentence"]
        retjson={ 
            "Status":200,
            "Sentence": str(sentence)
        }
        return jsonify(retjson)

#Adding Tokens 
class AddToken(Resource):
    def post(self):

        pdata= request.get_json()

        username = pdata["username"]
        password = pdata["password"]

    # Validate User
        cpass=validateUser(username, password)

        if not cpass:
            retjson={
                "Status":302,
                "Msg":"Wrong Username or Password"
            }
            return jsonify(retjson)

        user.update({
            "Username":username
        },{
            "$set": {
                "Tokens":10
            }
        })

        retjson = {
            "Status":200,
            "Msg":"Tokens added"
        }

        return jsonify(retjson)




api.add_resource(Register, "/register")
api.add_resource(Store, "/store")
api.add_resource(Get, "/get")
api.add_resource(AddToken, "/addTokens")

if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True)




        

        


        














    



