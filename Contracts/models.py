from db import db
from sqlalchemy import Column, Integer, String, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from Client.models import ClientModel


class ContractModel(db.Model):
    """Modèle de contrat"""

    __tablename__ = "contracts"

    id_contract = db.Column(Integer, primary_key=True)
    id_client = db.Column(Integer, ForeignKey("clients.id_client"))

    date_debut = db.Column(db.Date, nullable=False)
    date_fin = db.Column(db.Date, nullable=False)
    conditions_financieres = db.Column(String, nullable=False)
    prochaine_action = db.Column(String, nullable=True)
    date_prochaine_action = db.Column(db.Date, nullable=True)
    date_rappel = db.Column(db.Date, nullable=True)
    fichier_pdf = db.Column(String, nullable=True)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)

    client = relationship("ClientModel", backref="contracts")

    def __init__(
        self,
        id_client,
        date_debut,
        date_fin,
        conditions_financieres,
        prochaine_action=None,
        date_prochaine_action=None,
        date_rappel=None,
        fichier_pdf=None,
    ):
        self.id_client = id_client
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.conditions_financieres = conditions_financieres
        self.prochaine_action = prochaine_action
        self.date_prochaine_action = date_prochaine_action
        self.date_rappel = date_rappel
        self.fichier_pdf = fichier_pdf

    def serialize(self):
        return {
            "id_contract": self.id_contract,
            "id_client": self.id_client,
            "date_debut": self.date_debut.strftime("%Y-%m-%d"),
            "date_fin": self.date_fin.strftime("%Y-%m-%d"),
            "conditions_financieres": self.conditions_financieres,
            "prochaine_action": self.prochaine_action,
            "date_prochaine_action": self.date_prochaine_action.strftime("%Y-%m-%d")
            if self.date_prochaine_action
            else None,
            "date_rappel": self.date_rappel.strftime("%Y-%m-%d")
            if self.date_rappel
            else None,
            "fichier_pdf": self.fichier_pdf,
            "creation_date": self.creation_date.strftime("%Y-%m-%d %H:%M:%S"),

        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
