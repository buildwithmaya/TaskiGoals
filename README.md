# TaskiGoals

TaskiGoals is a simple, user-friendly task and project management web application built with Flask and SQLite. It allows users to manage their daily tasks, organize them by projects, and keep track of their progress.

## Features

- User registration and login
- Add, view, and delete tasks
- Organize tasks by projects
- View completed, today, upcoming, and inbox tasks
- Search tasks by keyword
- Flash messages for user feedback

## Technologies Used

- Python 3
- Flask
- SQLite
- HTML/CSS (Jinja2 templates)

## Getting Started

### Prerequisites
- Python 3.x installed
- pip (Python package manager)

### Installation
1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd TaskiGoals
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables (optional but recommended for production):
   ```bash
   cp .env.example .env
   # Edit .env and set a strong SECRET_KEY
   ```

### Running the App
1. Start the Flask server:
   ```bash
   python app.py
   ```
2. Open your browser and go to `http://127.0.0.1:5000/`

## Project Structure

```
TaskiGoals/
├── app.py
├── model.py
├── requirements.txt
├── TaskiGoals.db
├── static/
│   └── styles.css
├── templates/
│   ├── base.html
│   ├── completed.html
│   ├── inbox.html
│   ├── index.html
│   ├── login.html
│   ├── myProjects.html
│   ├── project.html
│   ├── register.html
│   ├── search.html
│   ├── today.html
│   └── upcoming.html
└── __pycache__/
```

## Usage
- Register a new account or log in with existing credentials.
- Add new tasks with title, priority, status, date, and project.
- View tasks by different categories (today, upcoming, completed, inbox, projects).
- Mark tasks as completed or edit existing tasks.
- Delete tasks as needed.
- Search for tasks using keywords (searches only your own tasks).

## Security Features
- Password hashing using bcrypt
- User authentication required for all task operations
- User data isolation (users can only access their own data)
- Environment variable support for secret keys

## License
This project is for educational purposes.
