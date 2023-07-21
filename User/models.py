from db import db
from datetime import datetime

#class user 
class UserModel(db.Model):
    __tablename__ = "user"
    id_user = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(), unique=True,  nullable=False)
    prenom = db.Column(db.String(), unique=True,  nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    description = db.Column(db.String())
    creation_date = db.Column(db.DateTime, default=datetime.utcnow) 
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id_profile'))
    profile = db.relationship("ProfileModel")
    # previleges = db.relationship("PrevilegeModel", secondary="user_previlege",backref=db.backref('use_previ'))
    
    def __init__(self,nom,prenom,email,description,password_hash,profile_id ):
        self.nom = nom
        self.prenom = prenom      
        self.email = email
        self.description = description
        self.password_hash = password_hash
        self.profile_id = profile_id 
        
    def serialize(self):
            return {
                'id_user': self.id_user,
                'nom': self.nom,
                'prenom': self.prenom,
                'email': self.email,
                'password_hash': self.password_hash,
                'description': self.description,
                'creation_date': self.creation_date.strftime("%d-%b-%Y"),
                'profile_id': self.profile_id
                # 'previleges': [act.serialize() for act in self.previleges.all()],

                }


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
