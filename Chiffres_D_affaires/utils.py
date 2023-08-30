from Chiffres_D_affaires.models import ChiffreDaffaires
from Factures.models import FactureModel
from Client.models import ClientModel
from Paiement.models import PaiementModel
from datetime import datetime
from db import db
from sqlalchemy import or_

def filter_by_clients():
    clients = ChiffreDaffaires.query.all()
    return [client.serialize() for client in clients]



def filter_by_client(client_name):
    clients = db.session.query(ChiffreDaffaires)\
        .join(ClientModel, ChiffreDaffaires.client_id == ClientModel.id_client)\
        .filter(or_(ClientModel.nom.ilike(f"%{client_name}%"))).all()
    
    if not clients:
        return {'Message': 'Client non trouvé !'}, 404
    return [client.serialize() for client in clients]


def filter_by_period(date_emission, date_fin):
    if isinstance(date_emission, str):
        date_emission = datetime.strptime(date_emission, '%Y-%m-%d').date()
    if isinstance(date_fin, str):
        date_fin = datetime.strptime(date_fin, '%Y-%m-%d').date()
    clients = ChiffreDaffaires.query.filter(ChiffreDaffaires.date_emission >= date_emission, ChiffreDaffaires.date_emission <= date_fin).all()
    return [client.serialize() for client in clients]

def generate_cda(id_facture, client_id, paiement_id):
    facture = FactureModel.query.get(id_facture)
    client = ClientModel.query.get(client_id)
    paiement = PaiementModel.query.get(paiement_id)
    if facture and client and paiement:
        cda = ChiffreDaffaires(facture_rel=facture, client_rel=client, paiement_rel=paiement)
        db.session.add(cda)
        db.session.commit()
        return cda.serialize()
    return {'Message': 'Facture, Client, or Paiement not found !'}, 404
