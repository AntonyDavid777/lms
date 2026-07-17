# TechTots LMS - Quick Start Guide

Get the TechTots LMS running in 5 minutes!

## Prerequisites
- Python 3.9+
- Node.js 18+ (or pnpm/npm/yarn)
- Docker & Docker Compose (for MongoDB)

## Step 1: Start MongoDB

```bash
# From project root
docker-compose up -d

# Verify MongoDB is running
docker-compose ps
```

You can access Mongo Express at `http://localhost:8081`

## Step 2: Start the Backend

```bash
# Terminal 1: Backend
cd backend
pip install -r requirements.txt
python run.py
```

Backend will be available at `http://localhost:5000`

Test the backend:
```bash
curl http://localhost:5000/health
```

## Step 3: Start the Frontend

```bash
# Terminal 2: Frontend (from project root)
pnpm install  # or npm install
pnpm dev      # or npm run dev
```

Frontend will be available at `http://localhost:3000`

## Step 4: Test the Application

1. **Open browser** → `http://localhost:3000`
2. **Sign up** with test credentials:
   - Name: John Doe
   - Email: john@example.com
   - Password: TestPass123
   - Role: Student
3. **Log in** with those credentials
4. **Explore** the dashboard

## What's Ready to Use

### Authentication
- Register new users ✅
- Login with email/password ✅
- Session management with JWT tokens ✅
- Auto token refresh ✅

### User Management
- View user profiles ✅
- Update user information ✅
- Change password ✅
- View enrolled courses (placeholder) ✅

### API
- All endpoints have proper error handling ✅
- Request validation ✅
- Role-based access control ✅
- Pagination support ✅

## API Examples

### Register
```bash
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123",
    "name": "John Doe",
    "role": "student"
  }'
```

### Login
```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123"
  }'
```

### Get Current User
```bash
curl -X GET http://localhost:5000/api/v1/auth/me \
  -H "Authorization: Bearer <access_token>"
```

## Project Structure

```
techtots-lms/
├── backend/                    # Flask API
│   ├── app/
│   │   ├── models/            # Data models
│   │   ├── routes/            # API endpoints
│   │   ├── services/          # Business logic
│   │   ├── middleware/        # Auth, logging
│   │   └── utils/             # Helpers
│   ├── requirements.txt
│   ├── run.py                 # Start backend
│   └── README.md              # Backend docs
│
├── app/                       # Next.js frontend
│   ├── auth/                  # Auth pages
│   ├── dashboard/             # Dashboard pages
│   ├── layout.tsx
│   └── page.tsx               # Homepage
│
├── components/                # React components
├── contexts/                  # React contexts
├── lib/                       # Utilities & API client
├── types/                     # TypeScript types
│
├── docker-compose.yml         # MongoDB setup
├── package.json
├── next.config.mjs
├── tsconfig.json
├── tailwind.config.ts
└── PROJECT_SETUP.md           # Detailed setup guide
```

## Stopping Services

```bash
# Stop MongoDB
docker-compose down

# Stop all dev servers with Ctrl+C
```

## Common Issues

### "Connection refused" (Backend)
- Check MongoDB is running: `docker-compose ps`
- Restart: `docker-compose restart`

### "CORS error"
- Backend is running on 5000? Check `FLASK_PORT`
- Frontend env var set? Check `NEXT_PUBLIC_API_URL=http://localhost:5000`

### "Port already in use"
```bash
# Kill process using port
lsof -i :5000    # For backend
lsof -i :3000    # For frontend
kill -9 <PID>
```

### Database questions
- Connection: `mongodb://localhost:27017`
- Database: `techtots_lms`
- Admin: `admin` / `password`

## Next: What to Build

After exploring the app, here are the next phases:

1. **Courses & Lessons** - Create, manage, and enroll in courses
2. **Quizzes & Assessments** - Interactive quizzes with auto-grading
3. **Progress Tracking** - Monitor learning journey
4. **Gamification** - Points, badges, leaderboards
5. **Analytics** - Track engagement and performance

See `PROJECT_SETUP.md` for detailed implementation roadmap.

## Environment Files

### .env.local (Frontend)
```
NEXT_PUBLIC_API_URL=http://localhost:5000
```

### backend/.env
```
FLASK_ENV=development
MONGODB_URI=mongodb://localhost:27017
JWT_SECRET_KEY=dev-secret-key
```

## Getting Help

- Frontend code issues → See `app/` and `components/`
- Backend code issues → See `backend/app/`
- API integration → See `lib/api-client.ts`
- Type definitions → See `types/index.ts`

## Next Steps

1. ✅ Run the app (done!)
2. Test auth flow by signing up and logging in
3. Check browser console for any errors
4. Review `PROJECT_SETUP.md` for implementation details
5. Start implementing Phase 3 (Courses & Lessons)

Happy learning! 🚀
