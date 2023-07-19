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

from User.views import profile
from Entreprise.views import entreprise


=======
from Factures.views import facture
from Logo import upload
>>>>>>> e67c56819950ebaca063aaf76779e0a0acab5498
app = Flask(__name__)
app.template_folder = "templates"
CORS(app)
load_dotenv()
<<<<<<< HEAD


app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
=======
app.config["JWT_TOKEN_LOCATION"] = ["headers", "query_string"]
app.config["JWT_HEADER_TYPE"] = ""
app.config["JWT_HEADER_NAME"] = "Authorization"
app.config["JWT_QUERY_STRING_NAME"] = "token"
app.config["JWT_QUERY_STRING_VALUE_PREFIX"] = "Bearer"
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

>>>>>>> e67c56819950ebaca063aaf76779e0a0acab5498






api = Api(app)
db.init_app(app)
app.secret_key = os.getenv("SECRET_KEY")


<<<<<<< HEAD
@app.route("/")
def hello_client():  # put application's code here
    return "Hello client!"


app.register_blueprint(contract)
app.register_blueprint(client)


# @app.before_first_request
# def create_tables():
#   db.create_all()
=======

@app.route('/')
def hello_world():  # put application's code here
    return 'Bienvenue au Gestion Commerciale PME !'

app.register_blueprint(upload)
app.register_blueprint(facture)


>>>>>>> e67c56819950ebaca063aaf76779e0a0acab5498

app.register_blueprint(profile)
app.register_blueprint(entreprise)

<<<<<<< HEAD

=======
#@app.before_first_request
#def create_tables():
 #   db.create_all()
>>>>>>> e67c56819950ebaca063aaf76779e0a0acab5498
with app.app_context():
    db.create_all()
# @app.before_first_request
# def create_tables():
# db.create_all()


# apload_image


<<<<<<< HEAD
if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
=======

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=5000, host="0.0.0.0")
>>>>>>> e67c56819950ebaca063aaf76779e0a0acab5498
