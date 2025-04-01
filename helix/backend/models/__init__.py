from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models at the bottom of this file to avoid circular imports
# These imports will be executed after db is created

# DO NOT import models here - import them in app.py after db.init_app(app)

# Import models to ensure they're registered with SQLAlchemy
# These imports are intentionally at the bottom to avoid circular imports
from models.user import User
from models.session import Session
from models.message import Message
from models.outreach_sequence import OutreachSequence
from models.outreach_step import OutreachStep
