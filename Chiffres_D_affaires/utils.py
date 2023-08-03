from Chiffres_D_affaires.models import ChiffreDaffaires
from datetime import datetime
from db import db

def filter_by_clients():
    clients = ChiffreDaffaires.query.all()
    return [client.serialize() for client in clients]

def filter_by_client():
    client = ChiffreDaffaires.query.get(id)
    if client:
        return client.serialize()
    return {'Message': 'Client non trouvée !'}, 404

def filter_by_period(date_emission, date_fin):
    if isinstance(date_emission, str):
        date_emission = datetime.strptime(date_emission, '%Y-%m-%d').date()
    if isinstance(date_fin, str):
        date_fin = datetime.strptime(date_fin, '%Y-%m-%d').date()
    clients = ChiffreDaffaires.query.filter(ChiffreDaffaires.date >= date_emission, ChiffreDaffaires.date <= date_fin).all()
    return [client.serialize() for client in clients]


def generate_cda(id ,date_emission,periode,id_facture,client ,montant_facture ,montant_paye,status_facture ,total_facture,total_paye,total_du):
   cda = ChiffreDaffaires(

    )
   
    db.session.add(cda)
    db.session.commit()
    return 

def 