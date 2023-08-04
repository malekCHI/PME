from db import db
from datetime import datetime

class RelanceModel(db.Model):
    __tablename__ = "relance"
    id_relance = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Relation Many-to-One avec la table "FactureModel"
    id_facture = db.Column(db.Integer, db.ForeignKey('facture.id_facture'), nullable=False)
    date_relance = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    message = db.Column(db.String(200), nullable=False)


    # Relation One-to-Many avec la table "RelanceModel"
    #relances = db.relationship("RelanceModel", backref="facture", lazy=True)
    # Relation Many-to-One avec la table "FactureModel" avec le paramètre overlaps
    #facture_relance = db.relationship("FactureModel", backref="relances", overlaps="facture")

    def __init__(self, id_facture, date_relance, message):
        self.id_facture = id_facture
        self.date_relance = date_relance
        self.message = message

    def serialize(self):
        data = {
            "id_relance": self.id_relance,
            "id_facture": self.id_facture,
            "date_relance": self.date_relance.strftime("%Y-%m-%d %H:%M:%S"),
            "message": self.message,
        }
        return data

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()