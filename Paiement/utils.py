from datetime import datetime
from Factures.models import FactureModel
from .models import PaiementModel
from db import db
from sqlalchemy import Enum as EnumSQL
from enum import Enum

from sqlalchemy import func


last_accessed_month = None
cached_total = 0.0


def calculate_total_paid_current_month():
    global last_accessed_month
    global cached_total

    # Get the current date and time
    current_time = datetime.utcnow()

    # Get the current month and year
    current_month = current_time.month
    current_year = current_time.year

    # Check if the month has changed since the last access
    if last_accessed_month != current_month:
        # Reset the cached total and update the last accessed month
        cached_total = 0.0
        last_accessed_month = current_month

        # Create a datetime object representing the first day of the current month
        first_day_of_month = datetime(current_year, current_month, 1)

        # Filter and sum the 'montant' from PaiementModel for the current month
        total_this_month = db.session.query(func.sum(PaiementModel.montant))\
                                     .filter(PaiementModel.date_paiement >= first_day_of_month)\
                                     .scalar()

        # Update the cached total if the query returns a non-null value
        if total_this_month is not None:
            cached_total = total_this_month

    return cached_total
# Énumération pour les différents statuts de paiement


class TypeStatut(Enum):
    PAYEE = "PAYEE"
    NON_PAYEE = "NON_PAYEE"
    PAYEE_PARTIELLEMENT = "PAYEE_PARTIELLEMENT"


def get_all_paiements():
    return {"paiements": list(map(lambda x: x.serialize(), PaiementModel.query.all()))}


def get_paiements_by_facture(id_facture):
    return {
        "paiements": list(
            map(
                lambda x: x.serialize(),
                PaiementModel.query.filter_by(id_facture=id_facture).all(),
            )
        )
    }


def calculate_etat_paiement(facture):
    montant_total = facture.total_ttc
    montant_paye = sum(paiement.montant for paiement in facture.paiements)

    if montant_paye == 0:
        return TypeStatut.NON_PAYEE
    elif montant_paye < montant_total:
        return TypeStatut.PAYEE_PARTIELLEMENT
    elif montant_total == montant_paye:
        return TypeStatut.PAYEE
    else:
        return None  # or raise an exception if needed


def add_paiement(montant, id_facture, date_paiement):
    # Créer une nouvelle instance de PaiementModel avec les données fournies
    nouveau_paiement = PaiementModel(
        montant=montant, id_facture=id_facture, date_paiement=date_paiement)

    # Calculer le statut du paiement en fonction du montant
    if montant == 0:
        # Si le montant du paiement est égal à zéro, le statut est "NON_PAYEE"
        nouveau_paiement.statut = "NON_PAYEE"
    else:
        # Sinon, le montant du paiement est positif, donc le statut est "PAYEE"
        nouveau_paiement.statut = "PAYEE"

    nouveau_paiement.save_to_db()

    return {"message": "Le paiement a été ajouté avec succès"}
