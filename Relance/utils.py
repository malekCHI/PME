from db import db
from Relance.models import RelanceModel
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os



def send_email(to_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg["From"] = os.getenv('EMAIL_ADDRESS')
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        # Connexion au serveur SMTP
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=120) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(os.getenv('EMAIL_ADDRESS', ''), os.getenv('EMAIL_PASSWORD', ''))
            smtp.sendmail(os.getenv('EMAIL_ADDRESS',''), to_email, msg.as_string())

    except Exception as e:
        print(f"An error occurred while sending the email: {e}")


def get_all_relances():
    return RelanceModel.query.all()


def create_relance(id_facture, date_relance, message):
    relance = RelanceModel(
        id_facture=id_facture, date_relance=date_relance, message=message
    )
    db.session.add(relance)
    db.session.commit()
    return relance


def get_relance_by_id(id_relance):
    return RelanceModel.query.get(id_relance)


def delete_relance(relance):
    db.session.delete(relance)
    db.session.commit()
