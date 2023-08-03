from flask import Flask, jsonify, request, render_template, redirect
from flask_cors import CORS
from dotenv import load_dotenv
import os
from db import db
from flask_restful import Api
from Client.views import client
from Contracts.views import contract
from Paiement.views import paiement

from Email.views import email
# from User.views import profile
from Entreprise.views import entreprise
from Factures.views import facture
from Relance.views import relance 

from Logo import upload

app = Flask(__name__)
app.template_folder = "templates"
CORS(app)
load_dotenv()


app.config["JWT_TOKEN_LOCATION"] = ["headers", "query_string"]
app.config["JWT_HEADER_TYPE"] = ""
app.config["JWT_HEADER_NAME"] = "Authorization"
app.config["JWT_QUERY_STRING_NAME"] = "token"
app.config["JWT_QUERY_STRING_VALUE_PREFIX"] = "Bearer"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True


api = Api(app)
db.init_app(app)
app.secret_key = os.getenv("SECRET_KEY")


app.register_blueprint(contract)
app.register_blueprint(client)
app.register_blueprint(upload)
app.register_blueprint(facture)
# app.register_blueprint(profile)
app.register_blueprint(entreprise)
app.register_blueprint(paiement)
app.register_blueprint(relance)
app.register_blueprint(email)

@app.route("/")
def hello_world():  # put application's code here
    return "Bienvenue au Gestion Commerciale PME !"


with app.app_context():
    db.create_all()
# @app.before_first_request
# def create_tables():
# db.create_all()


# apload_image


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=5000, host="0.0.0.0")
