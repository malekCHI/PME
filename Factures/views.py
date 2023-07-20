from flask import Blueprint, request, jsonify
from Factures.utils import get_all_factures, get_facture,create_facture, update_facture, delete_facture, get_factures_by_type 

from Factures.models import FactureModel,TypeFacture


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
    prix_forfaitaire= data.get("prix_forfaitaire")
    prix_jour= data.get("prix_jour")  
    nbr_jour= data.get("nbr_jour")
    prix_livrable= data.get("prix_livrable") 
    total = data.get("total")
    tva = data.get("tva")
    total_ttc =data.get ("total_ttc")

    if not (_id_facture and TypeFacture):
        return {'error': 'Please provide id_facture, and TypeFacture.'}, 400

    id_facture = create_facture(_id_facture, TypeFacture, date_emission, description, prix_ht, prix_forfaitaire, prix_jour, nbr_jour, prix_livrable, total, tva, total_ttc)

    
    return {'message': (f'Facture {id_facture} créée')}, 201

# @facture.post('/FORFAIT')
# def forfaitaire():
#     data = request.get_json()
#     _id_facture = data.get("id_facture")
#     TypeFacture = data.get("TypeFacture") # Assuming FORFAIT is the desired TypeFacture value
#     date_emission = data.get("date_emission")
#     description = data.get("description")
#     prix_ht = data.get("prix_ht")
#     prix_forfaitaire = data.get("prix_forfaitaire")
#     total = data.get("total")
#     tva = data.get("tva")
#     total_ttc = data.get("total_ttc")
    
#     if not _id_facture:
#         return {'Error': 'Insérer un ID de facture forfaitaire !'}, 400
    
#     id_facture = forfaitaire (id_facture,date_emission,description, prix_ht,TypeFacture,prix_forfaitaire,total, tva, total_ttc)
    
#     if id_facture:
#         return {'message': 'Facture forfaitaire créée !'}, 201
    
#     return {'message': 'Failed to create facture.'}, 500

# @facture.post('/jour_homme')
# def jour_homme():
#     data = request.get_json()
#     _id_facture = data.get("id_facture")
#     # TypeFacture = TypeFacture.JOUR_HOMME  # Assuming JOUR_HOMME is the desired TypeFacture value
#     date_emission = data.get("date_emission")
#     description = data.get("description")
#     prix_ht = data.get("prix_ht")
#     nbr_jour = data.get("nbr_jour")
#     prix_jour = data.get("prix_jour")
#     total = data.get("total")
#     tva = data.get("tva")
#     total_ttc = data.get("total_ttc")
    
#     if not _id_facture:
#         return {'Error': 'Insérer un ID de facture jour/homme !'}, 400
    
#     id_facture = jour_homme(_id_facture, date_emission, description, prix_ht, nbr_jour, prix_jour, total, tva, total_ttc)
    
#     if id_facture:
#         return {'message': 'Facture jour/homme créée !'}, 201
    
#     return {'message': 'Failed to create facture.'}, 500


# @facture.post('/livrables')
# def livrables():
#     data = request.get_json()
#     _id_facture = data.get("id_facture")
#     TypeFacture = data.get("TypeFacture") # Assuming LIVRABLES is the desired TypeFacture value
#     date_emission = data.get("date_emission")
#     description = data.get("description")
#     prix_ht = data.get("prix_ht")
#     prix_livrable = data.get("prix_livrable")
#     total = data.get("total")
#     tva = data.get("tva")
#     total_ttc = data.get("total_ttc")
    
#     if not _id_facture:
#         return {'Error': 'Insérer un ID de facture livrable !'}, 400
    
#     id_facture = livrables(_id_facture, TypeFacture, date_emission, description, prix_ht, prix_livrable, total, tva, total_ttc)
    
#     if id_facture:
#         return {'message': 'Facture livrable créée !'}, 201
    
#     return {'message': 'Failed to create facture.'}, 500




@facture.put('/<int:_id>')
def update(id_facture, TypeFacture, date_emission, description, prix_ht,prix_forfaitaire,prix_jour, nbr_jour, prix_livrable, total, tva, total_ttc):
    data = request.get_json()
    
    id_facture = data.get("id_facture")
    TypeFacture = data.get("TypeFacture")
    date_emission = data.get("date_emission")
    description= data.get("description")
    prix_ht=data.get("prix_ht")
    prix_forfaitaire = data.get("prix_forfaitaire")
    prix_jour= data.get("prix_jour")
    nbr_jour= data.get("nbr_jour")
    prix_livrable = data.get("prix_livrable")
    total= data.get("total")
    tva= data.get("tva")
    total_ttc=data.get("total_ttc")


    if not (id_facture,TypeFacture,date_emission,description,prix_ht,prix_forfaitaire, prix_jour,nbr_jour,prix_livrable, total,tva,total_ttc):
        return {'error': 'Provide full info.'}, 400

    if update_facture(id_facture, TypeFacture,date_emission,description, prix_ht,prix_forfaitaire,prix_jour, nbr_jour,prix_livrable,total,tva, total_ttc):
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