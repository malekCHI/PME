from Client.models import ClientModel
from Entreprise.models import Entreprise
from Client.utils import get_all_Clients, add_client, get_client, get_entreprise_by_id
from flask import Blueprint, request, jsonify
from db import db
# from flask_sqlalchemy import paginate
from Client.utils import get_entreprise_by_id


client = Blueprint("client", __name__, url_prefix="/client")


@client.post("/create")
def create_client():
    data = request.get_json()
    nom = data.get("nom")
    adresse = data.get("adresse")
    contact = data.get("contact")
    id_Entreprise = data.get("id_Entreprise")
    frequence_relance = data.get("frequence_relance")
    email_destinataire = data.get("email_destinataire")
    email_copies = data.get("email_copies")

    client = ClientModel(
        nom=nom,
        adresse=adresse,
        contact=contact,
        id_Entreprise=id_Entreprise,
        frequence_relance=frequence_relance,
        email_destinataire=email_destinataire,
        email_copies=email_copies,
    )
    client.save_to_db()

    return {"message": "Client added successfully"}


@client.get("/get_client")
def get_clients():
    pages = request.args.get("page")
    per_page = 10
    id_client = request.args.get("client_id")

    if not pages:
        if id_client:
            # Utilisez simplement get_client(id_client) pour obtenir le client par son ID
            client = get_client(id_client)
            if client:
                return jsonify({"client": client})
            else:
                return jsonify({"message": "Client not found"}), 404
        else:
            return jsonify({"clients": get_all_Clients()})
    else:
        page = int(pages)
        if id_client:
            return jsonify(
                {
                    "client": get_client(id_client)
                    .paginate(page, per_page, error_out=False)  # type: ignore
                    .items
                }
            )
        else:
            return jsonify(
                {
                    "clients": get_all_Clients()
                    .paginate(page, per_page, error_out=False)  # type: ignore
                    .items
                }
            )


@client.get("/get_entreprise_by_client_id/<int:id_client>")
def get_entreprise_by_client_id(id_client):
    client_data = get_client(id_client)
    if client_data:
        client = ClientModel.query.get(id_client)
        if client and client.entreprise:
            entreprise_name = client.entreprise.nom
            return jsonify({"entreprise_name": entreprise_name})
        else:
            return jsonify({"message": "Entreprise not found"}), 404
    else:
        return jsonify({"message": "Client not found"}), 404


@client.put("/update/<int:client_id>")
def update_client(client_id):
    data = request.get_json()
    nom = data.get("nom", "")
    adresse = data.get("adresse", "")
    contact = data.get("contact", "")
    id_Entreprise = data.get("id_Entreprise", "")
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
    client.id_Entreprise = id_Entreprise
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
                "id_Entreprise": client.id_Entreprise,
                "frequence_relance": client.frequence_relance,
                "email_destinataire": client.email_destinataire,
                "email_copies": client.email_copies,
            },
        }
    )
