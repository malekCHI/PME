from flask import Blueprint, request, jsonify
from Entreprise.models import Entreprise
from Entreprise.utils import get_all_Entreprises, get_entreprise
from Entreprise.utils import add_entreprise, update_entreprise, delete_entreprise
import re
from flask_sqlalchemy import paginate


entreprise = Blueprint("entreprise", __name__, url_prefix="/entreprise")


@entreprise.post("/create")
def create_entreprise():
    nom = request.json.get("nom", "")
    adresse = request.json.get("adresse", "")
    description = request.json.get("description", "")
    email = request.json.get("email", "")
    tel = request.json.get("tel", "")
    logo_path = request.files.get("logo")

    if len(adresse) > 10:
        return jsonify({"error": "adresse must be less than 10 characters!"}), 400
    if not (nom and adresse):
        return jsonify({"error": "Please enter valid name and adresse!"}), 400
    if Entreprise.query.filter_by(nom=nom).first() is not None:
        return jsonify({"error": "Entreprise already exist!"}), 409
    if len(email) > 50:
        return jsonify({"error": "Email must be less than 50 characters!"}), 400
    if re.search(r"\d", email):
        return (
            jsonify(
                {"error": "Invalid email format. Numbers are not allowed in the email"}
            ),
            400,
        )
    if "@" not in email or "com" not in email:
        return (
            jsonify(
                {"error": 'Invalid email format. Email must contain "@" and "com"'}
            ),
            400,
        )
    add_entreprise(nom, adresse, description, email, tel, logo_path)
    return (
        jsonify(
            {
                "message": "Entreprise created",
            }
        ),
        201,
    )


@entreprise.put("/update/<int:_id_Entreprise>")
def edit_entreprise(_id_Entreprise):
    
    _nom = request.json.get("nom", "")
    _adresse = request.json.get("adresse", "")
    _description = request.json.get("description", "")
    _creation_date = request.json.get("creation_date", "")
    _email = request.json.get("email", "")
    _tel = request.json.get("tel", "")
    # logo
    _logo_path = request.files.get("logo")

    if not (_id_Entreprise and _nom):
        return jsonify({"error": "Please enter a valid ID and  name!"}), 400

    if update_entreprise(
        _id_Entreprise, _nom, _adresse, _description, _creation_date, _email, _tel
    ):
        return (
            jsonify(
                {
                    "message": "Entreprise updated",
                }
            ),
            200,
        )
    else:
        return jsonify({"error": "No Entreprise found with the given ID!"}), 404


@entreprise.get("/get_entreprise")
def get_entreprise():
    pages = request.args.get("page")
    per_page = 10
    id = request.args.get("entreprise_id")

    if not pages:
        if id:
            return jsonify({"entreprise": get_entreprise()})
        else:
            return jsonify({"entreprises": get_all_Entreprises()})
    else:
        page = int(pages)
        if id:
            return jsonify(
                {
                    "entreprise": get_entreprise()
                    .paginate(page, per_page, error_out=False)
                    .items
                }
            )
        else:
            return jsonify(
                {
                    "entreprises": get_all_Entreprises()
                    .paginate(page, per_page, error_out=False)
                    .items
                }
            )


@entreprise.delete("/delete/<int:_id_Entreprise>")
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
