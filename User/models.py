from db import db
from datetime import datetime
from enum import Enum

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
    profile = db.relationship("ProfileModel", backref="associated_users")
    previleges = db.relationship("PrevilegeModel", secondary="user_previlege",lazy='dynamic',backref=db.backref('users_previlege', lazy='dynamic'))
    
    def __init__(self,nom,prenom,email,description,password_hash,creaation_date,profile_id):
        self.nom = nom
        self.prenom = prenom      
        self.email = email
        self.description = description
        self.password_hash = password_hash
        self.creation_date = creaation_date
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
                'profile_id': self.profile_id,
                'previleges': [act.serialize() for act in self.previleges.all()],

                }

#class profile 
   
class ProfileModel(db.Model):
    __tablename__ = "profiles"
    id_profile = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(), unique=True,  nullable=False)
    description = db.Column(db.String())
    creation_date = db.Column(db.DateTime, default=datetime.utcnow) 
    users = db.relationship('UserModel', backref="user_profile")
    previleges = db.relationship("PrevilegeModel", secondary="profile_previlege",lazy='dynamic',backref=db.backref('profiles_previlege', lazy='dynamic'))
    #user_id = db.Column(db.Integer,db.ForeignKey('user.id_user'))
    #users = db.relationship('UserModel', lazy='dynamic', backref="profiles")
    #previleges = db.relationship('PrevilegeModel', secondary=profile_previlege, lazy='dynamic', backref=db.backref('profiles', lazy='dynamic'))
    
    def __init__(self,nom,description,creation_date):
        self.nom = nom
        self.description = description
        self.creation_date = creation_date
    
    def serialize(self):
            return {
                'id_profile': self.id_profile,
                'nom': self.nom,
                'description': self.description,
                'creation_date': self.creation_date.strftime("%d-%b-%Y"),
                'users': [act.serialize() for act in self.users.all()],
                #It appears to be  related to a model previleges , the resulting serialized objects are stored in a list
                'previleges': [act.serialize() for act in self.previleges.all()],

                }

# join many to many 
profile_previlege= db.Table('profile_previlege',
    db.Column('id_profile',db.Integer,db.ForeignKey('profiles.id_profile')),
    db.Column('id_previlege',db.Integer,db.ForeignKey('previlege.id_previlege'))
)
#join many to many
user_previlege= db.Table('user_previlege',
    db.Column('id_user',db.Integer,db.ForeignKey('user.id_user')),
    db.Column('id_previlege',db.Integer,db.ForeignKey('previlege.id_previlege'))
)


#class previlege 
class PrevilegeModel(db.Model):
    __tablename__ = "previlege"
    id_previlege = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(), unique=True,  nullable=False)
    description = db.Column(db.String())
    creation_date = db.Column(db.DateTime, default=datetime.utcnow) 
    profiles = db.relationship("ProfileModel", secondary="profile_previlege",lazy='dynamic',backref=db.backref('previleges_profil', lazy='dynamic'))
    users = db.relationship("UserModel", secondary="user_previlege",lazy='dynamic',backref=db.backref('previleges_user', lazy='dynamic'))

    def __init__(self,nom,description,creation_date,profiles):
        self.nom = nom
        self.description = description
        self.creation_date = creation_date
        self.profiles = profiles
    
    def serialize(self):
            return {
                'id_previlege': self.id_previlege,
                'nom': self.nom,
                'description': self.description,
                'creation_date': self.creation_date.strftime("%d-%b-%Y"),
                'users': [act.serialize() for act in self.users.all()],
                'profiles': [act.serialize() for act in self.profiles.all()],

                }



    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
