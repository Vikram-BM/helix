"""
Database setup script for Helix backend - fixes circular import issues
"""

import os
from dotenv import load_dotenv
from flask import Flask

# Load environment variables
load_dotenv()

# Create app
app = Flask(__name__)

# Configure database
db_user = os.getenv('DB_USER', 'postgres')
db_password = os.getenv('DB_PASSWORD', 'bmvik1400')
db_host = os.getenv('DB_HOST', 'localhost')
db_port = os.getenv('DB_PORT', '5432')
db_name = os.getenv('DB_NAME', 'helix')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Import db and initialize
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

# Define models directly to avoid circular imports
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    company = db.Column(db.String(100))
    role = db.Column(db.String(100))
    preferences = db.Column(db.Text)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

class OutreachSequence(db.Model):
    __tablename__ = 'outreach_sequences'

    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    company_name = db.Column(db.String(255), nullable=True)
    role_name = db.Column(db.String(255), nullable=True)
    candidate_persona = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

class Session(db.Model):
    __tablename__ = 'sessions'
    
    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    current_sequence_id = db.Column(db.String(36), db.ForeignKey('outreach_sequences.id'), nullable=True)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.String(36), primary_key=True)
    session_id = db.Column(db.String(36), db.ForeignKey('sessions.id'), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tool_call = db.Column(db.Text)
    created_at = db.Column(db.DateTime)

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
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

if __name__ == "__main__":
    try:
        with app.app_context():
            db.create_all()
            print("Database tables created successfully!")
    except Exception as e:
        print(f"Error creating database tables: {e}")