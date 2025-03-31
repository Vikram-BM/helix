from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os
from dotenv import load_dotenv
import uuid
from datetime import datetime

from models.database import db, init_db
from flask_migrate import Migrate
from models.user import User
from models.session import Session
from models.message import Message
from models.sequence import OutreachSequence, OutreachStep

from services.agentic_service import AgenticService
from services.message_service import MessageService
from services.sequence_service import SequenceService

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///helix.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

init_db(app)
migrate = Migrate(app, db)

agentic_service = AgenticService()
message_service = MessageService(agentic_service)
sequence_service = SequenceService()

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/api/sessions/current', methods=['GET'])
def get_current_session():
    user_id = request.headers.get('X-User-Id', str(uuid.uuid4()))
    
    session = Session.query.filter_by(user_id=user_id).order_by(Session.updated_at.desc()).first()
    
    if not session:
        session = Session(
            id=str(uuid.uuid4()),
            user_id=user_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(session)
        db.session.commit()
    
    return jsonify(session.to_dict())

@app.route('/api/sessions', methods=['POST'])
def create_session():
    user_id = request.headers.get('X-User-Id', str(uuid.uuid4()))
    
    session = Session(
        id=str(uuid.uuid4()),
        user_id=user_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    db.session.add(session)
    db.session.commit()
    
    return jsonify(session.to_dict())

@app.route('/api/messages', methods=['POST'])
def create_message():
    data = request.json
    user_id = request.headers.get('X-User-Id', str(uuid.uuid4()))
    
    session = Session.query.filter_by(user_id=user_id).order_by(Session.updated_at.desc()).first()
    
    if not session:
        session = Session(
            id=str(uuid.uuid4()),
            user_id=user_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(session)
        db.session.commit()
    
    user_message = Message(
        id=str(uuid.uuid4()),
        session_id=session.id,
        role=data.get('role', 'user'),
        content=data.get('content', ''),
        created_at=datetime.utcnow()
    )
    
    db.session.add(user_message)
    session.updated_at = datetime.utcnow()
    db.session.commit()
    
    socketio.emit('message', user_message.to_dict())
    
    response = message_service.process_message(user_message, session)
    
    if response:
        socketio.emit('message', response.to_dict())
    
    return jsonify(user_message.to_dict())

@app.route('/api/sequences', methods=['GET'])
def get_sequences():
    user_id = request.headers.get('X-User-Id', str(uuid.uuid4()))
    
    sequences = OutreachSequence.query.filter_by(user_id=user_id).all()
    
    return jsonify([sequence.to_dict() for sequence in sequences])

@app.route('/api/sequences/<sequence_id>', methods=['GET'])
def get_sequence(sequence_id):
    sequence = OutreachSequence.query.get(sequence_id)
    
    if not sequence:
        return jsonify({"error": "Sequence not found"}), 404
    
    return jsonify(sequence.to_dict())

@app.route('/api/sequences', methods=['POST'])
def create_sequence():
    data = request.json
    user_id = request.headers.get('X-User-Id', str(uuid.uuid4()))
    
    sequence = OutreachSequence(
        id=str(uuid.uuid4()),
        user_id=user_id,
        name=data.get('name', 'New Outreach Sequence'),
        company_name=data.get('companyName', ''),
        role_name=data.get('roleName', ''),
        candidate_persona=data.get('candidatePersona', ''),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    db.session.add(sequence)
    db.session.commit()
    
    socketio.emit('sequence_update', sequence.to_dict())
    
    return jsonify(sequence.to_dict())

@app.route('/api/sequences/<sequence_id>', methods=['PUT'])
def update_sequence(sequence_id):
    data = request.json
    
    sequence = OutreachSequence.query.get(sequence_id)
    
    if not sequence:
        return jsonify({"error": "Sequence not found"}), 404
    
    if 'name' in data:
        sequence.name = data['name']
    
    if 'companyName' in data:
        sequence.company_name = data['companyName']
    
    if 'roleName' in data:
        sequence.role_name = data['roleName']
    
    if 'candidatePersona' in data:
        sequence.candidate_persona = data['candidatePersona']
    
    sequence.updated_at = datetime.utcnow()
    db.session.commit()
    
    socketio.emit('sequence_update', sequence.to_dict())
    
    return jsonify(sequence.to_dict())

@app.route('/api/sequences/<sequence_id>/steps/<step_id>', methods=['PUT'])
def update_step(sequence_id, step_id):
    data = request.json
    
    step = OutreachStep.query.get(step_id)
    
    if not step or str(step.sequence_id) != sequence_id:
        return jsonify({"error": "Step not found"}), 404
    
    if 'content' in data:
        step.content = data['content']
    
    if 'subject' in data:
        step.subject = data['subject']
    
    if 'type' in data:
        step.type = data['type']
    
    if 'timing' in data:
        step.timing = data['timing']
    
    if 'waitTime' in data:
        step.wait_time = data['waitTime']
    
    db.session.commit()
    
    sequence = OutreachSequence.query.get(sequence_id)
    socketio.emit('sequence_update', sequence.to_dict())
    
    return jsonify(sequence.to_dict())

@app.route('/api/users/profile', methods=['GET'])
def get_user_profile():
    user_id = request.headers.get('X-User-Id', str(uuid.uuid4()))
    
    user = User.query.get(user_id)
    
    if not user:
        user = User(
            id=user_id,
            name="",
            email="",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(user)
        db.session.commit()
    
    return jsonify(user.to_dict())

@app.route('/api/users/profile', methods=['PUT'])
def update_user_profile():
    data = request.json
    user_id = request.headers.get('X-User-Id', str(uuid.uuid4()))
    
    user = User.query.get(user_id)
    
    if not user:
        user = User(
            id=user_id,
            name=data.get('name', ''),
            email=data.get('email', ''),
            company=data.get('company', ''),
            role=data.get('role', ''),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(user)
    else:
        if 'name' in data:
            user.name = data['name']
        
        if 'email' in data:
            user.email = data['email']
        
        if 'company' in data:
            user.company = data['company']
        
        if 'role' in data:
            user.role = data['role']
        
        if 'preferences' in data:
            user.preferences = data['preferences']
        
        user.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify(user.to_dict())

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('message')
def handle_message(data):
    print('Received message:', data)

@socketio.on('update_sequence')
def handle_sequence_update(data):
    print('Sequence update:', data)
    sequence_id = data.get('id')
    
    if not sequence_id:
        return
    
    sequence = OutreachSequence.query.get(sequence_id)
    
    if not sequence:
        return
    
    if 'name' in data:
        sequence.name = data['name']
    
    if 'companyName' in data:
        sequence.company_name = data['companyName']
    
    if 'roleName' in data:
        sequence.role_name = data['roleName']
    
    if 'candidatePersona' in data:
        sequence.candidate_persona = data['candidatePersona']
    
    sequence.updated_at = datetime.utcnow()
    db.session.commit()
    
    emit('sequence_update', sequence.to_dict(), broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))