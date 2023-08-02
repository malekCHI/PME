from flask import Blueprint, jsonify, request
from .models import RelanceModel
from Factures.models import FactureModel
from .utils import send_email
from datetime import datetime, timedelta
import threading
from Client.models import ClientModel


relance = Blueprint("relance", __name__, url_prefix="/relance")


@relance.get("/")
def get_all():
    relances = RelanceModel.query.all()
    return jsonify(relances=[relance.serialize() for relance in relances])


@relance.post("/create")
def create_relance():
    data = request.get_json()
    id_facture = data.get("id_facture")
    date_relance = data.get("date_relance")
    message = data.get("message")
    

    if not (id_facture and date_relance and message):
        return {"error": "Please provide id_facture, date_relance, and message."}, 400

    try:
        # Convertir la date_relance en objet datetime
        date_relance = datetime.strptime(date_relance, "%Y-%m-%d %H:%M:%S")

        # Calculate the date for sending the reminder email (5 days after date_relance)
        reminder_date = date_relance + timedelta(seconds=1)

        relance = RelanceModel(
            id_facture=id_facture, date_relance=date_relance, message=message
        )
        relance.save_to_db()
        # Planifier l'envoi de l'e-mail après 1 seconde
        threading.Timer(1, send_email, args=[to_email, "Relance de paiement", "Bonjour, vous avez une facture en attente de paiement."]).start()
        return {
            "message": "Relance created successfully.",
            "reminder_date": reminder_date.strftime("%Y-%m-%d %H:%M:%S"),
        }, 201
    except Exception as e:
        return {
            "message": "An error occurred while creating the relance.",
            "error": str(e),
        }, 500
