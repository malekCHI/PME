from Client.models import ClientModel
from Client.utils import get_all_Clients, add_client
from flask import Blueprint, request, jsonify
from db import db

client = Blueprint("client", __name__, url_prefix="/client")


@client.post("/create")
def create_client():
    data = request.json
    nom = data.get("nom")
    adresse = data.get("adresse")
    contact = data.get("contact")
    frequence_relance = data.get("frequence_relance")
    email_destinataire = data.get("email_destinataire")
    email_copies = data.get("email_copies")

    add_client(
        nom=nom,
        adresse=adresse,
        contact=contact,
        frequence_relance=frequence_relance,
        email_destinataire=email_destinataire,
        email_copies=email_copies,
    )

    return {"message": "Client added successfully"}


@client.get("/get_client")
def get_client():
    pages = request.args.get("page")
    per_page = 10
    id_client = request.args.get("client_id")

    if not pages:
        if id_client:
            return jsonify({"client": get_client()})
        else:
            return jsonify({"client": get_all_Clients()})
    else:
        page = int(pages)
        if id_client:
            return jsonify(
                {"client": get_client().paginate(page, per_page, error_out=False).items}
            )
        else:
            return jsonify({"client": get_all_Clients().paginate(page, per_page, error_out=False).items})  # type: ignore


@client.put("/update/<int:client_id>")
def update_client(client_id):
    data = request.json
    nom = data.get("nom", "")
    adresse = data.get("adresse", "")
    contact = data.get("contact", "")
    frequence_relance = data.get("frequence_relance", "")
    email_destinataire = data.get("email_destinataire", "")
    email_copies = data.get("email_copies", "")

    if not (nom and adresse):
        return jsonify({"error": "Please enter valid name and address!"}), 400

    client = ClientModel.query.get(client_id)
    if client is None:
        return jsonify({"error": "Client not found!"}), 404

    client.nom = nom
    client.adresse = adresse
    client.contact = contact
    client.frequence_relance = frequence_relance
    client.email_destinataire = email_destinataire
    client.email_copies = email_copies

    # Enregistrer les modifications dans la base de données
    db.session.commit()

    return jsonify(
        {
            "message": "Client updated",
            "client": {
                "nom": client.nom,
                "adresse": client.adresse,
                "contact": client.contact,
                "frequence_relance": client.frequence_relance,
                "email_destinataire": client.email_destinataire,
                "email_copies": client.email_copies,
            },
        }
    )


# Usage: PUT /entreprise/update/123
# Request JSON body: {"nom": "New Name", "adresse": "New Address", "description": "New Description"}

# Usage: DELETE /entreprise/delete/123
