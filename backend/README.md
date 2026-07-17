# TechTots LMS - Backend API

Python Flask backend for the TechTots Learning Management System.

## Quick Start

### Prerequisites
- Python 3.9+
- MongoDB (local or Atlas)
- pip or uv package manager

### Installation

1. **Install dependencies**
```bash
pip install -r requirements.txt
```

2. **Configure environment**
```bash
# Copy .env.example to .env and update values
cp .env.example .env
```

3. **Configure MongoDB**
   - For local: Ensure MongoDB is running on `localhost:27017`
   - For Atlas: Update `MONGODB_URI` in `.env`

4. **Run development server**
```bash
python run.py
```

Server will start on `http://localhost:5000`

## Project Structure

```
backend/
├── app/
│   ├── models/          # Data models (User, Course, etc.)
│   ├── routes/          # API endpoints organized by resource
│   ├── services/        # Business logic layer
│   ├── middleware/      # Auth, logging, error handling
│   ├── utils/           # Helper functions
│   └── factory.py       # Flask app factory
├── config/
│   └── config.py        # Configuration management
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables
└── run.py              # Application entry point
```

## API Documentation

### Base URL
```
http://localhost:5000/api/v1
```

### Available Endpoints

#### Health Check
- `GET /health` - Server health check

#### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `GET /auth/me` - Get current user info
- `POST /auth/refresh` - Refresh access token

#### Users (Phase 2)
- `GET /users` - List all users
- `GET /users/:id` - Get user details
- `PUT /users/:id` - Update user
- `DELETE /users/:id` - Delete user

#### Courses (Phase 3)
- `GET /courses` - List courses
- `POST /courses` - Create course
- `GET /courses/:id` - Get course details
- `PUT /courses/:id` - Update course
- `DELETE /courses/:id` - Delete course

#### Lessons (Phase 3)
- `GET /courses/:id/lessons` - List course lessons
- `POST /courses/:id/lessons` - Add lesson
- `PUT /lessons/:id` - Update lesson
- `DELETE /lessons/:id` - Delete lesson

#### Assessments (Phase 4)
- `GET /assessments` - List assessments
- `POST /assessments` - Create assessment
- `POST /assessments/:id/questions` - Add question

#### Progress (Phase 5)
- `GET /progress` - Get user progress
- `POST /progress` - Record progress

#### Gamification (Phase 6)
- `GET /leaderboards` - Get leaderboards
- `GET /badges` - List available badges
- `GET /users/:id/badges` - Get user badges

#### Analytics (Phase 7)
- `GET /analytics` - Get analytics data

## Authentication

All protected endpoints require JWT token in the Authorization header:

```
Authorization: Bearer <access_token>
```

## Development

### Running Tests
```bash
# Tests will be added in Phase 16
pytest tests/
```

### Database Migrations
```bash
# Migrations are handled automatically on startup
```

### Code Style
```bash
# Code style checking (coming soon)
flake8 app/
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_ENV` | development | Environment mode |
| `FLASK_DEBUG` | True | Debug mode |
| `FLASK_HOST` | 0.0.0.0 | Server host |
| `FLASK_PORT` | 5000 | Server port |
| `MONGODB_URI` | mongodb://localhost:27017 | MongoDB connection string |
| `JWT_SECRET_KEY` | dev-key | JWT signing secret |
| `CORS_ORIGINS` | http://localhost:3000 | Allowed CORS origins |

## Production Deployment

For production:

1. Set `FLASK_ENV=production` in `.env`
2. Update `JWT_SECRET_KEY` with a strong random key
3. Use proper MongoDB (Atlas or managed service)
4. Run with Gunicorn:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 "app.factory:create_app()"
   ```
5. Use a reverse proxy (nginx) for SSL/TLS

## Troubleshooting

### MongoDB Connection Error
- Ensure MongoDB is running
- Check `MONGODB_URI` in `.env`
- For Atlas: Whitelist your IP address

### JWT Token Error
- Ensure `Authorization` header is present
- Format: `Bearer <token>`
- Check token hasn't expired

### CORS Error
- Update `CORS_ORIGINS` in `.env` if running on different host
- Ensure frontend Origin header matches

## Implementation Phases

- **Phase 1**: ✅ Project Setup & Dependencies
- **Phase 2**: Authentication & User Management (In Progress)
- **Phase 3**: Course & Lesson Management
- **Phase 4**: Assessments & Quizzes
- **Phase 5**: Progress Tracking
- **Phase 6**: Gamification
- **Phase 7**: Analytics
- **Phase 8**: File Upload & Media

## Contributing

See the implementation plan in `/v0_plans/innovative-route.md` for detailed technical specifications.
