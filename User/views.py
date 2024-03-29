from flask import Blueprint, request, jsonify,session
from User.models import UserModel
from Profile.models import ProfileModel
from Previlege.models import PrevilegeModel
from passlib.hash import bcrypt
import bcrypt
from sqlalchemy.exc import IntegrityError
from db import db
from flask_mail import Message
from mail import mail
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
import bcrypt
from User.utils import generate_reset_token,send_reset_email
from werkzeug.security import generate_password_hash,check_password_hash
from User.utils import add_user,update_user,delete_user,generate_random_password

profile = Blueprint("profile", __name__, url_prefix="/profile")
user = Blueprint("user", __name__, url_prefix="/users")


@user.post('/register')
def signup_user():
    try:
        data = request.get_json()
        print(request.json)
        nom = data.get('nom', None)
        prenom = data.get('prenom', None)
        email = data.get('email', None)
        description = data.get('description', None)
        profile_id = data.get('profile_id', None)
        # previleges = request.json.get('previleges', None)
        
        if not email:
            return 'Missing email', 400
        # Generate a random password for the user
        random_password  = generate_random_password()
        password_hashed =generate_password_hash(random_password, method='sha256')
        profile = ProfileModel.query.get(profile_id)
        if not profile:
            return 'Profile not found', 400
        add_user(nom, prenom, email,password_hashed, description, profile_id)  # Pass the password_hash
        # Send the confirmation email with the generated password
        recipients = [email]
        msg = Message(
            'SignUP Confirmation !',
            sender='malek.chiha@esprit.tn',
            recipients=recipients
        )
        msg.body = f'Hello {prenom} {nom},\n\nThank you for signing up on our plateforme! Your password is: {random_password}'

        mail.send(msg)

        return {"message": "User added successfully"}, 200
    except IntegrityError:
        # the rollback func reverts the changes made to the db
        db.session.rollback()
        return 'User Already Exists', 400
    except AttributeError:
        return 'Provide an Email and Password in JSON format in the request body', 400


@user.post('/login')
def login_user():
    try:
        data = request.get_json()
        print(request.json)
        email = data.get('email', None)
        password = data.get('password', None)
        
        if not email: 
            return 'Missing email', 400
        if not password:
            return 'Missing password', 400
        
        user = UserModel.query.filter_by(email=email).first()
        if not user:
            return 'User Not Found!', 404   
       # Check if the user is already logged in
        if 'email' in session and session['email'] == email:
            return {'message': 'You are already logged in', 'email': email}
        session['email'] = email
        print(f"Provided password: {password}")
        if check_password_hash(user.password_hash,password):
        # Verify the provided password
            access_token = create_access_token(identity={"id_user": user.id_user})
            return {"access_token": access_token,'email': email,'password': password}, 200
        else:
            return 'Invalid Login Info!', 400
    except AttributeError:
        return 'Provide an Email and Password in JSON format in the request body', 400
    
@user.get('/logout')
def logout():
	if 'email' in session:
		session.pop('email', None)
	return jsonify({'message' : 'You successfully logged out'})

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
    data = request.get_json()
    _nom = data.get('nom', None)
    _prenom = data.get('prenom', None)
    _email = data.get('email', None)
    _password_hash = data.get('password_hash', None)
    _description = data.get('description', None)
    _profile_id = data.get('profile_id', None)

    if not (_id_user and _nom ):
        return jsonify({
            "error": "Please enter a valid ID and  name!"
         }), 400
          
    if update_user(_id_user, _nom,_prenom,_email,_password_hash, _description,_profile_id):
        return jsonify({'message': "user updated",}), 200
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
    
@user.post('/assign_user_to_privileges')
def assign_user_to_privileges():
    data = request.get_json()
    try:
        user_id = data.get('id_user', '')
        previlege_id = data.get('previleges', [])
        
        user = UserModel.query.get(user_id)
        if not profile:
            return 'user not found', 404
        # Fetchi previleges by id 
        previleges = PrevilegeModel.query.filter(PrevilegeModel.id_previlege.in_(previlege_id)).all()
        # Assign the profile to the list of privileges
        user.previleges.extend(previleges)    
        print(user)
        # Commit changes 
        db.session.commit()
        return 'user assigned to privileges successfully', 200
    except Exception as e:
        db.session.rollback()
        return str(e), 500

@user.get("/currentuser")
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    return jsonify({
        "message": "successfully retrieved user profile",
        "data": user_id
    })
    
    
@user.post('/forgot_password')
def forgot_password():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Please provide your email address'}), 400

    # Check if the email belongs to a registered user
    user = UserModel.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Generate a reset token and save it in the user's record
    reset_token = generate_reset_token()
    user.reset_token = reset_token
    db.session.commit()

    # Send the reset token to the user's email
    send_reset_email(user.email, reset_token)

    return jsonify({'message': 'Password reset email sent successfully','reset_token':reset_token}), 200


@user.post('/reset_password/<reset_token>')
def reset_password(reset_token):
    data = request.get_json()
    password = data.get('password')

    if not password:
        return jsonify({'error': 'Please provide a new password'}), 400

    # Find the user by the reset token
    user = UserModel.query.filter_by(reset_token=reset_token).first()
    if not user:
        return jsonify({'error': 'Invalid reset token'}), 400

    # Reset the user's password and clear the reset token
    user.password_hash = generate_password_hash(password, method='sha256')
    user.reset_token = None
    db.session.commit()

    return jsonify({'message': 'Password reset successfully'}), 200