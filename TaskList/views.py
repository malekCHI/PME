from flask import Blueprint, request, jsonify
from TaskList.models import Task
from TaskList.utils import get_all_tasks, add_new_task

from db import db
task = Blueprint('tasklist', __name__, url_prefix="/tasklist")


@task.get('/tasks')
def get_tasks():
    return jsonify(get_all_tasks())


@task.post('/add_task')
def add_task():
    data = request.get_json()

    if 'badgeText' not in data or data['badgeText'] not in ["Faible", "Moyenne", "Haute"]:
        return jsonify({'message': 'Invalid badgeText value (Haute/Moyenne/Faible)'}), 400

    add_new_task(
        data['task'],
        data['badgeText']
    )
    return jsonify({'message': 'New task added successfully'})
