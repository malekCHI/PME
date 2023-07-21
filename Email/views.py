from flask import Blueprint, request, jsonify
from .utils import generate_email

email = Blueprint("email", __name__, url_prefix="/email")

# Route to generate an email
@email.post('/send_email')
def send_email():
    data = request.get_json()
    template = data.get('template')
    subject = data.get('subject')
    body = data.get('body')
    recepient_email = data.get('recepient_email')

    if not template or not subject or not body:
        return jsonify({'message': 'Missing required fields.'}), 400

    try:
        generate_email(template, subject, body, recepient_email=recepient_email)
        return jsonify({'message': 'Email sent successfully.'}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to send email.', 'error': str(e)}), 500
