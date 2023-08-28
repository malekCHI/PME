from db import db
from TaskList.models import Task
from sqlalchemy import func


def get_all_tasks():
    return {'tasks': list(map(lambda x: x.serialize(), Task.query.all()))}


def add_new_task(task, badgeText):
    if badgeText not in ["Faible", "Moyenne", "Haute"]:
        raise ValueError("Invalid badgeText value")

    badgeType_map = {
        "Faible": "warning",
        "Moyenne": "primary",
        "Haute": "error"
    }

    badgeType = badgeType_map[badgeText]

    max_id = db.session.query(func.max(Task.id)).scalar()
    next_id = max_id + 1 if max_id is not None else 1

    new_task = Task(
        id=next_id,
        task=task,
        badgeText=badgeText,
        badgeType=badgeType
    )
    new_task.save_to_db()
