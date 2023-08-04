from db import db
from Relance.models import RelanceModel
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import timedelta
from datetime import datetime, timedelta
# Initialize the scheduler
scheduler = BackgroundScheduler(daemon=True)
scheduler.start()


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
            smtp.login(os.getenv("EMAIL_ADDRESS", ""), os.getenv("EMAIL_PASSWORD", ""))
            smtp.sendmail(os.getenv("EMAIL_ADDRESS",''), to_email, msg.as_string())

        print("Email sent successfully!")

    except Exception as e:
        print(f"An error occurred while sending the email: {e}")
        raise  # Raise the exception to propagate it to the calling code


def schedule_email(to_email, subject, body):
    delay_seconds = 10
    send_time = datetime.now() + timedelta(seconds=delay_seconds)

    # Schedule the email sending task with the date trigger
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        send_email,
        args=[to_email, subject, body],
        trigger="date",
        run_date=send_time,
        id=str(
            to_email
        ),  # Utiliser l'adresse e-mail comme identifiant unique de la tâche
        max_instances=1,  # Limiter à une seule instance de la tâche en cours d'exécution
    )
    scheduler.start()


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