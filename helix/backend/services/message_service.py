from models.message import Message

class MessageService:
    def __init__(self, agentic_service):
        self.agentic_service = agentic_service
    
    def process_message(self, message, session):
        return self.agentic_service.process_message(message, session)