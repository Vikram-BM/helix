# Helix: The Agentic Recruiter

Helix is an AI-powered recruiter assistant that helps generate personalized outreach sequences. It uses a conversational interface to understand your recruiting needs and creates effective outreach sequences for connecting with candidates.

## Features

- Chat-driven interface for intuitive interactions
- Real-time sequence generation based on conversation
- Direct editing of sequences in the workspace
- Multi-step outreach sequence creation (email, LinkedIn, phone)
- Live updates between interface and server

## Tech Stack

### Frontend
- React with TypeScript
- Socket.io for real-time updates
- Modern responsive design

### Backend
- Flask REST API
- Flask-SocketIO for WebSocket communication
- Custom agentic framework
- OpenAI integration

### Database
- PostgreSQL (SQLAlchemy ORM)

## Getting Started

### Prerequisites

- Node.js (v14+)
- Python (v3.8+)
- PostgreSQL

### Installation

1. **Clone the repository**

```bash
git clone <repository-url>
cd helix
```

2. **Set up the backend environment**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configure the environment variables**

Create a `.env` file in the backend directory:

```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://username:password@localhost/helix
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4
```

4. **Initialize the database**

```bash
# Ensure PostgreSQL is running
flask db init
flask db migrate
flask db upgrade
```

5. **Set up the frontend environment**

```bash
cd ../frontend
npm install
```

6. **Create a .env file in the frontend directory**

```
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_SOCKET_URL=http://localhost:5000
```

### Running the Application

1. **Start the backend server**

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python app.py
```

2. **Start the frontend development server**

```bash
cd frontend
npm start
```

3. **Access the application**

Open your browser and go to `http://localhost:3000`

## Usage

1. Start a conversation by describing your recruiting needs
2. Helix will ask clarifying questions to understand your requirements
3. Once enough information is collected, a sequence will be generated
4. Edit the sequence directly in the workspace or through conversational interactions
5. Save and use your outreach sequences for recruiting

## Project Structure

```
helix/
├── frontend/                # React frontend
│   ├── public/              # Static files
│   └── src/                 # React source code
│       ├── components/      # React components
│       ├── contexts/        # React contexts for state management
│       ├── services/        # API and socket services
│       └── types/           # TypeScript type definitions
│
└── backend/                 # Flask backend
    ├── api/                 # API endpoints
    ├── models/              # Database models
    ├── services/            # Business logic services
    └── utils/               # Utility functions
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.