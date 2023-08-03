from flask import Blueprint, request, jsonify
from Contracts.utils import get_all_contracts, add_contract
from Contracts.models import ContractModel

from db import db


contract = Blueprint("contract", __name__, url_prefix="/contract")


@contract.post("/create")
def create_contract():
    data = request.get_json
    id_client = data.get("id_client")
    date_debut = data.get("date_debut")
    date_fin = data.get("date_fin")
    conditions_financieres = data.get("conditions_financieres")
    prochaine_action = data.get("prochaine_action")
    date_prochaine_action = data.get("date_prochaine_action")
    date_rappel = data.get("date_rappel")
    fichier_pdf = data.get("fichier_pdf")

    contract = ContractModel(
        id_client=id_client,
        date_debut=date_debut,
        date_fin=date_fin,
        conditions_financieres=conditions_financieres,
        prochaine_action=prochaine_action,
        date_prochaine_action=date_prochaine_action,
        date_rappel=date_rappel,
        fichier_pdf=fichier_pdf,
    )
    contract.save_to_db()

    return {"message": "Contract added successfully"}


@contract.get("/get_contract")
def get_contract():
    contracts = ContractModel.query.all()
    return jsonify({"contracts": [contract.serialize() for contract in contracts]})


@contract.put("/update/<int:contract_id>")
def update_contract(contract_id):
    data = request.get_json
    id_client = data.get("id_client")
    date_debut = data.get("date_debut")
    date_fin = data.get("date_fin")
    conditions_financieres = data.get("conditions_financieres")
    prochaine_action = data.get("prochaine_action")
    date_prochaine_action = data.get("date_prochaine_action")
    date_rappel = data.get("date_rappel")
    fichier_pdf = data.get("fichier_pdf")

    contract = ContractModel.query.get(contract_id)
    if contract is None:
        return jsonify({"error": "Contract not found!"}), 404

    contract.id_client = id_client
    contract.date_debut = date_debut
    contract.date_fin = date_fin
    contract.conditions_financieres = conditions_financieres
    contract.prochaine_action = prochaine_action
    contract.date_prochaine_action = date_prochaine_action
    contract.date_rappel = date_rappel
    contract.fichier_pdf = fichier_pdf

    contract.save_to_db()

    return {"message": "Contract updated successfully"}


@contract.delete("/delete/<int:contract_id>")
def delete_contract(contract_id):
    contract = ContractModel.query.get(contract_id)
    if contract:
        contract.delete_from_db()
        return {"message": "Contract deleted successfully"}
    return {"error": "Contract not found"}
