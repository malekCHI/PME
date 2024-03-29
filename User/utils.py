from functools import wraps
from flask import app, request,jsonify
import jwt
import time
import uuid
from werkzeug.security import generate_password_hash
from User.models import UserModel
import flask_jwt_extended 
import random
import string
from mail import mail
import secrets
from flask_mail import Message


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if 'x-access-tokens' not in request.headers:
            return jsonify({'message': 'A valid token is missing'}), 401

        token = request.headers['x-access-tokens']

        try:
            data = flask_jwt_extended.decode_token(token)
            current_user = UserModel.query.get(data['identity']['id_user'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
        except Exception as e:
            return jsonify({'message': 'Error decoding token: {}'.format(str(e))}), 401

        return f(current_user, *args, **kwargs)
    return decorator
    # def decorator(*args, **kwargs):
    #     token = request.headers['x-access-tokens']
    #     if not token:
    #        return jsonify({'message': 'a valid token is missing'})
       
    #     if 'x-access-tokens' in request.headers:
    #        token = request.headers['x-access-tokens']
    #        print(token)
    #        try:
    #             data = flask_jwt_extended.decode_token(token)
    #             print(data)
    #             current_user = UserModel.query.filter_by(id_user=data['identity']['id_user']).first()
    #        except:
    #             return jsonify({'message': 'token is invalid'})
 
    #     return f(current_user, *args, **kwargs)
    # return decorator

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
        # Update the password hash if provided
        if _password_hash:
            hashed_password = generate_password_hash(_password_hash, method='sha256')
            user_to_update.password_hash = hashed_password
        user_to_update.save_to_db()
        return True
    return False
   
def delete_user(_id_user):
    user_delete=UserModel.query.filter_by(id_user=_id_user).first()
    if user_delete:
        user_delete.delete_from_db() 
        return True
    return False      
    
    
def generate_random_password():
    password_length = 10
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(password_length))


def generate_reset_token():
    token = secrets.token_urlsafe(32)  # Generate a 32-character URL-safe token
    return token
    
def send_reset_email(user_email, reset_token):
    subject = 'Password Reset Request'
    body = f'Click the link below to reset your password:\n\n' \
           f'http://your-app-url/reset_password/{reset_token}'
    message = Message(subject=subject, recipients=[user_email], body=body)
    mail.send(message)
    