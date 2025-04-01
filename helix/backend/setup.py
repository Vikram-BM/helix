"""
Database setup script for Helix backend.
Run this script to initialize the database and apply migrations.
"""

import os
from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate, upgrade

# Load environment variables from .env file
load_dotenv()

from models import db

def setup_database():
    """Initialize the database and apply migrations."""
    app = Flask(__name__)
    
    # Database configuration using environment variables with defaults
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD', 'postgres')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME', 'helix')

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize DB and Migrate
    db.init_app(app)
    migrate = Migrate(app, db)
    
    with app.app_context():
        # Import models to ensure they're registered with SQLAlchemy
        from models.user import User
        from models.session import Session
        from models.message import Message
        from models.outreach_sequence import OutreachSequence
        from models.outreach_step import OutreachStep
        
        # Create tables if they don't exist
        db.create_all()
        
        print("Database tables created successfully.")

if __name__ == "__main__":
    setup_database()