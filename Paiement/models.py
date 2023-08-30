from db import db
from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship

from sqlalchemy import Enum as EnumSQL
from enum import Enum


# Modèle PaiementModel
class PaiementModel(db.Model):
    __tablename__ = "paiement"
    id_paiement = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Clé étrangère pour la relation One-to-Many avec la table FactureModel
    id_facture = db.Column(
        db.Integer, db.ForeignKey("facture.id_facture"), nullable=False
    )

    montant = db.Column(db.Float, nullable=False)
    date_paiement = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)

    def serialize(self):
        data = {
            "id_paiement": self.id_paiement,
            "id_facture": self.id_facture,
            "montant": self.montant,
            "date_paiement": self.date_paiement.strftime("%Y-%m-%d %H:%M:%S"),
        }
        return data

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
