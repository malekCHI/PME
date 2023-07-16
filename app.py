from flask import Flask, jsonify, request, render_template, redirect
from flask_cors import CORS
from dotenv import load_dotenv
import os
from db import db
from flask_restful import Api
<<<<<<< HEAD

from Client.views import client
from Contracts.views import contract
import os
from flask_sqlalchemy import SQLAlchemy
=======
from User.views import profile
from Entreprise.views import entreprise
>>>>>>> 3f3d2f39d8ce4e2ce8691828f5b706e70f730b84

app = Flask(__name__)
CORS(app)
load_dotenv()


app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True


api = Api(app)
db.init_app(app)
app.secret_key = os.getenv("SECRET_KEY")


@app.route("/")
def hello_client():  # put application's code here
    return "Hello client!"


<<<<<<< HEAD
app.register_blueprint(contract)
app.register_blueprint(client)


# @app.before_first_request
# def create_tables():
#   db.create_all()
=======
app.register_blueprint(profile)
app.register_blueprint(entreprise)

>>>>>>> 3f3d2f39d8ce4e2ce8691828f5b706e70f730b84
with app.app_context():
    db.create_all()
#@app.before_first_request
#def create_tables():
    #db.create_all()

<<<<<<< HEAD
if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
=======

if __name__ == '__main__':

    app.run(debug=True, port=5000)
>>>>>>> 3f3d2f39d8ce4e2ce8691828f5b706e70f730b84
