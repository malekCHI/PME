from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
from db import db
from flask_restful import Api
from User.views import userProfile

app = Flask(__name__)
CORS(app)
load_dotenv()


app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True



api = Api(app)
db.init_app(app)
app.secret_key = os.getenv("SECRET_KEY")


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


app.register_blueprint(userProfile)


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':

    app.run(debug=True, port=5000, host="0.0.0.0")