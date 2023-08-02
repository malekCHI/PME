from db import db
from datetime import datetime
class Entreprise (db.Model):
    __tablename__ = 'entreprise'
    id_Entreprise = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    adresse = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    tel = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(100), nullable=False)

    
    def __repr__(self):
        return f'<Entreprise {self.nom}>'

    def __init__(self,nom,adresse,description,email,tel,color):
        self.nom = nom
        self.adresse = adresse
        self.description = description
        self.email=email
        self.tel=tel
        self.color=color

    def serialize(self):
            return {
                'id_Entreprise': self.id_Entreprise,
                'nom': self.nom,
                'adresse': self.adresse, 
                'description': self.description, 
                'email': self.email, 
                'tel': self.tel,
                'color': self.color
                }
            
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

