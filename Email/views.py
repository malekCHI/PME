from flask import request, jsonify, Blueprint
from Email.utils import (
    generate_date_nego_email,
    generate_facture_email,
    generate_rappel_action_email,
    generate_rappel_paiement_email,
    generate_validation_email,

)
import os

TEMPLATES_FOLDER = os.getenv('TEMPLATES', '')

email = Blueprint("email", __name__, url_prefix="/email")


@email.post('/generate_date_nego')
def generate_date_nego():
    data = request.get_json()
    recipient_email = data.get('recipient_email', '')
    if not recipient_email:
        return jsonify({"message": "L'e-mail du destinataire est manquant"}), 400
    generate_date_nego_email(data['template_data'], recipient_email)
    return jsonify({"message": "Email envoyé"}), 200
# {
#     "recipient_email": "ahmed.alaya@medtech.tn",
#     "template_data": {
#         "Numéro_de_contrat": "CN987654",
#         "Nom_du_destinataire": "Jane Doe",
#         "Date_de_début_du_contrat": "2023-09-01",
#         "Date_de_fin_du_contrat": "2024-08-31",
#         "Date_de_rappel_de_négociation": "2024-07-31",
#         "Nom_de_l_entreprise": "Ma Société"
#     }
# }


@email.post('/generate_facture')
def generate_facture():
    data = request.get_json()
    recipient_email = data.get('recipient_email', '')
    if not recipient_email:
        return jsonify({"message": "L'e-mail du destinataire est manquant"}), 400
    generate_facture_email(data['template_data'], recipient_email)
    return jsonify({"message": "Email envoyé"}), 200
# {
#     "recipient_email": "ahmed.alaya@medtech.tn",
#     "template_data": {
#         "Numéro_de_facture": "F98765",
#         "Montant_de_la_facture": "1500.00",
#         "Date_de_la_facture": "2023-07-31",
#         "Date_d_échéance": "2023-08-15",
#         "Méthode_de_paiement": "Carte de crédit",
#         "Nom_de_l_entreprise": "Ma Société"
#     }
# }


@email.post('/generate_rappel_action')
def generate_rappel_action():
    data = request.get_json()
    recipient_email = data.get('recipient_email', '')
    if not recipient_email:
        return jsonify({"message": "L\'e-mail du destinataire est manquant"}), 400
    generate_rappel_action_email(data['template_data'], recipient_email)
    return jsonify({"message": "Email envoyé !"}), 200
# {
#     "recipient_email": "ahmed.alaya@medtech.tn",
#     "template_data": {
#         "Numéro_de_facture": "F98765",
#         "Montant_de_la_facture": "1500.00",
#         "Date_de_la_facture": "2023-07-31",
#         "Date_d_échéance": "2023-08-15",
#         "Méthode_de_paiement": "Espece",
#         "Nom_de_l_entreprise": "Ma Société"
#     }
# }


@email.post('/generate_rappel_paiement')
def generate_rappel_paiement():
    data = request.get_json()
    recipient_email = data.get('recipient_email', '')
    if not recipient_email:
        return jsonify({"message": "L'e-mail du destinataire est manquant"}), 400
    generate_rappel_paiement_email(data['template_data'], recipient_email)
    return jsonify({"message": "Email envoyé"}), 200
# {
#     "recipient_email": "ahmed.alaya@medtech.tn",
#     "template_data": {
#         "Description_de_l_action": "Réviser le rapport mensuel",
#         "Date_limite_de_l_action": "2023-08-15",
#         "Nom_de_l_utilisateur": "John Doe",
#         "Nom_de_l_entreprise": "Ma Société"
#     }
# }


@email.post('/create_template')
def create_template():
    data = request.get_json()
    template_content = data.get("template_content")
    if template_content:
        try:
            with open('template.txt', 'w') as file:
                file.write(template_content)
            return jsonify({"message": "Template created successfully"}), 201
        except Exception as e:
            return jsonify({"message": f"Error creating template: {str(e)}"}), 500
    else:
        return jsonify({"message": "Template content is required"}), 400


@email.get('/read_template')
def read_template():
    try:
        with open('template.txt', 'r') as file:
            template_content = file.read()
            return jsonify({"template_content": template_content}), 200
    except FileNotFoundError:
        return jsonify({"message": "Template not found"}), 404
    except Exception as e:
        return jsonify({"message": f"Error reading template: {str(e)}"}), 500


@email.put('/update_template')
def update_template():
    data = request.get_json()
    template_content = data.get('template_content')
    if template_content:
        try:
            with open('template.txt', 'w') as file:
                file.write(template_content)
            return jsonify({"message": "Template updated successfully"}), 200
        except Exception as e:
            return jsonify({"message": f"Error updating template: {str(e)}"}), 500
    else:
        return jsonify({"message": "Template content is required"}), 400


@email.delete('/delete_template')
def delete_template():
    try:
        os.remove('template.txt')
        return jsonify({"message": "Template deleted successfully"}), 200
    except FileNotFoundError:
        return jsonify({"message": "Template not found"}), 404
    except Exception as e:
        return jsonify({"message": f"Error deleting template: {str(e)}"}), 500


@email.post('/generate_validation')
def generate_validation():
    data = request.get_json()
    recipient_email = data.get('recipient_email', '')
    if not recipient_email:
        return jsonify({"message": "L'e-mail du destinataire est manquant"}), 400
    generate_validation_email(data['template_data'], recipient_email)
    return jsonify({"message": "Email envoyé"}), 200
# {
#     "recipient_email": "ahmed.alaya@medtech.tn",
#     "template_data": {
#         "Numéro_de_facture": "F98765",
#         "Montant_de_la_facture": "1500.00",
#         "Date_de_la_facture": "2023-07-31",
#         "Date_d_échéance": "2023-08-15",
#         "Méthode_de_paiement": "Carte de crédit",
#         "Nom_de_l_entreprise": "Ma Société"
#     }
# }
