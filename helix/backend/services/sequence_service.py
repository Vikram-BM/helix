from models.database import db
from models.sequence import OutreachSequence, OutreachStep

class SequenceService:
    def get_sequence(self, sequence_id):
        return OutreachSequence.query.get(sequence_id)
    
    def get_sequences_by_user(self, user_id):
        return OutreachSequence.query.filter_by(user_id=user_id).all()
    
    def update_sequence(self, sequence_id, updates):
        sequence = OutreachSequence.query.get(sequence_id)
        
        if not sequence:
            return None
        
        for key, value in updates.items():
            if hasattr(sequence, key):
                setattr(sequence, key, value)
        
        db.session.commit()
        
        return sequence
    
    def update_step(self, step_id, updates):
        step = OutreachStep.query.get(step_id)
        
        if not step:
            return None
        
        for key, value in updates.items():
            if hasattr(step, key):
                setattr(step, key, value)
        
        db.session.commit()
        
        return step.sequence