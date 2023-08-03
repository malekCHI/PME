from db import db
from datetime import datetime

class ChiffreDaffaires(db.Model):
    __tablename__ = 'Chiffre d\'affaires'
    id = db.Column(db.Integer, primary_key=True)
    date_emission = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    date_fin = db.Column(db.DateTime,default=datetime.utcnow, nullable=False)
    id_facture = db.Column(db.Integer, nullable=False)
    client = db.Column(db.String, nullable=False)
    montant_facture = db.Column(db.Float, nullable=False)
    montant_paye = db.Column(db.Float, nullable = False)
    status_facture = db.Column(db.String, nullable = False)
    total_facture = db.Column(db.Float,nullable = False)
    total_paye = db.Column(db.Float,nullable = False)
    total_du = db.Column(db.Float, nullable = False)

    def serialize(self):
        data={ 
            'id': self.id,
            'date_emission': self.date_emission.strftime('%Y-%m-%d %H:%M:%S'),
            'date_fin': self.date_fin.strftime('%Y-%m-%d %H:%M:%S'),
            'id_facture':self.id_facture,
            'client':self.client,
            'montant_facture':self.montant_facture,
            'montant_paye':self.montant_paye,
            'status_facture':self.status_facture,
            'total_facture':self.total_facture,
            'total_paye':self.total_paye,
            'total_du':self.du,

        }
        return data