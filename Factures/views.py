from flask import Blueprint, request, jsonify
from Factures.utils import get_all_factures, get_facture, create_facture, update_facture, delete_facture, get_factures_by_type
from Factures.models import FactureModel


facture = Blueprint("facture", __name__, url_prefix="/facture")



@facture.get('/')
def get_all():
    return jsonify(factures=get_all_factures())

@facture.get('/<int:_id>')
def get_by_id(_id):
    facture = get_facture(_id)
    if facture:
        return jsonify(facture=facture)
    return {'message': 'facture not found.'}, 404

@facture.post('/ajouter')
def create():
    data = request.get_json()
    _id_facture = data.get("id_facture")
    TypeFacture = data.get("TypeFacture")
    date_emission =data.get("date_emission")
    description= data.get("description")
    prix_ht= data.get("prix_ht")
    prix_forfitaire= data.get("prix_forfitaire")
    prix_jour= data.get("prix_jour")  
    nbr_jour= data.get("nbr_jour")
    prix_livrable= data.get("prix_livrable") 
    total = data.get("total")
    tva = data.get("tva")
    total_ttc =data.get ("total_ttc")

    if not (_id_facture and TypeFacture):
        return {'error': 'Please provide id_facture, and TypeFacture.'}, 400

    id_facture = create_facture(_id_facture, TypeFacture,date_emission,description, prix_ht,prix_forfitaire,prix_jour, nbr_jour,prix_livrable,total,tva, total_ttc)
    
    return {'message': (f'Facture {id_facture} créée')}, 201

 
    

@facture.put('/<int:_id>')
def update(id_facture, TypeFacture, date_emission, description, prix_ht,prix_forfitaire,prix_jour, nbr_jour, prix_livrable, total, tva, total_ttc):
    data = request.get_json()
    
    id_facture = data.get("id_facture")
    TypeFacture = data.get("TypeFacture")
    date_emission = data.get("date_emission")
    description= data.get("description")
    prix_ht=data.get("prix_ht")
    prix_forfitaire = data.get("prix_forfitaire")
    prix_jour= data.get("prix_jour")
    nbr_jour= data.get("nbr_jour")
    prix_livrable = data.get("prix_livrable")
    total= data.get("total")
    tva= data.get("tva")
    total_ttc=data.get("total_ttc")


    if not (id_facture,TypeFacture,date_emission,description,prix_ht,prix_forfitaire, prix_jour,nbr_jour,prix_livrable, total,tva,total_ttc):
        return {'error': 'Provide full info.'}, 400

    if update_facture(id_facture, TypeFacture,date_emission,description, prix_ht,prix_forfitaire,prix_jour, nbr_jour,prix_livrable,total,tva, total_ttc):
        return {'message': 'facture updated successfully.'}, 200
    return {'message': 'facture not found.'}, 404

@facture.get('/type/<string:facture_type>')
def get_by_type(facture_type):
    factures = get_factures_by_type(facture_type)
    return jsonify(factures=factures)

@facture.delete('/<int:_id>')
def delete(_id):
    if delete_facture(_id):
        return {'message': 'facture deleted successfully.'}, 200
    return {'message': 'facture not found.'}, 404