from .models import ContractModel
from flask import request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import timedelta
from datetime import datetime, timedelta
from typing import Dict
from jinja2 import Template
from sqlalchemy import event
from sqlalchemy.orm import Session
from db import db
from datetime import datetime
from operator import itemgetter

def find_closest_expiring_contract(contracts):
    """
    Finds the closest expiring contract based on the date_fin attribute.
    
    Parameters:
    - contracts: List of ContractModel objects
    
    Returns:
    - The closest expiring ContractModel object
    """
    closest_contract = None
    closest_date = None
    
    for contract in contracts:
        if closest_date is None or contract.date_fin < closest_date:
            closest_date = contract.date_fin
            closest_contract = contract
            
    return closest_contract

def get_all_contracts():
    # type: ignore
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


def send_email(to_email, subject, body):
    try:
        print("Trying to send email...")
        msg = MIMEMultipart()
        msg["From"] = os.getenv("EMAIL_ADDRESS")
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        # Connexion au serveur SMTP
        with smtplib.SMTP("smtp.office365.com", 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(os.getenv("EMAIL_ADDRESS", ""),
                       os.getenv("EMAIL_PASSWORD", ""))
            smtp.sendmail(os.getenv("EMAIL_ADDRESS", ''),
                          to_email, msg.as_string())

        print("Email envoyé successivement")

    except Exception as e:
        print(f"An error occurred while sending the email: {e}")
        raise  # Raise the exception to propagate it to the calling code


def schedule_email(to_email, subject, data, date_rappel):
    def render_email_template(template_path, data):
        with open(template_path, 'r', encoding='utf-8') as file:
            template_str = file.read()
        template = Template(template_str)
        result = template.render({
            "Nom": "John Doe",
            "Numero_du_contrat": "12345",
            "Nom_du_client": "ABC Corp",
            "Date_limite": "2023-08-31",
        })
        return result

    template_data: Dict[str, str] = data
    template_path = 'Contracts/Template/NegoContrat.txt'
    subject = 'Alerte - Date limite de nouvelle négociation de contrat approchant'
    email_content = render_email_template(template_path, template_data)

    send_time = date_rappel

    scheduler = BackgroundScheduler()
    scheduler.add_job(
        send_email,
        args=[to_email, subject, email_content],
        trigger="date",
        run_date=send_time,
        id=str(to_email),
        max_instances=1,
    )
    scheduler.start()
