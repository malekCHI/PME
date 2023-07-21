from flask import Blueprint, request, jsonify
from flask_jwt_extended import current_user
from Entreprise.models import Entreprise
from Entreprise.utils import add_entreprise,update_entreprise,delete_entreprise
import re

from User.utils import token_required
entreprise = Blueprint("entreprise", __name__, url_prefix="/entreprise")


@entreprise.post('/create')
def create_entreprise():
    nom = request.json.get('nom', '')
    adresse = request.json.get('adresse', '')
    description = request.json.get('description', '')
    email = request.json.get('email', '')
    tel = request.json.get('tel', '')
    id_user=request.json.get('id_user', '')
    if not id_user:
        return 'User not found', 400
    if len(adresse) > 10:
            return jsonify({
            "error": "adresse must be less than 10 characters!"
         }),400
    if not (nom and adresse):
        return jsonify({
            "error": "Please enter valid name and adresse!"
         }), 400
    if Entreprise.query.filter_by(nom=nom).first() is not None:
        return jsonify({'error': "Entreprise already exist!"}), 409
    if len(email) > 50:
        return jsonify({
            "error": "Email must be less than 50 characters!"
         }),400
    if re.search(r'\d', email):
        return jsonify({
           "error": "Invalid email format. Numbers are not allowed in the email"
         }),400
    if '@' not in email or 'com' not in email:
        return jsonify({
            "error": 'Invalid email format. Email must contain "@" and "com"'
         }),400
    add_entreprise(nom, adresse, description,email,tel,id_user)
    return jsonify({
         'message': "Entreprise created",
     }), 201

@entreprise.put('/update/<int:_id_Entreprise>')
def edit_entreprise(_id_Entreprise):
    _nom = request.json.get('nom', '')
    _adresse = request.json.get('adresse', '')
    _description = request.json.get('description', '')
    _creation_date = request.json.get('creation_date', '')
    _email = request.json.get('email', '')
    _tel = request.json.get('tel', '')
    _id_user = request.json.get('id_user', '')
    if not (_id_Entreprise and _nom ):
        return jsonify({
            "error": "Please enter a valid ID and  name!"
         }), 400

    if update_entreprise(_id_Entreprise, _nom, _adresse, _description,_creation_date,_email,_tel,_id_user):
        return jsonify({
             'message': "Entreprise updated",
         }), 200
    else:
        return jsonify({'error': "No Entreprise found with the given ID!"}), 404


@entreprise.get('/get_entreprise')
# @token_required
def get_entreprise():
    # print(current_user.id_user)
    # curentuser = Entreprise.query.filter_by(user_id=current_user.id_user)
    pages = request.args.get('page')
    per_page = 10
    id_Entreprise = request.args.get('id_Entreprise')
    # if curentuser:
    if not pages:
        if id_Entreprise:
            return {'entreprise': list(map(lambda x: x.serialize(), Entreprise.query.filter_by(id_Entreprise=id_Entreprise)))}
        else:
            return {'entreprises': list(map(lambda x: x.serialize(), Entreprise.query.all()))}
    else:
        page = int(pages)
        if id_Entreprise:
            return {'entreprise': list(map(lambda x: x.serialize(), Entreprise.query.filter_by(id_Entreprise=id_Entreprise).paginate(page, per_page, error_out=False).items))}
        else:
            return {'entreprises': list(map(lambda x: x.serialize(), Entreprise.query.paginate(page, per_page, error_out=False).items))}

 
@entreprise.delete('/delete/<int:_id_Entreprise>')
def remove_entreprise(_id_Entreprise):
    if not (_id_Entreprise):
            return jsonify({
            "error": "Please enter a valid ID!"
         }), 400
    if delete_entreprise(_id_Entreprise):
        return jsonify({
             'message': "Entreprise deleted ",
         }), 200
    else:
        return jsonify({'error': "No Entreprise found with the given ID!"}), 404