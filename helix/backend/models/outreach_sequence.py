from datetime import datetime, UTC
from models import db

class OutreachSequence(db.Model):
    __tablename__ = 'outreach_sequences'

    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), nullable=False)
    name = db.Column(db.String(255), nullable=False)
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
            'userId': self.user_id,
            'name': self.name,
            'companyName': self.company_name,
            'roleName': self.role_name,
            'candidatePersona': self.candidate_persona,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None,
            'steps': [step.to_dict() for step in self.steps] if self.steps else []
        }

