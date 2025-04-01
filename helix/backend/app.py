import os
import uuid
from datetime import datetime, UTC
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_migrate import Migrate

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app first
app = Flask(__name__)
CORS(app)

# Database configuration using environment variables with defaults
db_user = os.getenv('DB_USER', 'postgres')
db_password = os.getenv('DB_PASSWORD', 'bmvik1400')
db_host = os.getenv('DB_HOST', 'localhost')
db_port = os.getenv('DB_PORT', '5432')
db_name = os.getenv('DB_NAME', 'helix')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set up the database directly in this file to avoid circular imports
db = SQLAlchemy(app)

# Initialize other extensions
migrate = Migrate(app, db)
socketio = SocketIO(app, cors_allowed_origins="*")

# Define models
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    company = db.Column(db.String(100))
    role = db.Column(db.String(100))
    preferences = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now(UTC))
    updated_at = db.Column(db.DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'company': self.company,
            'role': self.role,
            'preferences': {},
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None,
        }

class OutreachSequence(db.Model):
    __tablename__ = 'outreach_sequences'

    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
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
        
class Session(db.Model):
    __tablename__ = 'sessions'
    
    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    current_sequence_id = db.Column(db.String(36), db.ForeignKey('outreach_sequences.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(UTC))
    updated_at = db.Column(db.DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))
    
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
            'toolCall': None,
            'timestamp': self.created_at.isoformat() if self.created_at else None,
        }

class OutreachStep(db.Model):
    __tablename__ = 'outreach_steps'

    id = db.Column(db.String(36), primary_key=True)
    sequence_id = db.Column(db.String(36), db.ForeignKey('outreach_sequences.id'), nullable=False)
    step_number = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    subject = db.Column(db.String(255), nullable=True)
    timing = db.Column(db.String(50), nullable=True)
    wait_time = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now(UTC))
    updated_at = db.Column(db.DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))

    def to_dict(self):
        return {
            'id': self.id,
            'sequence_id': self.sequence_id,
            'step_number': self.step_number,
            'type': self.type,
            'content': self.content,
            'subject': self.subject,
            'timing': self.timing,
            'wait_time': self.wait_time,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# Create tables
with app.app_context():
    db.create_all()

# Import services
from services.agentic_service import AgenticService
from services.message_service import MessageService

# Update AgenticService to use this db instance
AgenticService.db = db


# ------------------------------
# Initialize Services
# ------------------------------

# Create AgenticService instance
agentic_service = AgenticService()
# Set the db instance in AgenticService
agentic_service.db = db

# Pass agentic_service when initializing MessageService
message_service = MessageService(agentic_service)


# ------------------------------
# API Endpoints
# ------------------------------

@app.route('/api/sessions/current', methods=['GET'])
def get_current_session():
    user_id = request.headers.get('X-User-Id', str(uuid.uuid4()))

    # Check if user exists, create if not
    user = db.session.get(User, user_id)
    if not user:
        user = User(
            id=user_id,
            name="Test User",
            email="test@example.com",
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC)
        )
        db.session.add(user)
        db.session.commit()

    session = (
        Session.query.filter_by(user_id=user_id)
        .order_by(Session.updated_at.desc())
        .first()
    )

    # Create a session if one doesn't exist
    if not session:
        session = Session(
            id=str(uuid.uuid4()),
            user_id=user_id,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC)
        )
        db.session.add(session)
        db.session.commit()

    return jsonify(session.to_dict())


@app.route('/api/messages', methods=['POST'])
def create_message():
    data = request.json
    user_id = request.headers.get('X-User-Id', str(uuid.uuid4()))

    # Ensure user exists
    user = db.session.get(User, user_id)
    if not user:
        user = User(
            id=user_id,
            name="Test User",
            email="test@example.com",
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC)
        )
        db.session.add(user)
        db.session.commit()

    session = (
        Session.query.filter_by(user_id=user_id)
        .order_by(Session.updated_at.desc())
        .first()
    )

    # Create a session if it doesn't exist
    if not session:
        session = Session(
            id=str(uuid.uuid4()),
            user_id=user_id,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC)
        )
        db.session.add(session)
        db.session.commit()

    # Create a new message
    user_message = Message(
        id=str(uuid.uuid4()),
        session_id=session.id,
        role=data.get('role', 'user'),
        content=data.get('content', ''),
        created_at=datetime.now(UTC)
    )

    db.session.add(user_message)
    session.updated_at = datetime.now(UTC)
    db.session.commit()

    # Emit message to WebSocket clients
    # socketio.emit('message', user_message.to_dict())

    # Process message using message_service
    response = message_service.process_message(user_message, session)

    if response:
        socketio.emit('message', response.to_dict())

    return jsonify(user_message.to_dict())


@app.route('/api/sessions', methods=['POST'])
def create_session():
    user_id = request.headers.get('X-User-Id', str(uuid.uuid4()))

    # Check if user exists
    user = db.session.get(User, user_id)
    if not user:
        user = User(
            id=user_id,
            name="Test User",
            email="test@example.com",
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC)
        )
        db.session.add(user)
        db.session.commit()

    # Create new session
    session = Session(
        id=str(uuid.uuid4()),
        user_id=user_id,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC)
    )

    db.session.add(session)
    db.session.commit()

    return jsonify(session.to_dict())


@app.route('/api/sessions/<session_id>', methods=['GET'])
def get_session(session_id):
    session = db.session.get(Session, session_id)
    if not session:
        return jsonify({'error': 'Session not found'}), 404
    return jsonify(session.to_dict())


@app.route('/api/sequences', methods=['GET'])
def get_sequences():
    sequences = OutreachSequence.query.all()
    return jsonify([sequence.to_dict() for sequence in sequences])


@app.route('/api/messages/<session_id>', methods=['GET'])
def get_messages(session_id):
    messages = (
        Message.query.filter_by(session_id=session_id)
        .order_by(Message.created_at)
        .all()
    )
    return jsonify([message.to_dict() for message in messages])


# ------------------------------
# WebSocket Event Handling
# ------------------------------

@socketio.on('connect')
def handle_connect():
    print('Client connected')


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


# ------------------------------
# Error Handlers
# ------------------------------

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


# ------------------------------
# Run Application
# ------------------------------

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
