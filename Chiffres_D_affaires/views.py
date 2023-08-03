from flask import Blueprint, jsonify, request
from datetime import datetime
from Chiffres_D_affaires.utils import filter_by_client,filter_by_clients,filter_by_period

cda=Blueprint( "cda" ,__name__,url_prefix="/cda")
@cda.get('/')
def get_all():
    return jsonify(clients=filter_by_clients())

@cda.get('/<int:_id>')
def get_by_id(id):
    client = filter_by_client(id)
    if isinstance(client, dict) and 'Message' in client:
        return jsonify(client), 404
    return jsonify(client=client)
@cda.get('/filter_by_period')
def filter_by_period():
    date_emission_str = request.args.get('date_emission')
    date_fin_str = request.args.get('date_fin')
    try:
        date_emission = datetime.strptime(date_emission_str, '%Y-%m-%d').date()
        date_fin = datetime.strptime(date_fin_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Format invalide !  Insérez YYYY-MM-DD !'}), 400
    filtered_clients = filter_by_period(date_emission, date_fin)
    return jsonify(filtered_clients)