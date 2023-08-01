from flask import Blueprint, request, jsonify
from Factures.utils import get_all_factures, get_facture, create_facture, update_facture, delete_facture, get_factures_by_type

facture = Blueprint("facture", __name__, url_prefix="/facture")

@facture.get('/')
def get_all():
    return jsonify(factures=get_all_factures())

@facture.get('/<int:_id>')
def get_by_id(_id):
    facture = get_facture(_id)
    if isinstance(facture, dict) and 'Message' in facture:
        return jsonify(facture), 404
    return jsonify(facture=facture)

# @facture.post('/<int:facture_id>/add_taches')
# def add_taches(facture_id):
#     data = request.get_json()
#     taches = data.get('taches', [])
#     result = add_taches_to_facture(facture_id, taches)
#     return jsonify(result)
@facture.post('/ajouter')
def create():
    data = request.get_json()
    _id_facture = data.get("id_facture")
    TypeFacture = data.get("TypeFacture")
    date_emission = data.get("date_emission")
    descriptions = data.get("descriptions")
    total = data.get("total")
    tva = data.get("tva")
    total_ttc = data.get("total_ttc")

    if not (_id_facture and TypeFacture):
        return {'Erreur': 'Veuillez fournir ID, Type du facture et les taches !'}, 400

    descriptions_data = []
    if descriptions:
        if TypeFacture == 'FORFAIT':
            for desc in descriptions:
                tache_data = {
                    'tache': desc.get('tache'),
                    'prix_ht': desc.get('prix_ht'),
                    'prix_forfaitaire': desc.get('prix_forfaitaire_ht'),
                }
                descriptions_data.append(tache_data)
        elif TypeFacture == 'JOUR_HOMME':
            for desc in descriptions:
                tache_data = {
                    'tache': desc.get('tache'),
                    'prix_ht': desc.get('prix_ht'),
                    'nbr_jour': desc.get('nbr_jour'),
                    'prix_jour': desc.get('prix_jour'),
                }
                descriptions_data.append(tache_data)
        elif TypeFacture == 'LIVRABLES':
            for desc in descriptions:
                tache_data = {
                    'tache': desc.get('tache'),
                    'prix_ht': desc.get('prix_ht'),
                    'prix_livrable': desc.get('prix_livrable'),
                }
                descriptions_data.append(tache_data)
        else:
            descriptions_data = [{'tache': desc.get('tache')} for desc in descriptions]

    id_facture = create_facture(
        id_facture=_id_facture,
        TypeFacture=TypeFacture,
        date_emission=date_emission,
        descriptions=descriptions_data,
        total=total,
        tva=tva,
        total_ttc=total_ttc,
    )
    
    return {'Message': f'Facture {id_facture} créée !'}, 201

@facture.put('/<int:_id>')
def update(_id):
    data = request.get_json()

    # Extract data from the request JSON
    TypeFacture = data.get("TypeFacture")
    date_emission = data.get("date_emission")
    total = data.get("total")
    tva = data.get("tva")
    total_ttc = data.get("total_ttc")

    # Check if all data is provided
    if not (TypeFacture and date_emission and total and tva and total_ttc):
        return {'Erreur': 'Veuillez fournir les informations complètes !'}, 400

    # Extract descriptions data from the request JSON and apply the enum conditions
    descriptions_data = []
    if 'descriptions' in data:
        for desc in data['descriptions']:
            tache_data = {
                'tache': desc.get('tache'),
                'prix_ht': desc.get('prix_ht')
            }

            # Apply the enum conditions
            if TypeFacture == 'FORFAIT':
                tache_data.update({
                    'prix_forfaitaire_ht': desc.get('prix_forfaitaire_ht'),
                    'prix_livrable': None,
                    'nbr_jour': None,
                    'prix_jour': None
                })
            elif TypeFacture == 'JOUR_HOMME':
                tache_data.update({
                    'prix_forfaitaire_ht': None,
                    'prix_livrable': None,
                    'nbr_jour': desc.get('nbr_jour'),
                    'prix_jour': desc.get('prix_jour')
                })
            elif TypeFacture == 'LIVRABLES':
                tache_data.update({
                    'prix_forfaitaire_ht': None,
                    'nbr_jour': None,
                    'prix_jour': None,
                    'prix_livrable': desc.get('prix_livrable')
                })

            descriptions_data.append(tache_data)

    # Call the update_facture function with the extracted data and _id parameter
    update_message = update_facture(
        _id_facture=_id,
        TypeFacture=TypeFacture,
        date_emission=date_emission,
        descriptions=descriptions_data,
        total=total,
        tva=tva,
        total_ttc=total_ttc,
    )

    if update_message:
        return {'Message': 'Facture mise à jour avec succès !'}, 200
    return {'Message': 'Facture non trouvée !'}, 404



@facture.get('/type/<string:facture_type>')
def get_by_type(facture_type):
    factures = get_factures_by_type(facture_type)
    return jsonify(factures=factures)

@facture.delete('/<int:_id>')
def delete(_id):
    if delete_facture(_id):
        return {'Message': 'Facture supprimée avec succès !'}, 200
    return {'Message': 'Facture non trouvée !'}, 404



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




