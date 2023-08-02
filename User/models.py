from db import db
from datetime import datetime

#class user 
class UserModel(db.Model):
    __tablename__ = "user"
    id_user = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(), unique=False,  nullable=False)
    prenom = db.Column(db.String(), unique=False,  nullable=False) 
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.Text,nullable=True)
    description = db.Column(db.String(),nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow) 
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id_profile'))
    profile = db.relationship("ProfileModel")
    previleges = db.relationship("PrevilegeModel", secondary="user_previlege", back_populates="users")
    def __init__(self,nom,prenom,email,password_hash,description,profile_id,previleges=None):
        self.nom = nom
        self.prenom = prenom      
        self.email = email
        self.password_hash = password_hash
        self.description = description
        self.profile_id = profile_id 
        self.previleges = []        
        
    def serialize(self,visited=None):
        visited = visited or set()
        if self in visited:
            return {'id_user': self.id_user}

        visited.add(self)
        return {
                'id_user': self.id_user,
                'nom': self.nom,
                'prenom': self.prenom,
                'email': self.email,
                'password_hash': self.password_hash,
                'description': self.description,
                'creation_date': self.creation_date.strftime("%d-%b-%Y"),
                'profile_id': self.profile_id,
                'previleges': list(map(lambda previlege: previlege.serialize(visited), self.previleges)),
                }


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class user_previlege(db.Model):
    __tablename__ = 'user_previlege'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id_user'), primary_key=True)
    previlege_id = db.Column(db.Integer, db.ForeignKey('previlege.id_previlege'), primary_key=True)