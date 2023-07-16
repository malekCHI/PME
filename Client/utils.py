from .models import ClientModel
from flask import request


def get_all_Clients():
    return {"client": list(map(lambda x: x.serialize(), ClientModel.query.all()))}


def get_client(_id_Client):
    return {
        "client": list(
            map(
                lambda x: x.serialize(),
                ClientModel.query.filter_by(id_client=_id_Client).first(),
            )
        )
    }


def is_valid_email(email):
    return "@" in email and email.endswith(".com")


def is_valid_string(value):
    return value is not None and isinstance(value, str) and value.strip() != ""


def add_client(
    nom, adresse, contact, frequence_relance, email_destinataire, email_copies
):
    if not is_valid_string(nom):
        return {"error": "Invalid name"}
    if not is_valid_string(adresse):
        return {"error": "Invalid address"}
    if not is_valid_string(contact):
        return {"error": "Invalid contact"}
    if not is_valid_string(frequence_relance):
        return {"error": "Invalid frequency of reminder"}
    if not is_valid_email(email_destinataire):
        return {"error": "Invalid destination email"}
    if not is_valid_email(email_copies):
        return {"error": "Invalid copied email"}
    client = ClientModel(
        nom=nom,
        adresse=adresse,
        contact=contact,
        frequence_relance=frequence_relance,
        email_destinataire=email_destinataire,
        email_copies=email_copies,
    )
    client.save_to_db()


def update_client(client_id):
    client = ClientModel.query.filter_by(id_client=client_id).first()
    if client:
        data = request.json
        client.nom = data.get("nom", client.nom)
        client.adresse = data.get("adresse", client.adresse)
        client.contact = data.get("contact", client.contact)
        client.frequence_relance = data.get(
            "frequence_relance", client.frequence_relance
        )
        client.email_destinataire = data.get(
            "email_destinataire", client.email_destinataire
        )
        client.email_copies = data.get("email_copies", client.email_copies)
        client.save_to_db()
        return {"message": "Client updated successfully"}
    else:
        return {"error": "Client not found"}
