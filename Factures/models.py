from db import db
from datetime import datetime
from enum import Enum
from Paiement.models import PaiementModel
from Client.models import ClientModel
from Relance.models import RelanceModel
class TypeFacture(Enum):
    FORFAIT = 'FORFAIT'
    JOUR_HOMME = 'JOUR_HOMME'
    LIVRABLES = 'LIVRABLES'

facture_description_association = db.Table('facture_description_association',
    db.Column('facture_id', db.Integer, db.ForeignKey('facture.id_facture')),
    db.Column('description_id', db.Integer, db.ForeignKey('descriptions.id'))
)

class FactureModel(db.Model):
    __tablename__ = 'facture'
    id_facture = db.Column(db.Integer, primary_key=True)
    date_emission = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    TypeFacture = db.Column(db.Enum(TypeFacture), nullable=True)
    descriptions = db.Column(db.String)
    total = db.Column(db.Float, nullable=False)
    tva = db.Column(db.Float, nullable=False)
    total_ttc = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(), nullable=False, default = " NON_PAYEE")
    id_client = db.Column(db.Integer, db.ForeignKey ("clients.id_client"))
    
    paiements = db.relationship('PaiementModel', backref = 'facture', lazy=True)
    
    # Relationship with DescriptionModel
    descriptions = db.relationship('DescriptionModel', secondary=facture_description_association, backref='factures')
    client = db.relationship('ClientModel',backref='facture',lazy=True)
    relances = db.relationship("RelanceModel", backref="facture",lazy=True)
    def serialize(self):
        data = {
            'id_facture': self.id_facture,
            'paiements':self.paiements,
            'client':self.client,
            'date_emission': self.date_emission.strftime('%Y-%m-%d %H:%M:%S'),
            'TypeFacture': self.TypeFacture.value if self.TypeFacture else None,
            'total': self.total,
            'tva': self.tva,
            'total_ttc': self.total_ttc,
            'status': self.status,
            'descriptions': [desc.serialize() for desc in self.descriptions], # type: ignore
            'status':self.status.value,
        }
        return data

class DescriptionModel(db.Model):
    __tablename__ = 'descriptions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tache = db.Column(db.String(100), nullable=False)
    prix_ht = db.Column(db.Float, nullable=True)
    prix_forfaitaire_ht = db.Column(db.Float, nullable=True)
    prix_livrable = db.Column(db.Float, nullable=True)
    nbr_jour = db.Column(db.Integer, nullable=True)
    prix_jour = db.Column(db.Float, nullable=True)

    def serialize(self):
        return {
            'id': self.id,
            'tache': self.tache,
            'prix_ht': self.prix_ht,
            'prix_forfaitaire_ht': self.prix_forfaitaire_ht,
            'prix_livrable': self.prix_livrable,
            'nbr_jour': self.nbr_jour,
            'prix_jour': self.prix_jour
        }


# {
#   "id_facture": 6,
#   "date_emission": "2023-07-17 00:00:00",
  
#   "TypeFacture": "JOUR_HOMME",
#   "total": 120,
#   "tva": 20,
#   "total_ttc": 140,
#   "descriptions": [
#     {
#       "id": 1,
#       "tache": "Tache 1",
#       "prix_ht": 50,
#       "prix_forfaitaire_ht": 50,
#       "prix_livrable":777,
#       "nbr_jour":777,
#       "prix_jour":777

#     },
#     {
#       "id": 2,
#       "tache": "Tache 2",
#       "prix_ht": 30,
#       "prix_forfaitaire_ht": 30,
#       "prix_livrable":777,
#       "nbr_jour":777,
#       "prix_jour":777
#     }
#   ]
# }






