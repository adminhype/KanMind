# KanMind Backend

This is the backend repository for the **KanMind** project, a Kanban board management tool. It is built with **Django** and **Django REST Framework (DRF)** and serves as the RESTful API for the KanMind frontend application.

## Project Demo

[![Watch Demo](./assets/thumbnail.png)](https://github.com/user-attachments/assets/33864fa5-dd86-40ca-9874-b9d974f6edd6)
*(Click the image to watch the video)*

> **Note:** If the video does not play directly, you can view it by navigating to the `assets/` folder in this repository.

---

## Features

*   **Modular Architecture:** The project uses a strictly separated app structure (`auth_app`, `board_app`, `task_app`).
*   **Authentication:** Secure Token-based authentication via `rest_framework.authtoken`.
*   **CORS Configuration:** Pre-configured to accept requests from local frontend servers running on Port 5500.
*   **Board & Task Management:** Complete CRUD operations including assignment logic and sub-tasks.
*   **Permissions:** Granular access control (e.g., only board members can edit tasks).
*   **Code Quality:** Adheres to PEP8 standards with comprehensive documentation.

---

## Technology Stack

*   **Framework:** Django 5.2 & Django REST Framework
*   **Database:** SQLite (Development default)
*   **Authentication:** DRF Token Authentication
*   **Middleware:** django-cors-headers

---

## Setup & Installation

Follow these steps to set up the project locally.

### 1. Clone the Repository
```bash
git clone <YOUR_GITHUB_REPO_URL>
cd <YOUR_PROJECT_FOLDER>
```

### 2. Create and Activate a Virtual Environment

**Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory of your project. This file should contain your Django `SECRET_KEY`. You can generate a new, secure key on websites like https://djecrety.ir/.

Example `.env` file:
```
SECRET_KEY='your_very_secret_key_here'
```

### 5. Database Setup
Initialize the database and apply migrations for `auth_app`, `board_app`, and `task_app`.

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Run the Server
Start the development server.

```bash
python manage.py runserver
```

The API will be accessible at: `http://127.0.0.1:8000/`

---

## Frontend Integration

This backend is specifically designed to work with the **KanMind Frontend**, which is built using Vanilla JavaScript.

*   **Frontend Repository:** [Developer-Akademie-Backendkurs/project.KanMind](https://github.com/Developer-Akademie-Backendkurs/project.KanMind)

**How to connect:**
1.  Clone the frontend repository separately.
2.  Open the frontend project in VS Code.
3.  Start the frontend using the **Live Server** extension (usually running on Port 5500).
4.  The backend `CORS_ALLOWED_ORIGINS` is already configured to accept requests from `http://127.0.0.1:5500` and `http://localhost:5500`.

---

## Project Structure

The project follows a strictly modular architecture. The main configuration is located in the `core` folder.

```text
root/
├── core/               # Project settings, wsgi, asgi, main urls
├── auth_app/           # Login, Registration, Token logic
│   └── api/            # Serializers, Views, URLs for Auth
├── board_app/          # Logic for Kanban Boards
│   └── api/            # Serializers, Views, URLs for Boards
├── task_app/           # Logic for Tasks and Comments
│   └── api/            # Serializers, Views, URLs for Tasks
├── manage.py
└── requirements.txt
```

---

## API Documentation

Below is an overview of the key endpoints.

### Authentication (`auth_app`)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/registration/` | Register a new user |
| `POST` | `/api/login/` | Login and retrieve token |

### Boards (`board_app`)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/boards/` | List all boards |
| `POST` | `/api/boards/` | Create a new board |
| `GET` | `/api/boards/{id}/` | Get board details |
| `PATCH` | `/api/boards/{id}/` | Update board |
| `DELETE`| `/api/boards/{id}/` | Delete board |
| `GET` | `/api/email-check/` | Check user availability |

### Tasks (`task_app`)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/tasks/` | List tasks |
| `POST` | `/api/tasks/` | Create a new task |
| `GET` | `/api/tasks/assigned-to-me/`| Get tasks assigned to user |
| `GET` | `/api/tasks/reviewing/` | Get tasks where user is reviewer |
| `PATCH` | `/api/tasks/{id}/` | Update task |
| `DELETE`| `/api/tasks/{id}/` | Delete task |

### Comments
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/tasks/{id}/comments/` | List comments for a task |
| `POST` | `/api/tasks/{id}/comments/` | Add a comment |
| `DELETE`| `/api/tasks/{id}/comments/{comment_id}/`| Delete a comment |

---

## License

This project is created for educational purposes.
```