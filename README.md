# Helix: AI-Powered Recruiting Assistant

Helix is an intelligent recruiting assistant that helps create personalized outreach sequences for contacting candidates. It provides a conversational interface where recruiters can describe their needs and get tailored outreach sequences generated for them.

## Features

- **Conversational Interface**: Chat with Helix to describe your recruiting needs
- **Personalized Sequences**: Generate outreach sequences tailored to specific roles and candidate personas
- **Multi-Channel Outreach**: Create sequences across email, LinkedIn, and phone
- **Sequence Management**: Save, edit, and manage your outreach sequences
- **Real-time Updates**: See responses as they're generated using WebSocket technology

## Project Structure

- `/frontend`: React TypeScript frontend application
- `/backend`: Flask Python backend API

## Prerequisites

- Node.js and npm (for frontend)
- Python 3.9+ (for backend)
- PostgreSQL database

## Quick Start

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd helix
   ```

2. Set up environment variables:
   - Backend: Copy `backend/.env.example` to `backend/.env` and update with your credentials
   - Frontend: Copy `frontend/.env.example` to `frontend/.env` if needed

3. Make sure the run scripts are executable:
   ```bash
   chmod +x run.sh
   chmod +x helix/backend/run_backend.sh
   chmod +x helix/frontend/run_frontend.sh
   ```

4. Run the application:
   ```bash
   ./run.sh
   ```

   This script will:
   - Start the backend Flask server in a separate terminal window
   - Start the frontend React application
   - Open the application in your browser

   **Troubleshooting:** If the application doesn't start properly, you may need to run the backend and frontend separately:
   - In one terminal: `cd helix/backend && ./run_backend.sh`
   - In another terminal: `cd helix/frontend && ./run_frontend.sh`

## Manual Setup

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd helix/backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database:
   ```bash
   python setup.py
   ```

5. Start the backend:
   ```bash
   python app.py
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd helix/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the frontend development server:
   ```bash
   npm start
   ```

## Usage

1. Open your browser and navigate to http://localhost:3000
2. Start a conversation with Helix by describing your recruiting needs
3. Helix will guide you through creating an outreach sequence
4. You can view, edit, and manage your sequences in the workspace panel

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for providing the AI models that power Helix
- The Flask and React communities for their excellent frameworks