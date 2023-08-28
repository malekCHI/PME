from flask import Flask, jsonify, request, render_template, redirect
from flask_cors import CORS
from dotenv import load_dotenv
import os

from db import db
import time
from flask_restful import Api
from Client.views import client
from Contracts.views import contract
from Paiement.views import paiement
from Mail.views import eemail
from TaskList.views import task
from Email.views import email
from Profile.views import profiles
from Entreprise.views import entreprise
from Factures.views import facture
from Relance.views import relance
from Chiffres_D_affaires.views import cda
from Logo import upload
from Previlege.views import previlege
from User.views import user
from mail import mail

from flask_apscheduler import APScheduler
from flask_jwt_extended import (
    JWTManager
)
app = Flask(__name__)

app.template_folder = "./Mail/template"
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
# configuration of mail
app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'carryusvayne@hotmail.fr'
app.config['MAIL_PASSWORD'] = '50Aloulou007'
app.config['MAIL_USE_TLS'] = True   # Set to True for TLS
app.config['MAIL_USE_SSL'] = False  # Set to False for SSL
app.config['MAIL_DEFAULT_SENDER'] = 'carryusvayne@hotmail.fr'
mail.init_app(app)


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


app.register_blueprint(contract)
app.register_blueprint(client)
app.register_blueprint(upload)
app.register_blueprint(facture)
app.register_blueprint(profiles)
app.register_blueprint(entreprise)
app.register_blueprint(paiement)
app.register_blueprint(relance)
app.register_blueprint(email)
app.register_blueprint(user)
app.register_blueprint(previlege)
app.register_blueprint(cda)
app.register_blueprint(task)


@app.route("/")
def hello_world():  # put application's code here
    return "Bienvenue au Gestion Commerciale PME !"


with app.app_context():
    db.create_all()
# @app.before_first_request
# def create_tables():
#     with app.app_context():
#         db.create_all()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=5000, host="0.0.0.0")
