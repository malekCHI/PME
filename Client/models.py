from db import db
from sqlalchemy import Column, Integer, String, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship

class ClientModel(db.Model):
    """Client model"""

    __tablename__ = "clients"
    id_client = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(), unique=True, nullable=False)
    adresse = db.Column(db.String(), nullable=False)
    contact = db.Column(db.String(), nullable=False)
    # clé etranger
    id_Entreprise = db.Column(Integer, ForeignKey("entreprise.id_Entreprise"))
    frequence_relance = db.Column(db.String(), nullable=False)
    email_destinataire = db.Column(db.String(), nullable=False)
    email_copies = db.Column(db.String(), nullable=False)

    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    # Relation Many-to-One avec la table "Entreprise"
    entreprise = relationship("Entreprise", backref="client")  # Modifiez "entreprise" en "Entreprise"
 
    # Relation One-to-Many avec la table "facture"
    #factures_relance = db.relationship("FactureModel", backref="client", lazy=True)
 
    def __init__(
        self,
       
        nom,
        adresse,
        contact,
        id_Entreprise,
        frequence_relance,
        email_destinataire,
        email_copies,
    ):
        
        self.nom = nom
        self.adresse = adresse
        self.contact = contact
        self.id_Entreprise = id_Entreprise
        self.frequence_relance = frequence_relance
        self.email_destinataire = email_destinataire
        self.email_copies = email_copies

    def serialize(self):
        return {
            "id_client":self.id_client,
            "nom": self.nom,
            "adresse": self.adresse,
            "contact": self.contact,
            "id_Entreprise": self.id_Entreprise,
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
