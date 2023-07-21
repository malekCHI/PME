import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os
from .models import Facture, Validation_de_la_facture, Rappel_daction, Rappel_de_date_nego, Rappel_de_paiement, EmailTemplate


# Load environment variables from .env file
load_dotenv()



# Function to generate email based on the template
def generate_email(template: EmailTemplate, subject: str, body: str, recepient_email : str):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = os.getenv('EMAIL_ADDRESS')
    msg['To'] = recepient_email
    
    if template == 'Facture':
        body = Facture
    elif template == 'Rappel de paiement':
        body = Rappel_de_paiement
    elif template == 'Validation de la facture':
        body = Validation_de_la_facture
    elif template == 'Rappel daction':
        body = Rappel_daction
    elif template == 'Rappel de date nego':
        body = Rappel_de_date_nego

    msg.set_content(body)

    with smtplib.SMTP_SSL('smtp.live.com', 465) as smtp:
        smtp.login(os.getenv('EMAIL_ADDRESS', ''), os.getenv('EMAIL_PASSWORD', ''))
        smtp.send_message(msg)
        
    generate_email(template, subject, body, recepient_email=recepient_email)