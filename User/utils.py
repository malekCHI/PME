from functools import wraps
from flask import app, request,jsonify
import jwt
import uuid
from werkzeug.security import generate_password_hash
from User.models import UserModel


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
       token = None
       if 'x-access-tokens' in request.headers:
           token = request.headers['x-access-tokens']
 
       if not token:
           return jsonify({'message': 'a valid token is missing'})
       try:
           data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
           current_user = UserModel.query.filter_by(id_user=data['id_user']).first()
       except:
           return jsonify({'message': 'token is invalid'})
 
       return f(current_user, *args, **kwargs)
    return decorator



def get_all_users():
    return {'users': list(map(lambda x: x.serialize(), UserModel.query.all()))}

 
def get_user(_id_user):
    return {'user': list(map(lambda x: x.serialize(), UserModel.query.filter_by(id_user=_id_user).first()))}


def add_user(nom, prenom, email,password_hash,description,profile_id):
    user = UserModel(nom=nom,prenom=prenom,email=email,password_hash=password_hash,description=description,profile_id=profile_id) 
    user.save_to_db()
    
    
def update_user(_id_user, _nom, _prenom, _email,_password_hash,_description,_profile_id):
    user_to_update = UserModel.query.filter_by(id_user=_id_user).first()
    if user_to_update:
        user_to_update.nom = _nom
        user_to_update.prenom = _prenom
        user_to_update.email = _email
        user_to_update.password_hash = _password_hash
        user_to_update.description = _description
        user_to_update.profile_id = _profile_id
        user_to_update.save_to_db()
        return True
    return False
   
def delete_user(_id_user):
    user_delete=UserModel.query.filter_by(id_user=_id_user).first()
    if user_delete:
        user_delete.delete_from_db() 
        return True
    return False      
    