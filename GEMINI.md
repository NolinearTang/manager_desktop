# GEMINI.md

## Project Overview

This project is a "Label System Management System," an intelligent platform for managing tag hierarchies based on intent recognition. It features a Python FastAPI backend and a frontend built with HTML, Tailwind CSS, and vanilla JavaScript. The system supports multi-level tag management, rule configuration, and intelligent intent recognition.

**Key Technologies:**

*   **Backend:** Python, FastAPI, SQLAlchemy, Redis
*   **Frontend:** HTML, Tailwind CSS, JavaScript
*   **Database:** MySQL/PostgreSQL

**Architecture:**

The project is divided into two main parts: a `backend` directory containing the FastAPI application and a `web` directory with static frontend files. The backend serves the API and the frontend. The database schema is designed to handle a hierarchical label system, rules for intent recognition, and mappings between entities and tags.

## Building and Running

**1. Install Dependencies:**

*   **Backend:**
    ```bash
    cd backend
    pip install -r requirements.txt
    ```

**2. Configure Environment:**

*   Copy the `.env.example` file to `.env` and update it with your database connection details.
    ```bash
    cp backend/.env.example backend/.env
    ```

**3. Set up the Database:**

*   Create a database (e.g., `label_system`).
*   Import the database schema:
    ```bash
    mysql -u <username> -p <database_name> < database_schema.sql
    ```

**4. Run the Application:**

*   Start the backend server:
    ```bash
    python start_backend.py
    ```
    or
    ```bash
    cd backend
    uvicorn app.main:app --reload
    ```

*   Access the application in your browser:
    *   **API Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
    *   **Frontend:** [http://127.0.0.1:8000/static/tag-system-list.html](http://127.0.0.1:8000/static/tag-system-list.html)

## Development Conventions

*   **Code Style:** The backend uses `black` for code formatting and `flake8` for linting. `mypy` is used for static type checking.
*   **Testing:** The backend uses `pytest` for testing.
*   **API Documentation:** The API is documented using OpenAPI, and the documentation is available at the `/docs` endpoint.
*   **Frontend:** The frontend uses Tailwind CSS for styling and vanilla JavaScript for interactivity. The data is currently mocked in the HTML files but is intended to be fetched from the backend API.
