from .database import db
from datetime import datetime

class OutreachSequence(db.Model):
    __tablename__ = 'outreach_sequences'
    
    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    company_name = db.Column(db.String(100))
    role_name = db.Column(db.String(100))
    candidate_persona = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    steps = db.relationship('OutreachStep', backref='sequence', lazy=True, order_by='OutreachStep.step_number')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'companyName': self.company_name,
            'roleName': self.role_name,
            'candidatePersona': self.candidate_persona,
            'steps': [step.to_dict() for step in self.steps],
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None,
        }

class OutreachStep(db.Model):
    __tablename__ = 'outreach_steps'
    
    id = db.Column(db.String(36), primary_key=True)
    sequence_id = db.Column(db.String(36), db.ForeignKey('outreach_sequences.id'), nullable=False)
    step_number = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    subject = db.Column(db.String(200))
    timing = db.Column(db.String(100))
    wait_time = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'stepNumber': self.step_number,
            'type': self.type,
            'content': self.content,
            'subject': self.subject,
            'timing': self.timing,
            'waitTime': self.wait_time,
        }