from flask import Blueprint, jsonify, request
from datetime import datetime
from Chiffres_D_affaires.utils import filter_by_client, filter_by_clients, filter_by_period

cda = Blueprint("cda", __name__, url_prefix="/cda")

@cda.route('/')
def get_all():
    return jsonify(clients=filter_by_clients())

@cda.get('/<string:client_name>')
def get_by_client_name(client_name):
    client = filter_by_client(client_name)
    if isinstance(client, dict) and 'Message' in client:
        return jsonify(client), 404
    return jsonify(clients=client)


@cda.route('/filter_by_period')
def get_by_period():
    date_emission_str = request.args.get('date_emission')
    date_fin_str = request.args.get('date_fin')
    if not date_emission_str or not date_fin_str:
        return jsonify({'error': 'Both date d\'emission and date fin parameters are required!'}), 400
    try:
        date_emission = datetime.strptime(date_emission_str, '%Y-%m-%d').date()
        date_fin = datetime.strptime(date_fin_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Format invalide !  Insérez YYYY-MM-DD !'}), 400
    filtered_clients = filter_by_period(date_emission, date_fin)
    return jsonify(clients=filtered_clients)
