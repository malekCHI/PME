from flask import Blueprint, request, jsonify
from Factures.models import FactureModel
from db import db
from Paiement.models import PaiementModel
from Paiement.utils import add_paiement, calculate_etat_paiement, TypeStatut

paiement = Blueprint("paiement", __name__, url_prefix="/paiement")


@paiement.post("/create")
def create_paiement():
    data = request.get_json()
    id_facture = data.get("id_facture")
    montant = data.get("montant")
    date_paiement = data.get("date_paiement")   
    if not id_facture or not montant:
        return jsonify({"message": "Les données du paiement sont incomplètes."}), 400

    # Vérifier si la facture existe dans la base de données
    facture = FactureModel.query.get(id_facture)
    if facture is None:
        return jsonify({"message": "La facture avec l'ID spécifié n'existe pas."}), 404

    # Vérifier si la facture est déjà payée
    if facture.statut == TypeStatut.PAYEE.value:
        return jsonify({"message": "La facture est déjà payée. Impossible d'ajouter un nouveau paiement."}), 400
    
    montant = float(data.get("montant"))
    total_ttc = float(facture.total_ttc)
    # Vérifier si le montant est supérieur au montant total de la facture
    if montant > facture.total_ttc:
       raise Exception("Le montant du paiement ne doit pas dépasser le montant total de la facture (TTC).")

     # Calculer le montant restant à payer
    montant_restant = facture.total_ttc - sum(paiement.montant for paiement in facture.paiements)

    # Vérifier si le montant est supérieur au montant restant à payer
    if montant > montant_restant:
      raise Exception(f"Le montant du paiement ne doit pas dépasser le montant restant à payer de la facture. Montant restant à payer : {montant_restant}.")



    # Créez l'objet PaiementModel
    nouveau_paiement = PaiementModel(
        id_facture=id_facture,
        montant=montant,
        date_paiement=date_paiement,
    )

    # Enregistrez le paiement dans la base de données
    nouveau_paiement.save_to_db()

    # Mettez à jour le statut de la facture associée en utilisant la fonction calculate_etat_paiement
    statut = calculate_etat_paiement(facture)

    if statut is not None:
        facture.statut = statut.value
    else:
        
        
     # Si la fonction retourne None, vous pouvez lever une exception si nécessaire
     raise Exception(f"Impossible de déterminer le paiement de la facture. Montant restant à payer : {montant_restant}.")
    db.session.commit()

    return jsonify({"message": "Paiement créé avec succès."}), 201
