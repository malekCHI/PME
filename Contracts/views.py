from flask import Blueprint, request, jsonify
from Contracts.utils import find_closest_expiring_contract, add_contract, get_all_contracts
from Contracts.models import ContractModel
from Client.models import ClientModel
from datetime import datetime
from db import db
from Contracts.utils import schedule_email
from sqlalchemy.orm import Session
from datetime import date

contract = Blueprint("contract", __name__, url_prefix="/contract")


@contract.get("/active_contracts")
def get_active_contracts_count():
    """
    Endpoint to get the count of active contracts.
    """
    try:
        # Fetch all contracts
        all_contracts = ContractModel.query.all()

        # Count the number of active contracts
        active_count = 0
        for contract in all_contracts:
            if contract.date_fin >= date.today():
                active_count += 1

        return jsonify({"statut": "success", "active_contracts_count": active_count}), 200
    except Exception as e:
        return jsonify({"statut": "failure", "message": str(e)}), 500


@contract.get("/closest_expiring_contract")
def get_closest_expiring_contract():
    """
    Endpoint to get the closest expiring contract.
    """
    try:
        # Fetch all contracts
        all_contracts = ContractModel.query.all()

        # Find the closest expiring contract
        closest_contract = find_closest_expiring_contract(all_contracts)

        if closest_contract is not None:
            return jsonify({
                "statut": "success",
                "contract": {
                    "id_contract": closest_contract.id_contract,
                    "nom": closest_contract.client.nom,
                    "date_fin": closest_contract.date_fin.strftime("%Y-%m-%d"),
                    # Add other fields as needed
                }
            }), 200
        else:
            return jsonify({
                "statut": "failure",
                "message": "No active contracts found"
            }), 404  # Updated the message here
    except Exception as e:
        return jsonify({"statut": "failure", "message": str(e)}), 500


@contract.post("/create")
def create_contract():
    data = request.get_json()
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
    schedule_email_route()
    return {"message": "Contract added successfully"}


@contract.post('/schedule_email')
def schedule_email_route():
    data = request.get_json()

    try:
        id_client = data['id_client']
        subject = data['subject']
        body = data['body']

        # Fetch the client based on the provided name
        client = db.session.query(ClientModel).filter_by(
            id_client=id_client).first()

        if client:
            contract = ContractModel.query.filter_by(
                id_client=client.id_client).first()
            if contract:
                to_email = client.email_destinataire
                date_rappel = contract.date_rappel
                schedule_email(to_email, subject, body, date_rappel)

            to_email = client.email_destinataire
            schedule_email(to_email, subject, body,
                           date_rappel)  # type: ignore
            return jsonify({"message": "Email scheduled successfully."}), 200
        else:
            return jsonify({"error": "Client not found."}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@contract.get("/get_contract")
def get_contract():
    contracts = ContractModel.query.all()
    return jsonify({"contracts": [contract.serialize() for contract in contracts]})


@contract.put("/update/<int:contract_id>")
def update_contract(contract_id):
    data = request.get_json()
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
