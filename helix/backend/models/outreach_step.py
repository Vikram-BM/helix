from datetime import datetime, UTC
from models import db

class OutreachStep(db.Model):
    __tablename__ = 'outreach_steps'

    id = db.Column(db.String(36), primary_key=True)
    sequence_id = db.Column(db.String(36), db.ForeignKey('outreach_sequences.id'), nullable=False)
    step_number = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(50), nullable=False)  # email, linkedin, phone, other
    content = db.Column(db.Text, nullable=False)
    subject = db.Column(db.String(255), nullable=True)  # For email subject lines
    timing = db.Column(db.String(50), nullable=True)    # e.g., "Day 1", "Day 3"
    wait_time = db.Column(db.Integer, default=0)        # Days to wait after previous step
    created_at = db.Column(db.DateTime, default=datetime.now(UTC))
    updated_at = db.Column(db.DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))

    def to_dict(self):
        return {
            'id': self.id,
            'sequenceId': self.sequence_id,
            'stepNumber': self.step_number,
            'type': self.type,
            'content': self.content,
            'subject': self.subject,
            'timing': self.timing,
            'waitTime': self.wait_time,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None
        }
