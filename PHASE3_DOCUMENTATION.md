# Phase 3: Backend Course & Lesson Management

## Overview

Phase 3 implements the complete course and lesson management system for TechTots LMS. This phase enables instructors to create courses and lessons, allows students to enroll in courses, and provides tracking of enrollment and progress.

## Features Implemented

### 1. Course Management
- **Create Courses**: Teachers can create new courses with title, description, category, and level
- **Update Courses**: Edit course information (title, description, category, level, status, thumbnail)
- **Delete Courses**: Remove courses (cascades to delete related lessons and enrollments)
- **List Courses**: Browse published courses with pagination and filtering
- **Retrieve Course Details**: Get full course information including lessons

### 2. Lesson Management
- **Create Lessons**: Add lessons to courses with content, video URLs, and learning objectives
- **Update Lessons**: Edit lesson content and metadata
- **Delete Lessons**: Remove lessons from courses
- **Retrieve Lessons**: Get all lessons for a course ordered by sequence
- **Lesson Ordering**: Lessons are ordered sequentially within courses

### 3. Course Enrollment
- **Enroll Students**: Students can enroll in published courses
- **Unenroll Students**: Students can leave courses at any time
- **Prevent Duplicate Enrollments**: System prevents duplicate enrollments
- **View Enrollments**: Students can view their enrolled courses
- **Enrollment Tracking**: Track enrollment dates and completion status

### 4. Progress Tracking
- **Update Progress**: Track student progress percentage in courses
- **Mark Complete**: Mark courses as completed with timestamp
- **Get Enrollment Stats**: View student enrollments with pagination

## Data Models

### Course Model
```python
{
    "_id": ObjectId,
    "title": str,
    "description": str,
    "instructor_id": ObjectId,
    "category": str,
    "level": str,  # "beginner", "intermediate", "advanced"
    "status": str,  # "draft", "published", "archived"
    "thumbnail_url": str,
    "enrollment_count": int,
    "average_rating": float,
    "lesson_ids": [ObjectId],
    "created_at": datetime,
    "updated_at": datetime
}
```

### Lesson Model
```python
{
    "_id": ObjectId,
    "title": str,
    "description": str,
    "course_id": ObjectId,
    "order": int,
    "content_type": str,  # "text", "video", "interactive"
    "content": str,
    "video_url": str,
    "duration": int,  # in minutes
    "learning_objectives": [str],
    "resources_url": [str],
    "created_at": datetime,
    "updated_at": datetime
}
```

### Enrollment Model
```python
{
    "_id": ObjectId,
    "user_id": ObjectId,
    "course_id": ObjectId,
    "progress_percentage": float,
    "enrolled_at": datetime,
    "completed_at": datetime  # null if not completed
}
```

## API Endpoints

### Courses

#### List Courses
- **GET** `/api/v1/courses`
- **Query Parameters**: `page`, `page_size`, `category`, `level`, `search`
- **Authentication**: Optional (non-authenticated users see published only)
- **Response**: Paginated list of courses

#### Get Course Details
- **GET** `/api/v1/courses/<course_id>`
- **Authentication**: Optional
- **Response**: Full course object with lessons

#### Create Course
- **POST** `/api/v1/courses`
- **Authentication**: Required (Teacher or Admin)
- **Body**: `{ title, description, category, level, thumbnail_url }`
- **Response**: Created course object

#### Update Course
- **PUT** `/api/v1/courses/<course_id>`
- **Authentication**: Required (Course creator or Admin)
- **Body**: Any course fields to update
- **Response**: Updated course object

#### Delete Course
- **DELETE** `/api/v1/courses/<course_id>`
- **Authentication**: Required (Course creator or Admin)
- **Response**: Success message

#### Enroll in Course
- **POST** `/api/v1/courses/<course_id>/enroll`
- **Authentication**: Required (Student)
- **Response**: Enrollment object

#### Unenroll from Course
- **DELETE** `/api/v1/courses/<course_id>/unenroll`
- **Authentication**: Required
- **Response**: Success message

#### Get Enrolled Students
- **GET** `/api/v1/courses/<course_id>/enrolled-students`
- **Authentication**: Required (Course creator or Admin)
- **Query Parameters**: `page`, `page_size`
- **Response**: Paginated list of enrollments

#### Get Course Lessons
- **GET** `/api/v1/courses/<course_id>/lessons`
- **Authentication**: Required
- **Response**: All lessons in course

#### Add Lesson to Course
- **POST** `/api/v1/courses/<course_id>/lessons`
- **Authentication**: Required (Course creator or Admin)
- **Body**: Lesson details
- **Response**: Created lesson object

### Lessons

#### Get Lesson
- **GET** `/api/v1/lessons/<lesson_id>`
- **Authentication**: Required
- **Response**: Lesson object

#### Update Lesson
- **PUT** `/api/v1/lessons/<lesson_id>`
- **Authentication**: Required (Course creator or Admin)
- **Body**: Any lesson fields to update
- **Response**: Updated lesson object

#### Delete Lesson
- **DELETE** `/api/v1/lessons/<lesson_id>`
- **Authentication**: Required (Course creator or Admin)
- **Response**: Success message

## Service Layer

### CourseService

Main business logic for course operations:

**Course Operations**
- `create_course()` - Create new course
- `get_course_by_id()` - Retrieve course
- `update_course()` - Update course
- `delete_course()` - Delete course and related data
- `list_courses()` - List with pagination and filters
- `get_courses_by_instructor()` - Get instructor's courses

**Lesson Operations**
- `create_lesson()` - Create lesson
- `get_lesson_by_id()` - Retrieve lesson
- `update_lesson()` - Update lesson
- `delete_lesson()` - Delete lesson
- `get_course_lessons()` - Get all lessons in course

**Enrollment Operations**
- `enroll_student()` - Enroll in course
- `unenroll_student()` - Remove enrollment
- `get_student_enrollments()` - Get student's courses
- `get_enrolled_students()` - Get course's students
- `update_enrollment_progress()` - Update progress
- `mark_course_completed()` - Mark course complete

## Database Indexes

Optimized indexes created for performance:

```python
# Courses
courses.create_index('instructor_id')
courses.create_index('category')
courses.create_index('status')
courses.create_index('created_at')

# Lessons
lessons.create_index('course_id')
lessons.create_index([('course_id', 1), ('order', 1)])

# Enrollments
enrollments.create_index([('user_id', 1), ('course_id', 1)], unique=True)
enrollments.create_index('user_id')
enrollments.create_index('course_id')
```

## Error Handling

Comprehensive error handling for:
- **NotFoundError**: Course/lesson/enrollment not found (404)
- **ValidationError**: Invalid input data (400)
- **ConflictError**: Duplicate enrollment (409)
- **Authorization**: Insufficient permissions (403)

## Testing

Comprehensive test suite in `tests/test_courses.py`:

**Course Tests**
- Create course
- Retrieve course
- Update course
- Delete course
- List courses with pagination

**Lesson Tests**
- Create lesson
- Retrieve lesson
- Update lesson
- Delete lesson
- List lessons for course

**Enrollment Tests**
- Enroll student
- Prevent duplicate enrollments
- Unenroll student
- Retrieve student enrollments
- Update progress
- Mark course complete

## Authorization & Security

- **Draft Courses**: Only instructor and admin can view
- **Published Courses**: Visible to all users
- **Lesson Management**: Only course instructor or admin
- **Enrollment**: Only students can enroll
- **Student List**: Only instructor and admin can view

## Next Steps (Phase 4)

The next phase will implement:
- **Assessments & Quizzes**: Quiz creation and management
- **Quiz Questions**: Different question types (multiple choice, short answer)
- **Assessment Scoring**: Automatic grading and result tracking

## Running Tests

```bash
pytest tests/test_courses.py -v
```

## Code Structure

```
backend/app/
├── models/
│   └── course.py          # Course, Lesson, Enrollment models
├── services/
│   └── course_service.py  # Business logic for courses
├── routes/
│   ├── courses.py         # Course endpoints
│   └── lessons.py         # Lesson endpoints
└── utils/
    └── database.py        # Database connection and indexes

tests/
└── test_courses.py        # Test suite
```

## Dependencies

Uses existing project dependencies:
- Flask for HTTP routing
- PyMongo for MongoDB operations
- JWT authentication via Flask-JWT-Extended
- CORS support via Flask-CORS

No new dependencies required for this phase.
