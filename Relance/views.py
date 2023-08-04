from flask import Blueprint, jsonify, request
from .models import RelanceModel
from Factures.models import FactureModel
from .utils import send_email, schedule_email
from datetime import datetime
from dateutil.parser import parse

relance = Blueprint("relance", __name__, url_prefix="/relance")

@relance.get("/")
def get_all():
    relances = RelanceModel.query.all()
    return jsonify(relances=[relance.serialize() for relance in relances])

@relance.post("/create")
def create_relance():
    try:
        data = request.get_json()
        id_facture = data.get("id_facture")
        date_relance = data.get("date_relance")
        message = data.get("message")

        if not (id_facture and date_relance and message):
            return {
                "error": "Please provide id_facture, date_relance, and message."
            }, 400

        # Convertir la date_relance en objet datetime
        date_relance = parse(date_relance)

        # Créer une nouvelle instance de RelanceModel
        relance = RelanceModel(
            id_facture=id_facture, date_relance=date_relance, message=message
        )
        relance.save_to_db()

        # Récupérer l'objet Facture associé à l'id_facture
        facture = FactureModel.query.get(id_facture)

        # Récupérer l'objet Client associé à la facture
        client = facture.client

        if client and client.email_destinataire:
            # Schedule the email sending task
            schedule_email(client.email_destinataire, "Relance de paiement", "Bonjour, vous avez une facture en attente de paiement.")

        return {
            "message": "Relance created successfully.",
        }, 201
    except Exception as e:
        return {
            "message": "An error occurred while creating the relance.",
            "error": str(e),
        }, 500