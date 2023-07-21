from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
from db import db
from flask_restful import Api
from Factures.views import facture
from Logo import upload
from Email.views import email
app = Flask(__name__)
CORS(app)
load_dotenv()
app.config["JWT_TOKEN_LOCATION"] = ["headers", "query_string"]
app.config["JWT_HEADER_TYPE"] = ""
app.config["JWT_HEADER_NAME"] = "Authorization"
app.config["JWT_QUERY_STRING_NAME"] = "token"
app.config["JWT_QUERY_STRING_VALUE_PREFIX"] = "Bearer"
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True







api = Api(app)
db.init_app(app)
app.secret_key = os.getenv("SECRET_KEY")



@app.route('/')
def hello_world():  # put application's code here
    return 'Bienvenue au Gestion Commerciale PME !'

app.register_blueprint(upload)
app.register_blueprint(facture)
app.register_blueprint(email)




#@app.before_first_request
#def create_tables():
 #   db.create_all()
with app.app_context():
    db.create_all()




if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=5000, host="0.0.0.0")