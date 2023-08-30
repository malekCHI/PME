from db import db
from datetime import datetime
from Paiement.models import PaiementModel
from Client.models import ClientModel
from Factures.models import FactureModel

class ChiffreDaffaires(db.Model):
    __tablename__ = 'chiffre_daffaires'
    id = db.Column(db.Integer, primary_key=True)
    id_facture = db.Column(db.Integer, db.ForeignKey ("facture.id_facture"))
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id_client"))
    paiement_id = db.Column(db.Integer, db.ForeignKey("paiement.id_paiement"))
    date_emission = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    periode = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    client = db.Column(db.String, nullable=False)
    montant_facture = db.Column(db.Float, nullable=False)
    montant_paye = db.Column(db.Float, nullable=False)
    status_facture = db.Column(db.String, nullable=False)
    total_facture = db.Column(db.Float, nullable=False)
    total_paye = db.Column(db.Float, nullable=False)
    total_du = db.Column(db.Float, nullable=False)

    # relationships
    facture_rel = db.relationship('FactureModel', backref='chiffres_daffaires', lazy=True)
    client_rel = db.relationship('ClientModel', backref='chiffres_daffaires', lazy=True)
    paiement_rel = db.relationship('PaiementModel', backref='chiffres_daffaires', lazy=True)

    def __init__(self, facture_rel, client_rel, paiement_rel):
        self.facture_rel = facture_rel
        self.client_rel = client_rel
        self.paiement_rel = paiement_rel

        self.client = client_rel.nom
        self.montant_facture = facture_rel.total_ttc
        self.montant_paye = paiement_rel.montant
        self.status_facture = paiement_rel.status
        self.total_facture = facture_rel.total_ttc
        self.total_paye = paiement_rel.montant
        self.total_du = facture_rel.total_ttc - paiement_rel.montant

    def serialize(self):
        return {
            'id': self.id,
            'periode': self.periode.strftime('%Y-%m-%d %H:%M:%S'),
            'date_emission': self.date_emission.strftime('%Y-%m-%d %H:%M:%S'),
            'id_facture': self.id_facture,
            'client': self.client,
            'montant_facture': self.montant_facture,
            'montant_paye': self.montant_paye,
            'status_facture': self.status_facture,
            'total_facture': self.total_facture,
            'total_paye': self.total_paye,
            'total_du': self.total_du,
        }
