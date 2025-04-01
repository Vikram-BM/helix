# Message service will use the database instance from the app

class MessageService:
    def __init__(self, agentic_service):
        self.agentic_service = agentic_service

    def process_message(self, message, session):
        # Use the process_message method from AgenticService
        response = self.agentic_service.process_message(message, session)
        return response
