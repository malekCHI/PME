from datetime import datetime
from Factures.models import FactureModel
from .models import PaiementModel
from db import db
from sqlalchemy import Enum as EnumSQL
from enum import Enum


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



def add_paiement(montant,id_facture, date_paiement):
    # Créer une nouvelle instance de PaiementModel avec les données fournies
    nouveau_paiement = PaiementModel(montant=montant,id_facture=id_facture, date_paiement=date_paiement)

    # Calculer le statut du paiement en fonction du montant
    if montant == 0:
        # Si le montant du paiement est égal à zéro, le statut est "NON_PAYEE"
        nouveau_paiement.statut = "NON_PAYEE"
    else:
        # Sinon, le montant du paiement est positif, donc le statut est "PAYEE"
        nouveau_paiement.statut = "PAYEE"

    nouveau_paiement.save_to_db()

    return {"message": "Le paiement a été ajouté avec succès"}
