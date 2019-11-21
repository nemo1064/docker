from flask import Flask, jsonify,request
from flask_restful import Api,Resource
from pymongo import MongoClient


app=Flask(__name__)
api=Api(app)

client = MongoClient("mongodb://db:27017")
db = client.anewDB

UserNum = db["UserNum"]

UserNum.insert({
    "num_of_visits":0
})

class visit(Resource):
    def get(self):
        prev_num = UserNum.find({})[0]["num_of_visits"]
        new_num = prev_num+1
        UserNum.update({},{"$set":{"num_of_visits":new_num}})
        return str("Hello There! Padawan : "+str(new_num))

api.add_resource(visit , "/hello")


def checkdata(data, functionname):
    if functionname=="add" or functionname =="subtract" or functionname == "multiply" :
        if "x" not in data or "y" not in data:
            return 301
        else:
            return 200
    elif functionname =="divide":
        if "x" not in data or "y" not in data:
            return 301
        elif data["y"]==0:
            return 302
        else:
            return 200


class Add(Resource):
    def post(self):

        data=request.get_json()
        satusCode=checkdata(data,"add")
        if satusCode!=200:
            retE={
                "Message":"An Error Occured",
                "Status Code":satusCode
            }
            return jsonify(retE)

        x=data["x"]
        y=data["y"]
        x=int(x)
        y=int(y)
        ret=x+y
        retMap = {
            'Sum':ret,
            'Status Code':200
        }

        return jsonify(retMap)

api.add_resource(Add , "/add")


class Subtract(Resource):
    def post(self):
        data=request.get_json()
        satusCode=checkdata(data,"subtract")
        if satusCode!=200:
            retE={
                "Message":"An Error Occured",
                "Status Code":satusCode
            }
            return jsonify(retE)

        x=data["x"]
        y=data["y"]
        x=int(x)
        y=int(y)
        ret=x-y
        retMap = {
            'Difference':ret,
            'Status Code':200
        }

        return jsonify(retMap)

api.add_resource(Subtract , "/subtract")

class Multiply(Resource):
    def post(self):
        data=request.get_json()
        satusCode=checkdata(data,"multiply")
        if satusCode!=200:
            retE={
                "Message":"An Error Occured",
                "Status Code":satusCode
            }
            return jsonify(retE)

        x=data["x"]
        y=data["y"]
        x=int(x)
        y=int(y)
        ret=x*y
        retMap = {
            'Product':ret,
            'Status Code':200
        }

        return jsonify(retMap)

api.add_resource(Multiply , "/multiply")

class Divide(Resource):
    def post(self):
        data=request.get_json()
        satusCode=checkdata(data,"divide")
        if satusCode!=200:
            retE={
                "Message":"An Error Occured",
                "Status Code":satusCode
            }
            return jsonify(retE)

        x=data["x"]
        y=data["y"]
        x=int(x)
        y=int(y)
        ret=x/y
        retMap = {
            'Quotient':ret,
            'Status Code':200
        }

        return jsonify(retMap)

api.add_resource(Divide , "/divide")
@app.route('/')
def hello_world():
    return "Hello World!"
if __name__=="main":
    app.run()

@app.route('/habibi')
def walla():
    age=2*11
    js={
        'Name': 'Abdul',
        'Age':age,
        'phone':[
            {
                'phoneName':'Mi A1',
                'phoneNumber':123456
            },

            {
                'phoneName':'OnePlus 7pro',
                'phoneNumber':123789
            }
        ]
    }
    return jsonify(js)
"""@app.route("/add_two_nums",  methods=["POST"])
def add():
    dataDict=request.get_json()

    if "X" not in dataDict:
        return "Error", 305
    else:
        
        X=dataDict["X"]
        Y=dataDict["Y"]

        Z=X+Y

        rtJSON={
            "Z":Z
        }

        return jsonify(rtJSON), 200

"""


if __name__=="__main__":
    app.run(host='0.0.0.0',debug=True)

