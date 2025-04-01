#!/bin/bash

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Check for database initialization
python -c "
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

try:
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD', 'postgres')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME', 'helix')
    
    conn = psycopg2.connect(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
    conn.close()
    print('Database connection successful')
except Exception as e:
    print(f'Error connecting to database: {e}')
    exit(1)
"

if [ $? -ne 0 ]; then
    echo "Database connection failed. Please check your database settings and run setup.py."
    exit 1
fi

# Run database setup if needed
python setup.py

# Run the Flask application with SocketIO support
python app.py