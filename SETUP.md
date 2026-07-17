# TechTots LMS - Setup Guide

This is a complete Learning Management System built with Next.js (frontend) and Flask (backend).

## Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+
- MongoDB Atlas account (or local MongoDB)
- Git

### Frontend Setup (Next.js)

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Set up environment variables:**
   Create `.env.local` in the project root:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:5000
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```
   Open [http://localhost:3000](http://localhost:3000)

### Backend Setup (Flask)

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Install dependencies:**
   ```bash
   pip install --break-system-packages -r requirements.txt
   ```

3. **Start the Flask server:**
   ```bash
   bash start.sh
   ```
   Or manually:
   ```bash
   python3 run.py
   ```
   The backend runs on [http://localhost:5000](http://localhost:5000)

## Project Structure

```
/app                    # Next.js pages and routes
  /auth                 # Authentication pages (login, register)
  /dashboard           # Main dashboard page
  /profile             # User profile page
  /teach               # Teacher/instructor pages
    /my-courses
    /create-course
    /students
  /learn               # Student learning page
  layout.tsx           # Root layout
  page.tsx             # Home page

/components            # React components
  /dashboard           # Dashboard components (Student, Teacher, Admin)

/contexts              # React context providers
  /auth-context.tsx    # Authentication context

/lib                   # Utility functions
  /api-client.ts       # API client for backend calls

/types                 # TypeScript types

/backend               # Flask backend
  /app
    /routes            # API endpoints
    /models            # MongoDB models
    /services          # Business logic
    /utils             # Utility functions
  config/              # Configuration
  run.py               # Entry point
  requirements.txt     # Python dependencies
  start.sh             # Startup script
```

## Features

### Authentication
- User registration (Student, Teacher, Admin)
- Email & password login
- JWT token-based authentication
- Persistent session with localStorage
- Auto-redirect to dashboard on login
- Protected routes

### Student Features
- Browse and enroll in courses
- Track learning progress
- View course progress by lessons
- Earn badges and points
- View streaks and achievements
- Complete quizzes and assessments

### Teacher Features
- Create and manage courses
- Add lessons and content
- View enrolled students
- Track student progress
- Create quizzes and assessments
- View course analytics

### Admin Features
- View system-wide analytics
- Manage users (Students, Teachers, Admins)
- Monitor platform health
- View completion rates
- Track active users

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login
- `GET /api/v1/auth/me` - Get current user
- `POST /api/v1/auth/refresh` - Refresh token

### Courses
- `GET /api/v1/courses` - List courses
- `GET /api/v1/courses/<id>` - Get course details
- `POST /api/v1/courses` - Create course (teacher only)
- `PUT /api/v1/courses/<id>` - Update course
- `POST /api/v1/courses/<id>/enroll` - Enroll in course

### Progress
- `GET /api/v1/progress/courses` - Get student progress
- `GET /api/v1/progress/<id>` - Get specific progress

### Analytics
- `GET /api/v1/analytics/admin/dashboard` - Admin analytics

### Users
- `GET /api/v1/users` - List users (admin)
- `GET /api/v1/users/<id>` - Get user details
- `PUT /api/v1/users/<id>` - Update user

## Environment Variables

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:5000  # Backend API URL
```

### Backend (.env or start.sh)
```env
MONGODB_URI=mongodb://...                  # MongoDB connection string
DATABASE_NAME=techtots                     # Database name
JWT_SECRET_KEY=TECHTOTS@2026              # JWT secret
FLASK_ENV=development                      # Environment
FLASK_HOST=0.0.0.0                        # Host
FLASK_PORT=5000                           # Port
CORS_ORIGINS=http://localhost:3000        # CORS origins
```

## Testing

### Test Accounts (create via registration)
1. **Student account:**
   - Email: student@example.com
   - Password: Password123

2. **Teacher account:**
   - Email: teacher@example.com
   - Password: Password123

3. **Admin account:**
   - Email: admin@example.com
   - Password: Password123
   (Note: Admin account must be created directly in MongoDB)

## Build & Deployment

### Frontend Build
```bash
npm run build
npm run start
```

### Backend Deployment
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export MONGODB_URI="your-connection-string"
export JWT_SECRET_KEY="your-secret"

# Run with production server (e.g., Gunicorn)
gunicorn -w 4 -b 0.0.0.0:5000 'app.factory:create_app()'
```

## Fixed Issues

✅ React warning - Fixed navigation during render in Login/Register pages (moved to useEffect)
✅ Missing routes - Created all missing pages (/profile, /teach/my-courses, /teach/create-course, /teach/students)
✅ API endpoints - Fixed all dashboard API calls to use correct backend endpoints
✅ Token persistence - Added token storage to login and register methods
✅ Optional imports - Made dotenv and motor imports optional for flexibility
✅ Endpoint corrections - Fixed all frontend API calls to use correct URLs with environment variables

## Development Workflow

1. **Start both servers:**
   - Terminal 1: `npm run dev` (Frontend on port 3000)
   - Terminal 2: `cd backend && bash start.sh` (Backend on port 5000)

2. **Register new account:**
   - Go to http://localhost:3000/auth/register
   - Choose role (Student/Teacher)
   - Submit

3. **Login:**
   - Go to http://localhost:3000/auth/login
   - Use registered credentials

4. **Access dashboard:**
   - Redirects to role-specific dashboard
   - Student: See enrolled courses and progress
   - Teacher: See created courses and students
   - Admin: See system analytics

## Troubleshooting

### "Failed to fetch" error
- Ensure backend is running on port 5000
- Check `NEXT_PUBLIC_API_URL` environment variable
- Verify MongoDB connection

### 404 errors on API calls
- Check backend endpoint paths match frontend calls
- Verify JWT token is included in headers
- Check CORS configuration

### React warnings about rendering during navigation
- All fixed - navigation now happens in useEffect

### Missing routes/pages
- All routes are now created and available
- Check that all page.tsx files exist

## Submission Checklist

- [ ] Frontend builds without errors: `npm run build`
- [ ] All routes work: `/`, `/auth/login`, `/auth/register`, `/dashboard`, `/profile`, `/teach/*`
- [ ] Authentication flow works: Registration → Login → Dashboard
- [ ] Role-based dashboards display correctly
- [ ] API calls succeed with proper error handling
- [ ] No React warnings in console
- [ ] No TypeScript errors
- [ ] Environment variables properly configured
- [ ] Backend starts with proper MongoDB connection

## Support

For issues or questions, refer to:
- Frontend docs: [Next.js](https://nextjs.org)
- Backend docs: [Flask](https://flask.palletsprojects.com)
- Database: [MongoDB](https://docs.mongodb.com)
