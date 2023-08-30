from flask import Blueprint, request, jsonify
from Factures.utils import get_all_factures, get_facture, create_facture, update_facture, delete_facture, get_factures_by_type, find_total_factures_count, count_waiting_factures_util, calculate_total_ttc_non_payee_partiellement, update_validation, count_late_factures, sum_of_total_ttc_for_late_factures
from Paiement.utils import calculate_etat_paiement
from Factures.models import FactureModel, typeFacture
from db import db
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


# @facture.get('/factures_awaiting_payment')
# def get_factures_awaiting_payment_count():
#     try:
#         count = find_factures_awaiting_payment_count()
#         if count is not None:
#             return jsonify({"status": "success", "count": count}), 200
#         else:
#             return jsonify({"status": "failure", "message": "Could not get the count"}), 500
#     except Exception as e:
#         return jsonify({"status": "failure", "message": str(e)}), 500
@facture.get('/count_waiting_factures')
def count_waiting_factures():
    count = count_waiting_factures_util()
    return jsonify({"count": count})


@facture.get("/total_factures_count")
def get_total_factures_count():
    """
    Endpoint to get the total number of factures in the database.
    """
    try:
        # Find the total number of factures
        total_factures_count = find_total_factures_count()

        if total_factures_count is not None:
            return jsonify({
                "statut": "success",
                "total_factures_count": total_factures_count
            }), 200
        else:
            return jsonify({"statut": "failure", "message": "Could not calculate the total number of factures."}), 500
    except Exception as e:
        return jsonify({"statut": "failure", "message": str(e)}), 500


@facture.get('/late_factures_count')
def late_factures_count_route():
    count = count_late_factures()
    return jsonify({"late_factures_count": count}), 200


@facture.get('/NON_VALIDE')
def count_non_valide_factures():
    count = FactureModel.query.filter_by(validation='NON_VALIDE').count()
    return jsonify({'count_non_valide_factures': count}), 200


@facture.get('/non_regularisee')
def get_total_ttc_non_payee_partiellement():
    try:
        total_ttc_value = calculate_total_ttc_non_payee_partiellement()
        return jsonify({"statut": "success", "total_ttc_non_payee_partiellement": total_ttc_value})
    except Exception as e:
        return jsonify({"statut": "failure", "message": str(e)}), 500


@facture.post('/ajouter')
def create():
    data = request.get_json()
    _id_facture = data.get("id_facture")
    id_client = data.get("id_client")
    TypeFacture = data.get("TypeFacture")
    date_emission = data.get("date_emission")
    descriptions = data.get("descriptions")
    total = data.get("total")
    tva = data.get("tva")
    total_ttc = data.get("total_ttc")
    statut = data.get("statut")
    validation = data.get("validation")
    date_fin = data.get("date_fin")

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
            descriptions_data = [
                {'tache': desc.get('tache')} for desc in descriptions]

    id_facture = create_facture(
        id_facture=_id_facture,
        id_client=id_client,
        TypeFacture=TypeFacture,
        date_emission=date_emission,
        descriptions=descriptions_data,
        total=total,
        tva=tva,
        total_ttc=total_ttc,
        statut=statut,
        validation=validation,
        date_fin=date_fin


    )

    return {'Message': f'Facture {id_facture} crée !'}, 201


@facture.get('/sum_of_total_ttc_for_late_factures')
def sum_of_total_ttc_route():
    total_ttc_sum = sum_of_total_ttc_for_late_factures()
    return jsonify({"sum_of_total_ttc": total_ttc_sum}), 200


@facture.post('/validate_facture')
def validate_facture():
    data = request.get_json()
    id_facture = data['id_facture']
    validation = data['validation']

    message, status_code = update_validation(id_facture, validation)
    return jsonify({'message': message}), status_code


@facture.put('/<int:_id>')
def update(_id):
    data = request.get_json()

    # Extract data from the request JSON
    TypeFacture = data.get("TypeFacture")
    id_client = data.get("id_client")
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
        id_client=id_client,
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
