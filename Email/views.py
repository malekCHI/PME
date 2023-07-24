from flask import Blueprint, request, jsonify
from .utils import generate_email, TypeEmail

email = Blueprint("email", __name__, url_prefix="/email")

# Route to generate an email
@email.post('/send_email')
def send_email():
    data = request.get_json()
    template = data.get('template')
    subject = data.get('subject')
    recipient_email = data.get('recipient_email')

    if not template or not subject or not recipient_email:
        return jsonify({'message': 'Missing required fields.'}), 400

    try:
        # Add other required fields to the 'data' dictionary based on the template
        data['Nom du client'] = data.get('Nom du client', '')
        data['Numéro de facture'] = data.get('Numéro de facture', '')
        data['Montant de la facture'] = data.get('Montant de la facture', '')
        data['Date d\'échéance de paiement'] = data.get('Date d\'échéance de paiement', '')
        data['Nom de l\'entreprise'] = data.get('Nom de l\'entreprise', '')

        generate_email(TypeEmail(template), subject, data, recipient_email)
        return jsonify({'message': 'Email sent successfully.'}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to send email.', 'error': str(e)}), 500
