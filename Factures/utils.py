from Factures.models import FactureModel, DescriptionModel
from Paiement.models import PaiementModel
from db import db
from datetime import datetime
from sqlalchemy import func
# def add_taches_to_facture(facture_id, taches):
#     facture = FactureModel.query.get(facture_id)
#     if facture:
#         for tache in taches:
#             new_tache = DescriptionModel(tache=tache)
#             db.session.add(new_tache)
#         db.session.commit()
#         return {'Message': f'Taches added to Facture {facture_id} successfully!'}
#     return {'Message': 'Facture not found!'}, 404


def get_all_factures(): return [facture.serialize()
                                for facture in FactureModel.query.all()]


# def find_factures_awaiting_payment_count():
#     try:
#         count = db.session.query(FactureModel).filter(
#             FactureModel.TypeFacture != 'PAYEE').count()
#         return count
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return None

def count_late_factures():
    current_time = datetime.utcnow()
    late_factures_count = db.session.query(FactureModel)\
        .filter(FactureModel.date_fin < current_time)\
        .filter(FactureModel.statut.in_([" NON_PAYEE", "PAYEE_PARTIELLEMENT"]))\
        .count()
    return late_factures_count


def find_total_factures_count():
    try:
        total_factures_count = FactureModel.query.count()
        return total_factures_count
    except Exception as e:
        return str(e)


def get_facture(_id):
    facture = FactureModel.query.get(_id)
    if facture:
        return facture.serialize()
    return {'Message': 'Facture non trouvée !'}, 404


def count_waiting_factures_util():
    # Count the number of 'factures' where statut is "NON_PAYEE" or "PAYEE_PARTIELLEMENT"
    return db.session.query(FactureModel).filter(
        FactureModel.statut.in_([" NON_PAYEE", "PAYEE_PARTIELLEMENT"])
    ).count()


def calculate_total_ttc_non_payee_partiellement():
    try:
        # Query the database to filter factures with statut "NON_PAYEE" or "PAYEE_PARTIELLEMENT"
        factures = FactureModel.query.filter(
            FactureModel.statut.in_([" NON_PAYEE", "PAYEE_PARTIELLEMENT"])
        ).all()

        # Calculate the total amount of total_ttc
        total_ttc_value = sum(facture.total_ttc for facture in factures)

        return total_ttc_value

    except Exception as e:
        raise e


def sum_of_total_ttc_for_late_factures():
    current_time = datetime.utcnow()
    total_ttc_sum = db.session.query(db.func.sum(FactureModel.total_ttc))\
        .filter(FactureModel.date_fin < current_time)\
        .filter(FactureModel.statut.in_(["NON_PAYEE", "PAYEE_PARTIELLEMENT"]))\
        .scalar()

    return total_ttc_sum if total_ttc_sum else 0


def update_validation(id_facture, validation_status):
    if validation_status not in ['NON_VALIDE', 'VALIDE']:
        return 'Invalid validation parameter', 400

    facture = FactureModel.query.filter_by(id_facture=id_facture).first()
    if facture is None:
        return 'Facture not found', 404

    facture.validation = validation_status
    db.session.commit()

    return f'Facture {id_facture} validation set to {validation_status}', 200


def create_facture(id_facture, id_client, TypeFacture, date_emission, descriptions, total, tva, total_ttc, statut, date_fin, validation):
    if TypeFacture in ['FORFAIT', 'JOUR_HOMME', 'LIVRABLES']:

        facture = FactureModel(
            id_facture=id_facture,
            id_client=id_client,
            validation=validation,
            TypeFacture=TypeFacture,
            date_emission=date_emission,
            descriptions=descriptions,
            total=total,
            date_fin=date_fin,
            tva=tva,
            total_ttc=total_ttc,
            statut=statut,

        )

        if descriptions:
            for desc in descriptions:
                if TypeFacture == 'FORFAIT':
                    tache = DescriptionModel(
                        tache=desc['tache'],
                        prix_ht=desc['prix_ht'],
                        prix_forfaitaire_ht=desc['prix_forfaitaire'],
                    )
                elif TypeFacture == 'JOUR_HOMME':
                    tache = DescriptionModel(
                        tache=desc['tache'],
                        prix_ht=desc['prix_ht'],
                        prix_jour=desc['prix_jour'],
                        nbr_jour=desc['nbr_jour'],
                    )
                elif TypeFacture == 'LIVRABLES':
                    tache = DescriptionModel(
                        tache=desc['tache'],
                        prix_ht=desc['prix_ht'],
                        prix_livrable=desc['prix_livrable'],
                    )
                else:
                    tache = DescriptionModel(
                        tache=desc['tache'],
                    )

                facture.descriptions.append(tache)

        db.session.add(facture)
        db.session.commit()
        return id_facture
    else:
        return None


def update_facture(_id_facture, TypeFacture, date_emission, descriptions, total, tva, total_ttc, id_client):
    facture = FactureModel.query.get(_id_facture)
    if facture:
        facture.TypeFacture = TypeFacture
        facture.date_emission = date_emission
        facture.total = total
        facture.tva = tva
        facture.total_ttc = total_ttc
        facture.id_client = id_client

        # Clear existing descriptions
        facture.descriptions.clear()

        # Add new descriptions
        for desc in descriptions:
            description = DescriptionModel(
                tache=desc.get('tache'),
                prix_ht=desc.get('prix_ht'),
                prix_forfaitaire_ht=desc.get(
                    'prix_forfaitaire_ht') if TypeFacture == 'FORFAIT' else None,
                prix_livrable=desc.get(
                    'prix_livrable') if TypeFacture == 'LIVRABLES' else None,
                nbr_jour=desc.get(
                    'nbr_jour') if TypeFacture == 'JOUR_HOMME' else None,
                prix_jour=desc.get(
                    'prix_jour') if TypeFacture == 'JOUR_HOMME' else None
            )
            facture.descriptions.append(description)

        db.session.commit()
        return {'Message': 'Facture mise à jour avec succès !'}
    return {'Message': 'Facture non trouvée !'}, 404


def delete_facture(_id):
    facture = FactureModel.query.get(_id)
    if facture:
        db.session.delete(facture)
        db.session.commit()
        return {'Message': 'Facture supprimée avec succès !'}
    return {'Message': 'Facture non trouvée !'}, 404


def get_factures_by_type(TypeFacture):
    factures = FactureModel.query.filter_by(TypeFacture=TypeFacture).all()
    return [facture.serialize() for facture in factures]
