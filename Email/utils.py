import smtplib
from email.message import EmailMessage
from typing import Dict
from dotenv import load_dotenv
import os
from Email.models import EmailTemplates, TypeEmail

# Load environment variables from .env file
load_dotenv()

# Function to generate email based on the template and data
def generate_email(template: TypeEmail, subject: str, data: Dict[str, str], recipient_email: str):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = os.getenv('EMAIL_ADDRESS')
    msg['To'] = recipient_email

    # Get the email body template based on the selected template
    body_template = EmailTemplates[template.value].value

    # Replace placeholders with data values
    for key, value in data.items():
        placeholder = f"[{key}]"
        body_template = body_template.replace(placeholder, value)

    msg.set_content(body_template)

    with smtplib.SMTP_SSL('smtp.live.com', 465) as smtp:
        smtp.login(os.getenv('EMAIL_ADDRESS','None'), os.getenv('EMAIL_PASSWORD','None'))
        smtp.send_message(msg)
