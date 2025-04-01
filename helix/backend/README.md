# Helix Backend

This is the backend for Helix, an AI-powered recruiting assistant that helps create personalized outreach sequences.

## Setup

1. **Environment Setup**:

   - Create a Python virtual environment (Python 3.9+ recommended):
     ```bash
     python -m venv venv
     ```

   - Activate the virtual environment:
     - Windows: `venv\Scripts\activate`
     - Linux/Mac: `source venv/bin/activate`

   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```

2. **Database Setup**:

   - Make sure PostgreSQL is installed and running
   - Update the `.env` file with your database credentials
   - Create the database (if it doesn't exist already):
     ```bash
     createdb helix
     ```
   - Run the setup script to initialize the database:
     ```bash
     python setup.py
     ```

3. **Configure Environment Variables**:

   - Copy `.env.example` to `.env` if not already done
   - Update the environment variables in `.env`:
     - Set database credentials
     - Add your OpenAI API key
     - Adjust other settings as needed

## Running the Application

1. Start the backend server:
   ```bash
   flask run
   ```
   
   Or with the socketio support:
   ```bash
   python app.py
   ```

2. The server will be available at:
   - http://localhost:5000

## API Endpoints

- `GET /api/sessions/current`: Get or create the current session
- `POST /api/messages`: Send a message and get a response
- `POST /api/sessions`: Create a new session
- `GET /api/sessions/{session_id}`: Get session details
- `GET /api/sequences`: Get all outreach sequences
- `GET /api/messages/{session_id}`: Get all messages in a session

## WebSocket Events

- `message`: Emitted when a new message is created, either by a user or the AI assistant

## Development

- Run tests: `pytest`
- Apply database migrations:
  ```bash
  flask db migrate -m "Migration message"
  flask db upgrade
  ```