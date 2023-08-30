from db import db


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
