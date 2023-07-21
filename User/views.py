from flask import Blueprint, request, jsonify
from User.models import UserModel
from Profile.models import ProfileModel
from passlib.hash import bcrypt
import bcrypt
from sqlalchemy.exc import IntegrityError
from db import db
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
import bcrypt
from werkzeug.security import generate_password_hash,check_password_hash
from User.utils import add_user,update_user,delete_user


profile = Blueprint("profile", __name__, url_prefix="/profile")
user = Blueprint("user", __name__, url_prefix="/users")


@user.post('/register')
def signup_user():
    try:
        print(request.json)
        nom = request.json.get('nom', None)
        prenom = request.json.get('prenom', None)
        email = request.json.get('email', None)
        password_hash = request.json.get('password_hash', None)
        description = request.json.get('description', None)
        profile_id = request.json.get('profile_id', None)
        
        if not email:
            return 'Missing email', 400
        if not password_hash:
            return 'Missing password', 400
        hashed = generate_password_hash(password_hash, method='sha256')
        #hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        profile = ProfileModel.query.get(profile_id)
        if not profile:
            return 'Profile not found', 400
        add_user(nom, prenom, email,hashed,description,profile_id)
        access_token = create_access_token(identity={"email": email})
        return {"access_token": access_token}, 200
    except IntegrityError:
        # the rollback func reverts the changes made to the db
        db.session.rollback()
        return 'User Already Exists', 400
    except AttributeError:
        return 'Provide an Email and Password in JSON format in the request body', 400


@user.post('/login')
def login_user():
    try:
        print(request.json)
        email = request.json.get('email', None)
        password = request.json.get('password', None)
        
        if not email:
            return 'Missing email', 400
        if not password:
            return 'Missing password', 400
        
        user = UserModel.query.filter_by(email=email).first()
        if not user:
            return 'User Not Found!', 404   

        if check_password_hash(user.password_hash,password):
        # Verify the provided password
            access_token = create_access_token(identity={"email": email})
            return {"access_token": access_token}, 200
        else:
            return 'Invalid Login Info!', 400
    except AttributeError:
        return 'Provide an Email and Password in JSON format in the request body', 400


@user.get('/getusers')
def get_user():
    pages = request.args.get('page')
    per_page = 10
    id_user = request.args.get('id_user')

    if not pages:
        if id_user:
            return {'user': list(map(lambda x: x.serialize(), UserModel.query.filter_by(id_user=id_user)))}
        else:
            return {'users': list(map(lambda x: x.serialize(), UserModel.query.all()))}
    else:
        page = int(pages)
        if id_user:
            return {'user': list(map(lambda x: x.serialize(), UserModel.query.filter_by(id_user=id_user).paginate(page, per_page, error_out=False).items))}
        else:
            return {'users': list(map(lambda x: x.serialize(), UserModel.query.paginate(page, per_page, error_out=False).items))}


@user.put('/update/<int:_id_user>')
def edit_user(_id_user):
    _nom = request.json.get('nom', None)
    _prenom = request.json.get('prenom', None)
    _email = request.json.get('email', None)
    _password_hash = request.json.get('password_hash', None)
    _description = request.json.get('description', None)
    _profile_id = request.json.get('profile_id', None)

    if not (_id_user and _nom ):
        return jsonify({
            "error": "Please enter a valid ID and  name!"
         }), 400

    if update_user(_id_user, _nom,_prenom,_email,_password_hash, _description,_profile_id):
        return jsonify({
             'message': "user updated",
         }), 200
    else:
        return jsonify({'error': "No user found with the given ID!"}), 404


@user.delete('/delete/<int:_id_user>')
def remove_user(_id_user):
    if not (_id_user):
            return jsonify({
            "error": "Please enter a valid ID!"
         }), 400
    if delete_user(_id_user):
        return jsonify({
             'message': "user deleted ",
         }), 200
    else:
        return jsonify({'error': "No user found with the given ID!"}), 404
    



