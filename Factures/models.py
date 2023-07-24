from db import db
from datetime import datetime
from enum import Enum

class TypeFacture(Enum):
    FORFAIT = 'FORFAIT'
    JOUR_HOMME = 'JOUR_HOMME'
    LIVRABLES = 'LIVRABLES'


class FactureModel(db.Model):
    __tablename__ = 'facture'
    id_facture = db.Column(db.Integer, primary_key=True)
    date_emission = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    description = db.Column(db.String(100), nullable=False)
    prix_ht = db.Column(db.Float, nullable=False)
    TypeFacture = db.Column(db.Enum(TypeFacture), nullable=True)
    prix_forfaitaire = db.Column(db.Float, nullable=True)
    prix_jour = db.Column(db.Float, nullable=True)
    nbr_jour = db.Column(db.Integer, nullable=True)
    prix_livrable = db.Column(db.Float, nullable=True)
    total = db.Column(db.Float, nullable=False)
    tva = db.Column(db.Float, nullable=False)
    total_ttc = db.Column(db.Float, nullable=False)

    def serialize(self):
        data = {
            'id_facture': self.id_facture,
            'date_emission': self.date_emission.strftime('%Y-%m-%d %H:%M:%S'),
            'description':self.description,
            'prix_ht':self.prix_ht,
            'TypeFacture': self.TypeFacture.value if self.TypeFacture else None,
            'prix_forfaitaire':self.prix_forfaitaire,
            'prix_jour':self.prix_jour,
            'nbr_jour':self.nbr_jour,
            'prix_livrable':self.prix_livrable,
            'total': self.total,
            'tva': self.tva,
            'total_ttc':self.total_ttc,
            }
        return data

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

# class ForfaitModel(db.Model):
#     __tablename__ = 'forfaitaire'
#     id_facture= db.Column(db.Integer, primary_key=True)
#     TypeFacture = db.Column(db.Enum(TypeFacture), nullable=True)
#     date_emission = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
#     description = db.Column(db.String(100), nullable=False)
#     prix_ht = db.Column(db.Float, nullable=False)
#     prix_forfaitaire = db.Column(db.Float, nullable=True)
#     total = db.Column(db.Float, nullable=False)
#     tva = db.Column(db.Float, nullable=False)
#     total_ttc = db.Column(db.Float, nullable=False)
    

#     def serialize(self):
#         data = {
#             'id_facture': self.id,
#             'TypeFacture': self.TypeFacture,
#             'date_emission': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
#             'description':self.description,
#             'prix_ht':self.prix_ht,
#             'prix_forfaitaire':self.prix_forfaitaire,
#             'total': self.total,
#             'tva': self.tva,
#             'total_ttc':self.total_ttc,
#             }
#         return data
#     def save_to_db(self):
#         db.session.add(self)
#         db.session.commit()

#     def delete_from_db(self):
#         db.session.delete(self)
#         db.session.commit()
# class JourHommeModel(db.Model):
#     __tablename__= 'Jour_Homme'
#     id_facture = db.Column(db.Integer,primary_key=True)
#     date_emission = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
#     description = db.Column(db.String(100), nullable=False)
#     prix_ht = db.Column(db.Float, nullable=False)
#     TypeFacture = db.Column(db.Enum(TypeFacture), nullable=True)
#     prix_jour = db.Column(db.Float, nullable=True)
#     nbr_jour = db.Column(db.Integer, nullable=True)
#     total = db.Column(db.Float, nullable=False)
#     tva = db.Column(db.Float, nullable=False)
#     total_ttc = db.Column(db.Float, nullable=False)
#     def serialize(self):
#          data = {
#         'id_facture':self.id,
#         'TypeFacture': self.TypeFacture,
#         'date_emission': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
#         'description':self.description,
#         'prix_ht':self.prix_ht,
#         'prix_forfaitaire':self.prix_forfaitaire,
#         'total': self.total,
#         'tva': self.tva,
#         'total_ttc':self.total_ttc,
          
#      }
#          return data
#     def save_to_db(self):
#         db.session.add(self)
#         db.session.commit()

#     def delete_from_db(self):
#         db.session.delete(self)
#         db.session.commit()
# class LivrableModel(db.Model):
#     __tablename__ = 'Livrables'
#     id_facture=db.Column(db.Integer, primary_key=True)
#     date_emission = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
#     description = db.Column(db.String(100), nullable=False)
#     prix_ht = db.Column(db.Float, nullable=False)
#     TypeFacture = db.Column(db.Enum(TypeFacture), nullable=True)
#     total = db.Column(db.Float, nullable=False)
#     tva = db.Column(db.Float, nullable=False)
#     total_ttc = db.Column(db.Float, nullable=False)
#     prix_livrable = db.Column(db.Float, nullable=True)
#     def serialize(self):
#         data = {
#             'id_facture':self.id,
#             'TypeFacture': self.TypeFacture,
#             'date_emission': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
#             'description':self.description,
#             'prix_ht':self.prix_ht,
#             'prix_livrable':self.prix_livrable,
#             'total': self.total,
#             'tva': self.tva,
#             'total_ttc':self.total_ttc,
          
#         }
#         return data
    # def save_to_db(self):
    #     db.session.add(self)
    #     db.session.commit()

    # def delete_from_db(self):
    #     db.session.delete(self)
    #     db.session.commit()

#
 #def serialize(self):
#        if self.TypeFacture == TypeFacture.FORFAIT:
#            data = {
#                'Prix ht': self.prix_ht,
#                'Prix forfaitaire ht': self.prix_forfaitaire,
#                'Description': self.description,
#                'Total': self.total,
#               'TVA': self.tva,
#                'Total TTC': self.total_ttc,
 #               'Date': self.date_emission.strftime('%Y-%m-%d %H:%M:%S')
 #           }
  #      elif self.TypeFacture == TypeFacture.JOUR_HOMME:
  #          data= { 
  #              'Prix ht': self.prix_ht,
   #             'Description': self.description,
    #            'Total': self.total,
    #            'TVA': self.tva,
    #            'Total TTC': self.total_ttc,
    #            'Date': self.date_emission.strftime('%Y-%m-%d %H:%M:%S'),
    #            'nbr_jour': self.nbr_jour,
    #            'prix_jour':self.prix_jour,
    #    }
     #   elif self.TypeFacture == TypeFacture.LIVRABLES:
      #      data={
       #         'Prix ht': self.prix_ht,
        #        'Prix livrable': self.prix_livrable,
         #       'Description': self.description,
          #      'Total': self.total,
           #     'TVA': self.tva,
            #    'Total TTC': self.total_ttc,
             #   'Date': self.date_emission.strftime('%Y-%m-%d %H:%M:%S')
            #} return data
            
 #


