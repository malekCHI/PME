from db import db
from datetime import datetime

#profile_previlege= db.Table('profile_previlege',
    #db.Column('profile_id',db.Integer,db.ForeignKey('profiles.id')),
   # db.Column('previlege_id',db.Integer,db.ForeignKey('previlege.id'))
#)

class ProfileModel(db.Model):
    """ Profile model """
    __tablename__ = "profiles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True,  nullable=False)
    description = db.Column(db.String())
    creation_date = db.Column(db.DateTime, default=datetime.utcnow) 
    #users = db.relationship('UserModel', lazy='dynamic', backref="profiles")
    #previleges = db.relationship('PrevilegeModel', secondary=profile_previlege, lazy='dynamic', backref=db.backref('profiles', lazy='dynamic'))
    
    def __init__(self, name, description):
        self.name = name
        self.description = description
        

    def serialize(self):
            return {
                'id': self.id,
                'name': self.name,
                'previleges': [act.serialize() for act in self.previleges.all()],
                'creation_date': self.creation_date.strftime("%d-%b-%Y"),
                'description': self.description,
                }


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
