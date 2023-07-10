from flask import Blueprint, request, jsonify
from User.models import ProfileModel


profile = Blueprint("profile", __name__, url_prefix="/profile")


@profile.post('/create')
def create_profile():

    name = request.json.get('name', '')
    description = request.json.get('description', '')

    if not (name and description):
        return jsonify({
            "error": "Please enter valid name and description!"
        }), 400

    if ProfileModel.query.filter_by(name=name).first() is not None:
        return jsonify({'error': "Profile already exist!"}), 409

    profile = ProfileModel(name=name, description=description)
    profile.save_to_db()
    return jsonify({
        'message': "profile created",
        'profile': profile.serialize()
    }), 201



@profile.get('/')
def get_profile():
    pages = request.args.get('page')
    per_page = 10
    id = request.args.get('profile_id')

    if not pages:
        if id:
            return {'profile': list(map(lambda x: x.serialize(), ProfileModel.query.filter_by(id=id)))}
        else:
            return {'profiles': list(map(lambda x: x.serialize(), ProfileModel.query.all()))}
    else:
        page = int(pages)
        if id:
            return {'profile': list(map(lambda x: x.serialize(), ProfileModel.query.filter_by(id=id).paginate(page, per_page, error_out=False).items))}
        else:
            return {'profiles': list(map(lambda x: x.serialize(), ProfileModel.query.paginate(page, per_page, error_out=False).items))}
