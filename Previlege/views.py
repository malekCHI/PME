from flask import Blueprint,request,jsonify
from Previlege.models import PrevilegeModel
from Profile.models import ProfileModel
from Previlege.utils import add_previlege,update_previlege,delete_previlege
from db import db
previlege = Blueprint("previlege", __name__, url_prefix="/previlege")

@previlege.post('/create')
def create_previlege():
    data = request.get_json()
    nom = data.get('nom', '')
    description = data.get('description', '')
    creation_date = data.get('creation_date', '')
    profiles = data.get('profiles', [])
    if len(description) < 10:
            return jsonify({
            "error": "description must be less than 10 characters!"
         }),400
    if not (nom and description):
        return jsonify({
            "error": "Please enter valid name and description!"
         }), 400
    if PrevilegeModel.query.filter_by(nom=nom).first() is not None:
        return jsonify({'error': "Profile already exist!"}), 409

    add_previlege(nom,description,creation_date,profiles)
    return jsonify({
         'message': "previlege created",
     }), 201

@previlege.get('/')
def get_previlege():
    pages = request.args.get('page')
    per_page = 10
    id_previlege = request.args.get('id_previlege')

    if not pages:
        if id_previlege:
            return {'previlege': list(map(lambda x: x.serialize(), PrevilegeModel.query.filter_by(id_previlege=id_previlege)))}
        else:
            return {'previleges': list(map(lambda x: x.serialize(), PrevilegeModel.query.all()))}
    else:
        page = int(pages)
        if id_previlege:
            return {'previlege': list(map(lambda x: x.serialize(), PrevilegeModel.query.filter_by(id_previlege=id_previlege).paginate(page, per_page, error_out=False).items))}
        else:
            return {'previleges': list(map(lambda x: x.serialize(), PrevilegeModel.query.paginate(page, per_page, error_out=False).items))}


@previlege.put('/update/<int:_id_previlege>')
def edit_previlege(_id_previlege):
    data = request.get_json()
    _nom = data.get('nom', '')
    _description = data.get('description', '')
    _creation_date = data.get('creation_date', '')

    if not (_id_previlege and _nom ):
        return jsonify({
            "error": "Please enter a valid ID and  name!"
         }), 400

    if update_previlege(_id_previlege, _nom, _description,_creation_date):
        return jsonify({
             'message': "previlege updated",
         }), 200
    else:
        return jsonify({'error': "No previlege found with the given ID!"}), 404


@previlege.delete('/delete/<int:_id_previlege>')
def remove_previlege(_id_previlege):
    if not (_id_previlege):
            return jsonify({
            "error": "Please enter a valid ID!"
         }), 400
    if delete_previlege(_id_previlege):
        return jsonify({
             'message': "previlege deleted ",
         }), 200
    else:
        return jsonify({'error': "No previlege found with the given ID!"}), 404
    
    
    
            
@previlege.post('/assign_privileges_to_profile')
def assign_privileges_to_profile():
    try:
        data = request.get_json()
        id_previlege = data.get('id_previlege', '')
        profiles = data.get('profiles', [])
        previlege = PrevilegeModel.query.get(id_previlege)
        if not previlege:
            return 'previlege not found', 404
        # Fetchi profiles by id 
        profiles = ProfileModel.query.filter(ProfileModel.id_profile.in_(profiles)).all()
        # Assign the previlege to the list of profiles
        previlege.profiles.extend(profiles)    
        print(previlege)
        # Commit changes 
        db.session.commit()
        return 'previlege assigned to privileges successfully', 200
    except Exception as e:
        db.session.rollback()
        return str(e), 500