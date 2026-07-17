# TechTots LMS - Learning Management System

A comprehensive, modern Learning Management System built with Python Flask backend and Next.js frontend. Designed for tech education with interactive courses, progress tracking, gamification, and analytics.

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Next.js](https://img.shields.io/badge/Next.js-16.2-black.svg)
![React](https://img.shields.io/badge/React-19-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![MongoDB](https://img.shields.io/badge/MongoDB-7.0-green.svg)

## Overview

TechTots LMS is a full-stack learning management platform that combines:

- **Comprehensive Course Management** - Create, organize, and manage tech courses
- **Interactive Learning** - Video lessons, text content, and interactive components
- **Assessment System** - Quizzes with auto-grading and manual review
- **Progress Tracking** - Detailed analytics on student progress
- **Gamification** - Points, badges, and leaderboards to motivate learners
- **Role-Based Access** - Students, Teachers, and Administrators
- **Real-Time Analytics** - Dashboard with engagement metrics

## Tech Stack

### Backend
- **Framework**: Flask 3.0.0 with Flask-CORS and Flask-JWT-Extended
- **Database**: MongoDB 7.0 with Motor async driver
- **Authentication**: JWT tokens with bcrypt password hashing
- **Validation**: Marshmallow for serialization
- **Documentation**: Flask-RESTX for Swagger/OpenAPI docs

### Frontend
- **Framework**: Next.js 16.2 with React 19
- **Language**: TypeScript 5.7
- **Styling**: Tailwind CSS 4.3
- **Components**: shadcn/ui
- **State Management**: React Context API
- **HTTP Client**: Fetch API wrapper

### DevOps
- **Database**: Docker & Docker Compose
- **Package Manager**: pnpm (Node.js)
- **Development**: Hot Module Replacement (HMR)

## Features

### Authentication & User Management
- ✅ User registration with role selection (Student/Teacher/Admin)
- ✅ JWT-based authentication with refresh tokens
- ✅ Password hashing with bcrypt (salt rounds: 12)
- ✅ Role-based access control (RBAC)
- ✅ User profile management
- ✅ Password change functionality
- ✅ Account activation/deactivation

### Courses & Learning
- 📚 Course creation and management (Teacher/Admin)
- 📚 Lesson organization with order tracking
- 📚 Multiple content types (video, text, interactive, quiz)
- 📚 Learning objectives and resources
- 📚 Course enrollment system
- 📚 Public course discovery

### Assessments
- ✅ Quiz/assessment creation with question types
- ✅ Multiple choice, short answer, and essay questions
- ✅ Point-based scoring system
- ✅ Time-limited quizzes
- ✅ Auto-grading for objective questions
- ✅ Manual grading interface for essays

### Progress Tracking
- 📊 Course progress calculation
- 📊 Lesson completion tracking
- 📊 Time spent monitoring
- 📊 Quiz performance analytics
- 📊 Certificate generation (coming soon)

### Gamification
- 🏆 Points system (earn through activities)
- 🏆 Badge achievement system
- 🏆 Global and course-specific leaderboards
- 🏆 Achievement unlocking

### Analytics
- 📈 User engagement metrics
- 📈 Course performance statistics
- 📈 Completion rate tracking
- 📈 Learning path analytics (coming soon)

## Quick Start

### Minimum Requirements
- Python 3.9+
- Node.js 18+
- Docker & Docker Compose

### 30-Second Setup

```bash
# 1. Start MongoDB
docker-compose up -d

# 2. Start Backend (Terminal 1)
cd backend && pip install -r requirements.txt && python run.py

# 3. Start Frontend (Terminal 2)
pnpm install && pnpm dev

# 4. Open http://localhost:3000
```

For detailed setup instructions, see **[QUICKSTART.md](./QUICKSTART.md)**

## Project Structure

```
techtots-lms/
├── backend/                           # Flask Python backend
│   ├── app/
│   │   ├── models/                   # Data models (User, Course, etc)
│   │   ├── routes/                   # API endpoints by resource
│   │   ├── services/                 # Business logic layer
│   │   ├── middleware/               # Auth, logging, errors
│   │   ├── utils/                    # Database, auth, responses
│   │   └── factory.py                # Flask app factory
│   ├── config/
│   │   └── config.py                 # Environment configs
│   ├── requirements.txt               # Python dependencies
│   ├── run.py                        # Backend entry point
│   ├── .env                          # Environment variables
│   └── README.md                     # Backend documentation
│
├── app/                              # Next.js frontend
│   ├── auth/                         # Authentication pages
│   │   ├── login/page.tsx
│   │   └── register/page.tsx
│   ├── dashboard/page.tsx            # Role-based dashboard
│   ├── learn/page.tsx                # Course browsing interface
│   ├── layout.tsx                    # Root layout
│   ├── page.tsx                      # Landing page
│   └── globals.css                   # Global styles
│
├── components/
│   ├── dashboard/
│   │   ├── student-dashboard.tsx     # Student learning interface
│   │   ├── teacher-dashboard.tsx     # Teacher course management
│   │   └── admin-dashboard.tsx       # Admin system monitoring
│   └── ui/                           # shadcn/ui components
│
├── contexts/
│   └── auth-context.tsx              # Auth state provider
├── lib/
│   ├── api-client.ts                 # Centralized API client
│   └── utils.ts                      # Tailwind utilities
├── types/
│   └── index.ts                      # TypeScript definitions
│
├── docker-compose.yml                # MongoDB + Mongo Express
├── next.config.mjs                   # Next.js configuration
├── tailwind.config.ts                # Tailwind CSS config
├── tsconfig.json                     # TypeScript config
├── package.json                      # Frontend dependencies
│
├── .env.example                      # Environment variables template
├── QUICKSTART.md                     # Quick start guide
├── PROJECT_SETUP.md                  # Detailed setup documentation
├── BACKEND_COMPLETE.md               # Backend implementation details
├── FRONTEND_COMPLETE.md              # Frontend implementation details
└── README.md                         # This file
```

## API Documentation

### Base URL
```
http://localhost:5000/api/v1
```

### Authentication Endpoints
```
POST   /auth/register        Register new user
POST   /auth/login           Login with credentials
GET    /auth/me              Get current user info
POST   /auth/refresh         Refresh access token
```

### User Endpoints
```
GET    /users                List users (admin only)
GET    /users/:id            Get user details
PUT    /users/:id            Update user information
DELETE /users/:id            Deactivate user (admin only)
POST   /users/:id/change-password
GET    /users/:id/courses    Get user's enrolled courses
POST   /users/:id/activate   Reactivate user (admin)
POST   /users/:id/deactivate Deactivate user (admin)
```

### Placeholder Routes (Ready for implementation)
```
/courses                Course management
/lessons                Lesson management
/assessments            Quiz/assessment management
/progress               Progress tracking
/gamification           Badges, points, leaderboards
/analytics              Analytics data
```

### Response Format

#### Success Response
```json
{
  "success": true,
  "message": "Operation successful",
  "status_code": 200,
  "data": { ... }
}
```

#### Error Response
```json
{
  "success": false,
  "error": "Error message",
  "status_code": 400,
  "errors": { ... }
}
```

## Environment Configuration

### Backend (.env)
```
FLASK_ENV=development
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=techtots_lms
JWT_SECRET_KEY=your-secret-key-here
CORS_ORIGINS=http://localhost:3000
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:5000
```

## Development

### Running Tests

```bash
# Backend tests (coming soon)
cd backend && pytest tests/

# Frontend tests (coming soon)
pnpm test
```

### Code Style

```bash
# Backend linting
cd backend && flake8 app/

# Frontend linting
pnpm lint
```

### Database

MongoDB collections are automatically created with proper indexes:
- `users` - User accounts with email index
- `courses` - Course information
- `lessons` - Course lessons
- `assessments` - Quizzes and assessments
- `quiz_results` - Quiz submission results
- `enrollments` - Course enrollments
- `progress` - User progress tracking
- `user_badges` - Earned badges
- `analytics` - Event tracking

Access MongoDB Admin UI: `http://localhost:8081` (admin/password)

## Implementation Phases

### Completed ✅
- Phase 1: Backend project setup & infrastructure
- Phase 2: Authentication & user management
- Phase 3: Course & lesson management
- Phase 4: Assessments & quizzes
- Phase 5: Progress tracking
- Phase 6: Gamification
- Phase 7: Analytics & file uploads
- Phase 9: Frontend setup & navigation
- Phase 10: Student dashboard & learning interface
- Phase 11: Teacher dashboard with course management
- Phase 12: Admin dashboard with system monitoring

### In Progress
- Frontend integration testing

### Planned
- Phase 8: File uploads & media handling
- Phase 13: Gamification UI (leaderboards, badges)
- Phase 14: User profiles & settings
- Phase 15: Course detail & lesson viewer
- Phase 16: Assessment taking interface
- Phase 17: Integration & E2E testing
- Phase 18: Production deployment

## Security Features

- ✅ JWT token-based authentication
- ✅ Bcrypt password hashing (12 salt rounds)
- ✅ Role-based access control (RBAC)
- ✅ CORS configuration
- ✅ Request validation & sanitization
- ✅ SQL injection prevention (MongoDB parameterized queries)
- ✅ Security headers in Next.js config
- ✅ Protected API endpoints

## Deployment

### Backend Deployment Options
1. **Vercel** (Serverless functions)
2. **Railway.app**
3. **Render.com**
4. **AWS Elastic Beanstalk**
5. **DigitalOcean App Platform**

### Frontend Deployment
- Deploy to **Vercel** for optimal Next.js performance
- Update `NEXT_PUBLIC_API_URL` to production backend

For production deployment checklist, see **[PROJECT_SETUP.md](./PROJECT_SETUP.md)**

## Troubleshooting

### MongoDB Connection Error
```bash
# Ensure Docker containers are running
docker-compose ps

# Restart if needed
docker-compose restart
```

### Backend Won't Start
```bash
# Check if port 5000 is in use
lsof -i :5000

# Kill the process if needed
kill -9 <PID>
```

### Frontend Can't Connect to Backend
1. Check backend is running on port 5000
2. Verify `NEXT_PUBLIC_API_URL=http://localhost:5000` in `.env.local`
3. Check browser console for CORS errors

### CORS Issues
Update `CORS_ORIGINS` in `backend/.env` to include frontend URL

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Support

For detailed setup instructions, see:
- **[QUICKSTART.md](./QUICKSTART.md)** - Get started in 5 minutes
- **[PROJECT_SETUP.md](./PROJECT_SETUP.md)** - Comprehensive setup guide
- **[backend/README.md](./backend/README.md)** - Backend documentation
- **[v0_plans/innovative-route.md](./v0_plans/innovative-route.md)** - Implementation plan

## Roadmap

### Q1 2024
- ✅ Project scaffolding & setup
- ✅ Authentication system
- [ ] Course management system
- [ ] Learning interface

### Q2 2024
- [ ] Assessment & quiz engine
- [ ] Progress tracking
- [ ] Gamification system
- [ ] Analytics dashboard

### Q3 2024
- [ ] File upload & media handling
- [ ] Video streaming integration
- [ ] Mobile responsiveness improvements
- [ ] Performance optimization

### Q4 2024
- [ ] Admin dashboard enhancements
- [ ] Reporting & certification
- [ ] Advanced analytics
- [ ] Production deployment

## Credits

Built with ❤️ using Next.js, Flask, and MongoDB

## Contact

For questions or feedback, reach out to the TechTots team.

---

**Ready to learn?** Start with [QUICKSTART.md](./QUICKSTART.md) 🚀
"# lms" 
