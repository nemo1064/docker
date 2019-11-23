from flask import Flask, jsonify , request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt as bc

app=Flask(__name__)
api=Api(app)

client = MongoClient("mongodb://db:27017")
db=client.BANKapi

users=db["Users"]


def UserExists(username):

    if users.find({"Username":username}).count() == 0:
        return False
    else:
        return True

def retJson(status, msg):
    retjson = {
        "Status":status,
        "Msg":msg
    }

    return retjson


def VerifyPw(username, password):
    if  not UserExists(username):
        return False

    hashed_pw=users.find({
        "Username":username
        })[0]["Password"]

    if bc.hashpw(password.encode('utf8'), hashed_pw)==hashed_pw:
        return True
    else:
        return False

def VerifyCredentials(username, password):
    if not UserExists(username):
        return retJson(301,"Invalid Username"), True

    correct_pw = VerifyPw(username, password)

    if not correct_pw:
        return retJson(302, "Incrrect Password"), True

    return None, False

def CashWithUser(username):
    cash = users.find({
        "Username":username
        })[0]["Own"]
    return cash

def DebtWithUser(username):
    debt = users.find({
        "Username":username
        })[0]["Debt"]
    return debt

def UpdateBalance(username, balance):
    users.update({
        "Username":username
    },{
        "$set":{
            "Own":balance
        }
    })

def UpdateDebt(username, balance):
    users.update({
        "Username":username
    },{
        "$set":{
            "Debt":balance
        }
    })

class Regsiter(Resource):
    def post(self):

        pdata = request.get_json()

        username = pdata["username"]
        password = pdata["password"]

        if UserExists(username):
            return jsonify(retJson(301, "User name taken"))

        hashed_pw=bc.hashpw(password.encode("utf8"),bc.gensalt())
        users.insert_one({
            "Username":username,
            "Password":hashed_pw,
            "Own":0,
            "Debt":0
        })

        return jsonify(retJson(200 , "User Suceefully Regsitered"))

class Add(Resource):
    def post(self):
        pdata = request.get_json()

        username = pdata["username"]
        password = pdata["password"]
        money    = pdata["amount"]

        retjson , error = VerifyCredentials(username,password)

        if error:
            return jsonify(retjson)

        if money <=0:
            return jsonify(retJson(304,"Amount is less than zero"))

        money = money-1

        bankbalance = CashWithUser("BANK")
        userbalance = CashWithUser(username)

        UpdateBalance(username, userbalance+money)
        UpdateBalance("BANK", bankbalance+1)

        return jsonify(retJson(200, "Amount added sucessfully to account"))

class Transfer(Resource):
    def post(self):

        pdata= request.get_json()

        username = pdata["username"]
        password = pdata["password"]
        toUser   = pdata["to"]
        amount   = pdata["amount"]


        retjson, error = VerifyCredentials(username, password)

        if error:
            return jsonify(retjson)

        if not UserExists(toUser):
            return jsonify(retJson(303, "Invalid reciever"))

        
        if amount <=0:
            return jsonify(retJson(304,"Amount is less than zero"))
        
        userbalance = CashWithUser(username)

        if amount > userbalance:
            return jsonify(retJson(305,"Amount greater than Balance in account"))


        bankbalance = CashWithUser("BANK")
        UpdateBalance("BANK",bankbalance+1)

        UpdateBalance(username, userbalance-amount)

        toUserbalance  = CashWithUser(toUser)
        UpdateBalance(toUser, toUserbalance+amount-1)


        return jsonify(retJson(200, "Amount succefully transfered"))


class CheckBalance(Resource):
    def post(self):

        pdata = request.get_json()

        username = pdata["username"]
        password = pdata["password"]

        retjson,  error = VerifyCredentials(username, password)

        if error:
            return jsonify(retjson)
        
        retjson = users.find({
            "Username":username
        },{
            "Password":0,
            "_id":0
        })[0]

        return jsonify(retjson)

class TakeLoan(Resource):
    def post(self):
        pdata = request.get_json()

        username = pdata["username"]
        password = pdata["password"]
        money    = pdata["amount"]

        retjson,  error = VerifyCredentials(username, password)
         
        if error:
            return jsonify(retjson)

        if money <= 0:
            return(jsonify(retJson(303, "Amount is less than zero")))

        cash = CashWithUser(username)
        debt = DebtWithUser(username)
        debtBank = DebtWithUser("BANK")

        UpdateBalance(username, cash+money)
        UpdateDebt(username, debt+money)
        UpdateDebt("BANK", -(debtBank+money))

        return jsonify(retJson(200, "Loan Successfully Approved"))

class PayLoan(Resource):
    def post(self):
        pdata = request.get_json()

        username = pdata["username"]
        password = pdata["password"]
        money    = pdata["amount"]

        retjson,  error = VerifyCredentials(username, password)

        if error:
            return jsonify(retjson)

        if money <= 0:
            return(jsonify(retJson(303, "Amount is less than zero")))

        cash = CashWithUser(username)
        if money > cash:
            return jsonify(retJson(305,"Amount greater than Balance in account"))

        
        debt = DebtWithUser(username)
        debtBank = DebtWithUser("BANK")


        UpdateBalance(username, cash-money)
        UpdateDebt(username, debt-money)
        UpdateDebt("BANK", debtBank+money)

        return jsonify(200, "Amount received Successfully towards loan")


api.add_resource(Regsiter , "/register")
api.add_resource(Add , "/add")
api.add_resource(Transfer, "/transfer")
api.add_resource(CheckBalance, "/balance")
api.add_resource(TakeLoan, "/takeloan")
api.add_resource(PayLoan, "/payloan")

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)






















        



