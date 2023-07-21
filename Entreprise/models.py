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
    creation_date = db.Column(db.DateTime, default=datetime.utcnow,nullable=True) 
    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user'))

    
    def __repr__(self):
        return f'<Entreprise {self.nom}>'

    def __init__(self,nom,adresse,description,email,tel,id_user):
        self.nom = nom
        self.adresse = adresse
        self.description = description
        self.email=email
        self.tel=tel
        self.id_user=id_user

    def serialize(self):
            return {
                'id_Entreprise': self.id_Entreprise,
                'nom': self.nom,
                'adresse': self.adresse, 
                'description': self.description, 
                'email': self.email, 
                'tel': self.tel, 
                'creation_date':self.creation_date.strftime('%Y-%m-%d'),
                'id_user':self.id_user
                }
            
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

