from flask import Flask
from flask_restful import Api


app = Flask(__name__)
api = Api(app)

@app.route('/', methods=['GET'])
def index():
    return {
        'status':'rodando',
        'message':'hello world! =D'
    }


app.run(debug=True, host = "192.168.1.168", port = 35000)