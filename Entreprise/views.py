from flask import Blueprint, request, jsonify, render_template
from flask_jwt_extended import  jwt_required,get_jwt_identity
from Entreprise.models import Entreprise
from Entreprise.utils import add_entreprise,update_entreprise,delete_entreprise
import re

from User.utils import token_required
# from User.models import UserModel
entreprise = Blueprint("entreprise", __name__, url_prefix="/entreprise")


@entreprise.post("/create")
def create_entreprise():
    data = request.get_json()
    nom = data.get('nom', '')
    adresse = data.get('adresse', '')
    description = data.get('description', '')
    email = data.get('email', '')
    tel = data.get('tel', '')
    color = data.get('color', '')
    if not (nom and adresse):
        return jsonify({"error": "Please enter valid name and adresse!"}), 400
    if Entreprise.query.filter_by(nom=nom).first() is not None:
        return jsonify({"error": "Entreprise already exist!"}), 409
    if len(email) > 50:
        return jsonify({
            "error": "Email must be less than 50 characters!"
         }),400
    if tel is not None and not str(tel).isdigit():
        return jsonify({
        "error": "Invalid tel format. Tel must be an integer."
    }), 400
    if re.search(r'\d', nom):
        return jsonify({
           "error": "Invalid nom format. Numbers are not allowed in the nom"
         }),400
    if '@' not in email or 'com' not in email:
        return jsonify({
            "error": 'Invalid email format. Email must contain "@" and "com"'
         }),400
    add_entreprise(nom, adresse, description,email,tel,color)
    return jsonify({
         'message': "Entreprise created",
     }), 201


@entreprise.put("/update/<int:_id_Entreprise>")
def edit_entreprise(_id_Entreprise):
    data = request.get_json()
    _nom = data.get('nom', '')
    _adresse = data.get('adresse', '')
    _description = data.get('description', '')
    _email = data.get('email', '')
    _tel = data.get('tel', '')
    _color = data.get('color', '')
    if not (_id_Entreprise and _nom ):
        return jsonify({
            "error": "Please enter a valid ID and  name!"
         }), 400

    if update_entreprise(_id_Entreprise, _nom, _adresse, _description,_email,_tel,_color):
        return jsonify({
             'message': "Entreprise updated",
         }), 200
    else:
        return jsonify({"error": "No Entreprise found with the given ID!"}), 404


@entreprise.get('/get_entreprise')
@jwt_required()
def get_entreprisee():
    user_id = get_jwt_identity()
    print(user_id)
    pages = request.args.get('page')
    per_page = 10
    id_Entreprise = request.args.get('id_Entreprise')
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
        return jsonify({"error": "Please enter a valid ID!"}), 400
    if delete_entreprise(_id_Entreprise):
        return (
            jsonify(
                {
                    "message": "Entreprise deleted ",
                }
            ),
            200,
        )
    else:
        return jsonify({"error": "No Entreprise found with the given ID!"}), 404


@entreprise.route("/upload-image/<int:id_Entreprise>", methods=["GET", "POST"])
def upload_image(id_Entreprise):
    entreprise = Entreprise.query.get(id_Entreprise)
    if request.method == "POST":
        file = request.files["image"]
        # Gérer l'enregistrement du fichier, par exemple en utilisant une librairie comme Flask-Uploads
        # Assurez-vous d'ajouter la logique appropriée pour enregistrer le chemin du fichier dans votre modèle Entreprise
        if file:
            # Exemple d'enregistrement de fichier
            # file.save("chemin/vers/repertoire/" + file.filename)
            # entreprise.logo_path = "chemin/vers/repertoire/" + file.filename
            # entreprise.save()  # Sauvegarder les modifications dans la base de données
            return jsonify({"message": "Image uploaded successfully."}), 200
        else:
            return jsonify({"error": "No file provided."}), 400
    return render_template("upload_image.html", entreprise=entreprise)
