from flask import Flask, jsonify, request, render_template, redirect
from flask_cors import CORS
from dotenv import load_dotenv
import os
from db import db
from flask_restful import Api

from Client.views import client
from Contracts.views import contract
import os
from flask_sqlalchemy import SQLAlchemy

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


app.register_blueprint(contract)
app.register_blueprint(client)


# @app.before_first_request
# def create_tables():
#   db.create_all()
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
