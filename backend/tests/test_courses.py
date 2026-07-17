import pytest
from bson import ObjectId
from app.services.course_service import CourseService
from app.models.course import Course, Lesson, Enrollment
from app.utils.errors import NotFoundError, ConflictError


@pytest.fixture
def setup_service(db):
    """Setup course service for testing"""
    return CourseService(db)


class TestCourseOperations:
    """Test course CRUD operations"""
    
    def test_create_course(self, setup_service):
        """Test creating a new course"""
        instructor_id = str(ObjectId())
        
        course = setup_service.create_course(
            title="Python Basics",
            description="Learn Python programming from scratch",
            instructor_id=instructor_id,
            category="Programming",
            level="beginner"
        )
        
        assert course.title == "Python Basics"
        assert course.description == "Learn Python programming from scratch"
        assert str(course.instructor_id) == instructor_id
        assert course.category == "Programming"
        assert course.level == "beginner"
        assert course._id is not None
    
    def test_get_course_by_id(self, setup_service):
        """Test retrieving a course by ID"""
        instructor_id = str(ObjectId())
        
        created_course = setup_service.create_course(
            title="Advanced Python",
            description="Advanced Python techniques",
            instructor_id=instructor_id
        )
        
        retrieved_course = setup_service.get_course_by_id(str(created_course._id))
        
        assert retrieved_course.title == "Advanced Python"
        assert retrieved_course.description == "Advanced Python techniques"
    
    def test_get_nonexistent_course(self, setup_service):
        """Test retrieving a non-existent course raises error"""
        with pytest.raises(NotFoundError):
            setup_service.get_course_by_id(str(ObjectId()))
    
    def test_update_course(self, setup_service):
        """Test updating course information"""
        instructor_id = str(ObjectId())
        
        course = setup_service.create_course(
            title="Original Title",
            description="Original Description",
            instructor_id=instructor_id
        )
        
        updated = setup_service.update_course(
            str(course._id),
            title="Updated Title",
            category="New Category"
        )
        
        assert updated.title == "Updated Title"
        assert updated.description == "Original Description"
        assert updated.category == "New Category"
    
    def test_delete_course(self, setup_service):
        """Test deleting a course"""
        instructor_id = str(ObjectId())
        
        course = setup_service.create_course(
            title="To Delete",
            description="This course will be deleted",
            instructor_id=instructor_id
        )
        
        setup_service.delete_course(str(course._id))
        
        with pytest.raises(NotFoundError):
            setup_service.get_course_by_id(str(course._id))
    
    def test_list_courses(self, setup_service):
        """Test listing courses with pagination"""
        instructor_id = str(ObjectId())
        
        # Create multiple courses
        for i in range(15):
            setup_service.create_course(
                title=f"Course {i}",
                description=f"Description {i}",
                instructor_id=instructor_id,
                status="published" if i % 2 == 0 else "draft"
            )
        
        courses, total = setup_service.list_courses(page=1, page_size=10, status="published")
        
        assert len(courses) <= 10
        assert total >= 7  # At least half are published


class TestLessonOperations:
    """Test lesson CRUD operations"""
    
    def test_create_lesson(self, setup_service):
        """Test creating a new lesson"""
        instructor_id = str(ObjectId())
        course = setup_service.create_course(
            title="Test Course",
            description="Test Description",
            instructor_id=instructor_id
        )
        
        lesson = setup_service.create_lesson(
            title="Lesson 1",
            description="Introduction to Python",
            course_id=str(course._id),
            order=1,
            content="Python is a programming language...",
            content_type="text"
        )
        
        assert lesson.title == "Lesson 1"
        assert str(lesson.course_id) == str(course._id)
        assert lesson.order == 1
    
    def test_get_lesson_by_id(self, setup_service):
        """Test retrieving a lesson by ID"""
        instructor_id = str(ObjectId())
        course = setup_service.create_course(
            title="Test Course",
            description="Test Description",
            instructor_id=instructor_id
        )
        
        created_lesson = setup_service.create_lesson(
            title="Lesson 1",
            description="Description",
            course_id=str(course._id),
            order=1
        )
        
        retrieved_lesson = setup_service.get_lesson_by_id(str(created_lesson._id))
        
        assert retrieved_lesson.title == "Lesson 1"
    
    def test_update_lesson(self, setup_service):
        """Test updating lesson information"""
        instructor_id = str(ObjectId())
        course = setup_service.create_course(
            title="Test Course",
            description="Test Description",
            instructor_id=instructor_id
        )
        
        lesson = setup_service.create_lesson(
            title="Original Title",
            description="Original Description",
            course_id=str(course._id),
            order=1
        )
        
        updated = setup_service.update_lesson(
            str(lesson._id),
            title="Updated Title"
        )
        
        assert updated.title == "Updated Title"
    
    def test_delete_lesson(self, setup_service):
        """Test deleting a lesson"""
        instructor_id = str(ObjectId())
        course = setup_service.create_course(
            title="Test Course",
            description="Test Description",
            instructor_id=instructor_id
        )
        
        lesson = setup_service.create_lesson(
            title="To Delete",
            description="Description",
            course_id=str(course._id),
            order=1
        )
        
        setup_service.delete_lesson(str(lesson._id))
        
        with pytest.raises(NotFoundError):
            setup_service.get_lesson_by_id(str(lesson._id))
    
    def test_get_course_lessons(self, setup_service):
        """Test retrieving all lessons for a course"""
        instructor_id = str(ObjectId())
        course = setup_service.create_course(
            title="Test Course",
            description="Test Description",
            instructor_id=instructor_id
        )
        
        # Create multiple lessons
        for i in range(5):
            setup_service.create_lesson(
                title=f"Lesson {i+1}",
                description=f"Description {i+1}",
                course_id=str(course._id),
                order=i+1
            )
        
        lessons = setup_service.get_course_lessons(str(course._id))
        
        assert len(lessons) == 5
        # Check ordering
        for i, lesson in enumerate(lessons):
            assert lesson.order == i + 1


class TestEnrollmentOperations:
    """Test enrollment operations"""
    
    def test_enroll_student(self, setup_service):
        """Test enrolling a student in a course"""
        instructor_id = str(ObjectId())
        student_id = str(ObjectId())
        
        course = setup_service.create_course(
            title="Test Course",
            description="Test Description",
            instructor_id=instructor_id,
            status="published"
        )
        
        enrollment = setup_service.enroll_student(student_id, str(course._id))
        
        assert str(enrollment.user_id) == student_id
        assert str(enrollment.course_id) == str(course._id)
        assert enrollment.progress_percentage == 0.0
    
    def test_enroll_duplicate(self, setup_service):
        """Test enrolling a student twice raises error"""
        instructor_id = str(ObjectId())
        student_id = str(ObjectId())
        
        course = setup_service.create_course(
            title="Test Course",
            description="Test Description",
            instructor_id=instructor_id,
            status="published"
        )
        
        setup_service.enroll_student(student_id, str(course._id))
        
        with pytest.raises(ConflictError):
            setup_service.enroll_student(student_id, str(course._id))
    
    def test_unenroll_student(self, setup_service):
        """Test unenrolling a student from a course"""
        instructor_id = str(ObjectId())
        student_id = str(ObjectId())
        
        course = setup_service.create_course(
            title="Test Course",
            description="Test Description",
            instructor_id=instructor_id,
            status="published"
        )
        
        setup_service.enroll_student(student_id, str(course._id))
        setup_service.unenroll_student(student_id, str(course._id))
        
        with pytest.raises(NotFoundError):
            setup_service.unenroll_student(student_id, str(course._id))
    
    def test_get_student_enrollments(self, setup_service):
        """Test retrieving a student's enrollments"""
        instructor_id = str(ObjectId())
        student_id = str(ObjectId())
        
        # Create and enroll in multiple courses
        for i in range(3):
            course = setup_service.create_course(
                title=f"Course {i}",
                description=f"Description {i}",
                instructor_id=instructor_id,
                status="published"
            )
            setup_service.enroll_student(student_id, str(course._id))
        
        enrollments, total = setup_service.get_student_enrollments(student_id)
        
        assert len(enrollments) == 3
        assert total == 3
    
    def test_update_enrollment_progress(self, setup_service):
        """Test updating enrollment progress"""
        instructor_id = str(ObjectId())
        student_id = str(ObjectId())
        
        course = setup_service.create_course(
            title="Test Course",
            description="Test Description",
            instructor_id=instructor_id,
            status="published"
        )
        
        setup_service.enroll_student(student_id, str(course._id))
        setup_service.update_enrollment_progress(student_id, str(course._id), 50.0)
        
        enrollments, _ = setup_service.get_student_enrollments(student_id)
        assert enrollments[0].progress_percentage == 50.0
    
    def test_mark_course_completed(self, setup_service):
        """Test marking a course as completed"""
        instructor_id = str(ObjectId())
        student_id = str(ObjectId())
        
        course = setup_service.create_course(
            title="Test Course",
            description="Test Description",
            instructor_id=instructor_id,
            status="published"
        )
        
        setup_service.enroll_student(student_id, str(course._id))
        setup_service.mark_course_completed(student_id, str(course._id))
        
        enrollments, _ = setup_service.get_student_enrollments(student_id)
        assert enrollments[0].progress_percentage == 100.0
        assert enrollments[0].completed_at is not None
