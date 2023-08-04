from .models import ContractModel
from flask import request


def get_all_contracts():
    return {"contracts": list(map(lambda x: x.serialize(), ContractModel.query.all()))}


def get_contract(contract_id):
    contract = ContractModel.query.get(contract_id)
    if contract:
        return {"contract": contract.serialize()}
    return {"error": "Contract not found"}


def is_valid_date(date):
    # Ajoutez ici votre logique de validation de la date
    return True


def is_valid_string(value):
    return value is not None and isinstance(value, str) and value.strip() != ""


def add_contract(
    id_client,
    date_debut,
    date_fin,
    conditions_financieres,
    prochaine_action,
    date_prochaine_action,
    date_rappel,
    fichier_pdf,
):
    if not is_valid_date(date_debut):
        return {"error": "Invalid start date"}
    if not is_valid_date(date_fin):
        return {"error": "Invalid end date"}
    if not is_valid_string(conditions_financieres):
        return {"error": "Invalid financial conditions"}
    if not is_valid_string(prochaine_action):
        return {"error": "Invalid next action"}
    if not is_valid_date(date_prochaine_action):
        return {"error": "Invalid next action date"}
    if not is_valid_date(date_rappel):
        return {"error": "Invalid reminder date"}
    if not is_valid_string(fichier_pdf):
        return {"error": "Invalid PDF file"}
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


def update_contract(contract_id):
    contract = ContractModel.query.get(contract_id)
    if contract:
        data = request.get_json()
        contract.id_client = data.get("id_client", contract.id_client)
        contract.date_debut = data.get("date_debut", contract.date_debut)
        contract.date_fin = data.get("date_fin", contract.date_fin)
        contract.conditions_financieres = data.get(
            "conditions_financieres", contract.conditions_financieres
        )
        contract.prochaine_action = data.get(
            "prochaine_action", contract.prochaine_action
        )
        contract.date_prochaine_action = data.get(
            "date_prochaine_action", contract.date_prochaine_action
        )
        contract.date_rappel = data.get("date_rappel", contract.date_rappel)
        contract.fichier_pdf = data.get("fichier_pdf", contract.fichier_pdf)
        contract.save_to_db()
        return {"message": "Contract updated successfully"}
    else:
        return {"error": "Contract not found"}
