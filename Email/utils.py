from jinja2 import Template
import smtplib
from typing import Dict
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()

def render_email_template(template_path, data):
    with open(template_path, 'r', encoding='utf-8') as file:
        template_str = file.read()
    template = Template(template_str)
    result = template.render(**data)
    return result

def generate_email(subject: str, email_content: str, recipient_email: str):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = os.getenv('EMAIL_ADDRESS')
    msg['To'] = recipient_email
    msg.set_content(email_content)

    with smtplib.SMTP('smtp.office365.com', 587, timeout=120) as smtp:
        smtp.ehlo()  # send the extended hello to our server
        smtp.starttls()  # tell server we want to communicate with TLS encryption
        smtp.login(os.getenv('EMAIL_ADDRESS',''), os.getenv('EMAIL_PASSWORD',''))
        smtp.send_message(msg)
        smtp.quit()

def generate_date_nego_email(data: Dict[str, str], recipient_email: str):
    template_data: Dict[str, str] = data
    template_path = 'Email/Templates/Date_nego.txt'
    subject = 'Rappel de date de négociation de contrat - ' + template_data['Numéro_de_contrat'] + ' - ' + template_data['Nom_de_l_entreprise']
    email_content = render_email_template(template_path, template_data)
    generate_email(subject, email_content, recipient_email)
    
def generate_facture_email(data: Dict[str, str], recipient_email: str):
    template_data: Dict[str, str] = data
    template_path = 'Email/Templates/Facture.txt'
    subject = 'Facture - ' + template_data['Numéro_de_facture'] + ' - ' + template_data['Nom_de_l_entreprise']
    email_content = render_email_template(template_path, template_data)
    generate_email(subject, email_content, recipient_email)

def generate_rappel_action_email(data: Dict[str, str], recipient_email: str):
    template_data: Dict[str, str] = data
    template_path = 'Email/Templates/Rappel_action.txt'
    subject = 'Rappel d\'action - ' + template_data['Description_de_l_action'] + ' - ' + template_data['Nom_de_l_entreprise']
    email_content = render_email_template(template_path, template_data)
    generate_email(subject, email_content, recipient_email)

def generate_rappel_paiement_email(data: Dict[str, str], recipient_email: str):
    template_data: Dict[str, str] = data
    template_path = 'Email/Templates/Rappel_de_paiement.txt'
    subject = 'Rappel de paiement - ' + template_data['Numéro_de_facture'] + ' - ' + template_data['Nom_de_l_entreprise']
    email_content = render_email_template(template_path, template_data)
    generate_email(subject, email_content, recipient_email)

def generate_validation_email(data: Dict[str, str], recipient_email: str):
    template_data: Dict[str, str] = data
    template_path = 'Email/Templates/Validation.txt'
    subject = 'Validation de la facture - ' + template_data['Numéro_de_facture'] + ' - ' + template_data['Nom_de_l_entreprise']
    email_content = render_email_template(template_path, template_data)
    generate_email(subject, email_content, recipient_email)