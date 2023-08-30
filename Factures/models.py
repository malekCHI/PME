from db import db
from datetime import datetime
from enum import Enum
from Paiement.models import PaiementModel
from Client.models import ClientModel
from Relance.models import RelanceModel
from Factures.descriptions import DescriptionModel


class typeFacture(Enum):
    FORFAIT = 'FORFAIT'
    JOUR_HOMME = 'JOUR_HOMME'
    LIVRABLES = 'LIVRABLES'


facture_description_association = db.Table('facture_description_association',
                                           db.Column('facture_id', db.Integer, db.ForeignKey(
                                               'facture.id_facture')),
                                           db.Column('description_id', db.Integer, db.ForeignKey(
                                               'descriptions.id'))
                                           )


class FactureModel(db.Model):
    __tablename__ = 'facture'
    id_facture = db.Column(db.Integer, primary_key=True)
    date_emission = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=True)
    TypeFacture = db.Column(db.Enum(typeFacture), nullable=True)
    descriptions = db.Column(db.String)
    total = db.Column(db.Float, nullable=False)
    tva = db.Column(db.Float, nullable=False)
    total_ttc = db.Column(db.Float, nullable=False)
    statut = db.Column(db.String(), nullable=False, default=" NON_PAYEE")
    validation = db.Column(db.String(), nullable=False, default="NON_VALIDE")
    id_client = db.Column(db.Integer, db.ForeignKey("clients.id_client"))
    date_fin = db.Column(db.DateTime, nullable=False)
    paiements = db.relationship('PaiementModel', backref='facture', lazy=True)

    # Relationship with DescriptionModel
    descriptions = db.relationship(
        'DescriptionModel', secondary=facture_description_association, backref='factures')
    client = db.relationship('ClientModel', backref='facture', lazy=True)
    relances = db.relationship("RelanceModel", backref="facture", lazy=True)

    def __init__(
        self,
        id_facture,
        date_fin,
        date_emission,
        TypeFacture,
        descriptions,
        total,
        tva,
        total_ttc,
        statut,
        validation,
        id_client
    ):
        self.id_facture = id_facture
        self.date_emission = date_emission

        self.TypeFacture = TypeFacture
        self.descriptions = descriptions
        self.total = total
        self.total_ttc = total_ttc
        self.tva = tva
        self.statut = statut
        self.validation = validation
        self.id_client = id_client
        self.date_fin = date_fin

    def serialize(self):
        data = {
            'id_facture': self.id_facture,
            'paiements': self.paiements,
            'client': self.client,
            'validation': self.validation,
            'date_emission': self.date_emission.strftime('%Y-%m-%d %H:%M:%S'),
            'TypeFacture': self.TypeFacture.value if self.TypeFacture else None,
            'total': self.total,
            'tva': self.tva,
            'total_ttc': self.total_ttc,
            'statut': self.statut,


            # type: ignore
            'descriptions': [desc.serialize() for desc in self.descriptions],

        }
        return data
