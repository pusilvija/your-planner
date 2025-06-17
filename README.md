# Your Planner – Backend

This is the **backend API** for [Your Planner](https://github.com/pusilvija/your-planner-fe), it is a personal task management app featuring a visual taskboard, CRUD functionality, and user authentication. It’s built as a full-stack application, showcasing modern frontend development with React and a Django backend.

PostgreSQL database, backend and frontend are all deployed on Railway.

<br>

## ✨ Features

- Registration, login, and logout using token-based authentication.
- Task Management
  - Create, update, delete, and reorder tasks.
  - Each task can have a name, description, category, status (`To Do`, `In Progress`, `Done`), and order.
  - Tasks are associated with the authenticated user.
- Kanban Board
  - View tasks grouped by their status.
  - Bulk update of task status and order.
- REST API Endpoints for all CRUD operations.
- Manage all tasks via the Django admin interface.
- Includes automated tests for user authentication and task CRUD operations.


<br>


## 🛠️ Tech Stack

- **Django** - Python web framework for building secure and scalable web applications.
- **Django REST Framework** - toolkit for building RESTful APIs with Django.
- **Token Authentication** - a stateless authentication mechanism using tokens for secure API access.
- **PostgreSQL** - open-source relational database system for storing application data.


<br>

## 🚀 Getting Started (Local)

### 1. Clone the repository
```bash
git clone https://github.com/pusilvija/your-planner.git
cd your-planner
```
### 2. Set Up the backend

1. Create virtual environment:
- `python3 -m venv venv`
- `source venv/bin/activate`

2. Install Python dependencies:
- `pip install -r requirements.txt`

### 3. Start the backend server

```bash
python manage.py runserver
```
The backend will run at http://127.0.0.1:8000.

### 4. Management

If you have superuser you can manage application in:
http://127.0.0.1:8000/admin


### 5. Environment Variables
The following environment variables are required for the deployment process:
- **DJANGO_SECRET_KEY**: A secret key used for cryptographic signing in Django.
- **DJANGO_DEBUG**: True for for development, False for production.
- **DATABASE_URL**: Specifies the connection string for your database.
- **CORS_ALLOWED_ORIGINS**: Specifies the list of origins (domains) allowed to make cross-origin requests to your backend. Add your local development and production urls.

Copy .env.example file to create .env file with required variables.

### 6. Testing

To run test:
```bash
python manage.py test
```

<br> 

## 🚀 Deployment Process

The deployment process for **Your Planner** is automated with Railway. The deployment is triggered automatically whenever changes are pushed to the `release` branch.



<br>

## 🔗 Frontend Repository
Frontend code can be found [here](https://github.com/pusilvija/your-planner-fe).

<br>

## 📸 Some screenshots from application

### Landing Page view
![Landing Page Screenshot](docs/images/screenshot0.png)

### Login view
![Login Page Screenshot](docs/images/screenshot1.png)

### Taskboard View
![Taskboard Screenshot](docs/images/screenshot2.png)

### All Tasks View
![All Tasks Screenshot](docs/images/screenshot3.png)

### All Tasks View - Filter
![All Tasks - filter Screenshot](docs/images/screenshot4.png)

### Tasks Details View
![Task Details Screenshot](docs/images/screenshot5.png)
