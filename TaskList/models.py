
from db import db
from datetime import datetime


class Task(db.Model):
    __tablename__ = "tasklist"
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    badgeText = db.Column(db.String(50), nullable=False)
    badgeType = db.Column(db.String(50))

    def serialize(self):
        return {
            'id': self.id,
            'task': self.task,
            'date': self.date,
            'badgeText': self.badgeText,
            'badgeType': self.badgeType
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
