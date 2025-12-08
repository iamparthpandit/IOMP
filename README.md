# IOMP - Integrated Online Management Platform

A modern web application with Python Flask backend and beautiful UI for educational institution management.

## Features

- ✅ User Authentication (Login & Signup)
- ✅ JWT Token-based Authorization
- ✅ Role-based Access (Student, Teacher, Admin)
- ✅ Modern, Responsive UI with Tailwind CSS
- ✅ SQLite Database
- ✅ RESTful API

## Tech Stack

**Backend:**
- Python 3.x
- Flask
- Flask-SQLAlchemy (Database ORM)
- Flask-Bcrypt (Password Hashing)
- Flask-JWT-Extended (JWT Authentication)
- Flask-CORS (Cross-Origin Resource Sharing)

**Frontend:**
- HTML5
- Tailwind CSS
- Font Awesome Icons
- Vanilla JavaScript

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository** (if using Git)
   ```powershell
   git clone <repository-url>
   cd IOMP
   ```

2. **Create a virtual environment** (recommended)
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   - The `.env` file is already created with default values
   - For production, update these values:
     ```
     SECRET_KEY=your_unique_secret_key
     JWT_SECRET_KEY=your_unique_jwt_secret
     ```

5. **Run the application**
   ```powershell
   python app.py
   ```

6. **Access the application**
   - Open your browser and navigate to: `http://localhost:5000`
   - Login page: `http://localhost:5000/login`
   - Signup page: `http://localhost:5000/signup`

## API Endpoints

### Authentication

- **POST** `/api/auth/signup` - Register a new user
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123",
    "role": "student"
  }
  ```

- **POST** `/api/auth/login` - Login user
  ```json
  {
    "email": "john@example.com",
    "password": "password123"
  }
  ```

- **GET** `/api/auth/me` - Get current user (requires JWT token)
  - Header: `Authorization: Bearer <token>`

## Project Structure

```
IOMP/
│
├── app.py              # Main Flask application
├── models.py           # Database models
├── routes.py           # API routes
├── requirements.txt    # Python dependencies
├── .env               # Environment variables
├── .gitignore         # Git ignore file
│
├── index.html         # Dashboard page
├── login.html         # Login page
├── signup.html        # Signup page
└── profile.html       # Profile page
```

## Database

The application uses SQLite by default. The database file (`iomp.db`) will be created automatically when you first run the application.

### User Model
- `id` - Primary key
- `name` - User's full name
- `email` - Unique email address
- `password_hash` - Encrypted password
- `role` - User role (student, teacher, admin)
- `profile_picture` - Profile image URL
- `created_at` - Registration timestamp

## Development

To run in development mode with auto-reload:

```powershell
$env:FLASK_ENV="development"
python app.py
```

## Security Notes

- Passwords are hashed using Bcrypt before storing
- JWT tokens expire after 7 days
- CORS is enabled for all origins (configure for production)
- Change SECRET_KEY and JWT_SECRET_KEY in production

## License

ISC

## Author

IOMP Development Team
