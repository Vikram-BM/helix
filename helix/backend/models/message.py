from models import db
import json
from datetime import datetime, UTC

class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.String(36), primary_key=True)
    session_id = db.Column(db.String(36), db.ForeignKey('sessions.id'), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tool_call = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now(UTC))
    
    def to_dict(self):
        return {
            'id': self.id,
            'role': self.role,
            'content': self.content,
            'toolCall': json.loads(self.tool_call) if self.tool_call else None,
            'timestamp': self.created_at.isoformat() if self.created_at else None,
        }