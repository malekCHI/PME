from flask_cors import CORS
from dotenv import load_dotenv
import os
from flask import Flask,jsonify
from db import db
from flask_restful import Api
from Profile.views import profiles
from Entreprise.views import entreprise
from Previlege.views import previlege
from User.views import user
from flask_jwt_extended import (
    JWTManager
)
app = Flask(__name__)
CORS(app)
load_dotenv()


app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True


api = Api(app)
db.init_app(app)
SECRET_KEY = os.getenv("SECRET_KEY")
app.config['SECRET_KEY'] = SECRET_KEY
jwt = JWTManager(app)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


app.register_blueprint(profiles)
app.register_blueprint(previlege)
app.register_blueprint(entreprise)
app.register_blueprint(user)

with app.app_context():
    db.create_all()
#@app.before_first_request
#def create_tables():
    #db.create_all()


if __name__ == '__main__':
    app.run(debug=True, port=5000)