from .database import db
from datetime import datetime

class Session(db.Model):
    __tablename__ = 'sessions'
    
    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    current_sequence_id = db.Column(db.String(36), db.ForeignKey('outreach_sequences.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    messages = db.relationship('Message', backref='session', lazy=True, order_by='Message.created_at')
    
    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.user_id,
            'currentSequenceId': self.current_sequence_id,
            'messages': [message.to_dict() for message in self.messages],
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None,
        }