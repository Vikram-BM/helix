# Database Setup for Helix

Follow these steps to set up the database for the Helix application.

## Prerequisites

1. PostgreSQL installed on your system
2. Basic knowledge of PostgreSQL commands

## Setup Steps

1. Create the database:

   ```bash
   createdb helix
   ```

   If you prefer to use the PostgreSQL shell:

   ```bash
   psql
   CREATE DATABASE helix;
   \q
   ```

2. Create a user (optional):

   ```bash
   psql
   CREATE USER helix_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE helix TO helix_user;
   \q
   ```

3. Update the `.env` file in the backend directory with your database credentials:

   ```
   DB_USER=postgres  # or your custom user
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=helix
   ```

4. Initialize the database tables with the application:

   ```bash
   cd helix/backend
   python app.py
   ```

   The first run will automatically create all necessary tables.

## Troubleshooting

If you encounter any database connection issues:

1. Make sure PostgreSQL is running:
   ```
   pg_ctl status -D /path/to/data/directory
   ```

2. Check if you can connect to the database:
   ```
   psql -U postgres -d helix
   ```

3. Verify the credentials in your `.env` file match your PostgreSQL setup

4. Check the database tables:
   ```
   psql -U postgres -d helix
   \dt
   ```

## Manual Table Creation

If needed, you can manually create the tables using SQL:

```sql
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    company VARCHAR(100),
    role VARCHAR(100),
    preferences TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE outreach_sequences (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    company_name VARCHAR(255),
    role_name VARCHAR(255),
    candidate_persona TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE sessions (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) REFERENCES users(id) NOT NULL,
    current_sequence_id VARCHAR(36) REFERENCES outreach_sequences(id),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE messages (
    id VARCHAR(36) PRIMARY KEY,
    session_id VARCHAR(36) REFERENCES sessions(id) NOT NULL,
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    tool_call TEXT,
    created_at TIMESTAMP
);

CREATE TABLE outreach_steps (
    id VARCHAR(36) PRIMARY KEY,
    sequence_id VARCHAR(36) REFERENCES outreach_sequences(id) NOT NULL,
    step_number INTEGER NOT NULL,
    type VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    subject VARCHAR(255),
    timing VARCHAR(50),
    wait_time INTEGER DEFAULT 0,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```