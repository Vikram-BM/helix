# Import the shared SQLAlchemy instance
from models import db

def init_db(app):
    """Initialize the database with the given Flask app.
    
    This function is kept for backward compatibility, but models/__init__.py 
    should be the single source of the db instance.
    """
    db.init_app(app)
    
    with app.app_context():
        db.create_all()