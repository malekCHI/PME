from Factures.models import FactureModel
from db import db

#def get_all_factures():
#    return {'facture': list(map(lambda x: x.serialize(), FactureModel.query.all()))}

 
#def get_facture(_id_facture):
#    return {'facture': list(map(lambda x: x.serialize(), FactureModel.query.filter_by(id_facture=_id_facture).first()))}

def get_all_factures():
    factures = FactureModel.query.all()
    return [facture.serialize() for facture in factures]

def get_facture(_id):
    facture = FactureModel.query.get(_id)
    if facture:
        return facture.serialize()
    return {'message': 'facture not found.'}, 404

def create_facture(id_facture, TypeFacture,date_emission,description, prix_ht,prix_forfitaire,prix_jour, nbr_jour,prix_livrable,total,tva, total_ttc):
    facture = FactureModel(id_facture=id_facture, TypeFacture=TypeFacture,date_emission=date_emission,description=description,prix_ht=prix_ht,prix_forfitaire=prix_forfitaire,prix_jour=prix_jour,nbr_jour=nbr_jour,prix_livrable=prix_livrable,total=total,tva=tva,total_ttc=total_ttc)
    db.session.add(facture)
    db.session.commit()
    return 
    

def update_facture(_id_facture, TypeFacture,date_emission,description, prix_ht,prix_forfitaire,prix_jour, nbr_jour,prix_livrable,total,tva, total_ttc):
    facture = FactureModel.query.get(_id_facture)
    if facture:
        facture._id_facture = _id_facture,
        facture.TypeFacture = TypeFacture,
        facture.date_emission = date_emission,
        facture.description=description, 
        facture.prix_ht=prix_ht,
        facture.prix_forfitaire=prix_forfitaire,
        facture.prix_jour=prix_jour,
        facture.nbr_jour=nbr_jour,
        facture.prix_livrable=prix_livrable,
        facture.total=total,
        facture.tva=tva, 
        facture.total_ttc=total_ttc,
        db.session.commit()
        return {'message': 'facture updated successfully.'}
    return {'message': 'facture not found.'}, 404

def delete_facture(_id):
    facture = FactureModel.query.get(_id)
    if facture:
        db.session.delete(facture)
        db.session.commit()
        return {'message': 'facture deleted successfully.'}
    return {'message': 'facture not found.'}, 404

def get_factures_by_type(TypeFacture):
    factures = FactureModel.query.filter_by(TypeFacture=TypeFacture).all()
    return [facture.serialize() for facture in factures]

