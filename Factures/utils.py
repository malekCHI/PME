from Factures.models import FactureModel, DescriptionModel
from db import db

# def add_taches_to_facture(facture_id, taches):
#     facture = FactureModel.query.get(facture_id)
#     if facture:
#         for tache in taches:
#             new_tache = DescriptionModel(tache=tache)
#             db.session.add(new_tache)
#         db.session.commit()
#         return {'Message': f'Taches added to Facture {facture_id} successfully!'}
#     return {'Message': 'Facture not found!'}, 404

def get_all_factures():
    factures = FactureModel.query.all()
    return [facture.serialize() for facture in factures]

def get_facture(_id):
    facture = FactureModel.query.get(_id)
    if facture:
        return facture.serialize()
    return {'Message': 'Facture non trouvée !'}, 404

def create_facture(id_facture, TypeFacture, date_emission, descriptions, total, tva, total_ttc):
    if TypeFacture in ['FORFAIT', 'JOUR_HOMME', 'LIVRABLES']:
        facture = FactureModel(
            id_facture=id_facture,
            TypeFacture=TypeFacture,
            date_emission=date_emission,
            total=total,
            tva=tva,
            total_ttc=total_ttc,
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
def update_facture(_id_facture, TypeFacture, date_emission, descriptions, total, tva, total_ttc):
    facture = FactureModel.query.get(_id_facture)
    if facture:
        facture.TypeFacture = TypeFacture
        facture.date_emission = date_emission
        facture.total = total
        facture.tva = tva
        facture.total_ttc = total_ttc

        # Clear existing descriptions
        facture.descriptions.clear()

        # Add new descriptions
        for desc in descriptions:
            description = DescriptionModel(
                tache=desc.get('tache'),
                prix_ht=desc.get('prix_ht'),
                prix_forfaitaire_ht=desc.get('prix_forfaitaire_ht') if TypeFacture == 'FORFAIT' else None,
                prix_livrable=desc.get('prix_livrable') if TypeFacture == 'LIVRABLES' else None,
                nbr_jour=desc.get('nbr_jour') if TypeFacture == 'JOUR_HOMME' else None,
                prix_jour=desc.get('prix_jour') if TypeFacture == 'JOUR_HOMME' else None
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
