from db import db
from sqlalchemy import Column, Integer, String, ForeignKey
from datetime import datetime


class ClientModel(db.Model):
    """Client model"""

    __tablename__ = "clients"
    id_client = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(), unique=True, nullable=False)
    adresse = db.Column(db.String(), nullable=False)
    contact = db.Column(db.String(), nullable=False)
    # entreprise_id = db.Column(db.Integer, db.ForeignKey("entreprises.id_entreprise"))
    frequence_relance = db.Column(db.String(), nullable=False)
    email_destinataire = db.Column(db.String(), nullable=False)
    email_copies = db.Column(db.String(), nullable=False)

    creation_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(
        self,
        nom,
        adresse,
        contact,
        frequence_relance,
        email_destinataire,
        email_copies,
    ):
        self.nom = nom
        self.adresse = adresse
        self.contact = contact
        # self.entreprise_id = entreprise_id
        self.frequence_relance = frequence_relance
        self.email_destinataire = email_destinataire
        self.email_copies = email_copies

    def serialize(self):
        return {
            "nom": self.nom,
            "adresse": self.adresse,
            "contact": self.contact,
            # "entreprise_id": self.entreprise_id,
            "frequence_relance": self.frequence_relance,
            "email_destinataire": self.email_destinataire,
            "email_copies": self.email_copies,
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
