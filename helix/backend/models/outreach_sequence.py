from datetime import datetime, UTC
from models import db

class OutreachSequence(db.Model):
    __tablename__ = 'outreach_sequences'

    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    company_name = db.Column(db.String(255), nullable=True)
    role_name = db.Column(db.String(255), nullable=True)
    candidate_persona = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(UTC))
    updated_at = db.Column(db.DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))
    
    # Relationship with steps
    steps = db.relationship('OutreachStep', backref='sequence', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'company_name': self.company_name,
            'role_name': self.role_name,
            'candidate_persona': self.candidate_persona,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'steps': [step.to_dict() for step in self.steps] if self.steps else []
        }
