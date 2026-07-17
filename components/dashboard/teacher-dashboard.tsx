'use client'

import { useAuth } from '@/contexts/auth-context'
import Link from 'next/link'
import { useState, useEffect } from 'react'

interface TeacherCourse {
  _id: string
  title: string
  description: string
  status: 'draft' | 'published' | 'archived'
  lessons_count: number
  students_enrolled: number
  created_at: string
}

interface TeacherStats {
  total_courses: number
  published_courses: number
  total_students: number
  total_lessons: number
  average_rating: number
}

export function TeacherDashboard() {
  const { user } = useAuth()
  const [stats, setStats] = useState<TeacherStats>({
    total_courses: 0,
    published_courses: 0,
    total_students: 0,
    total_lessons: 0,
    average_rating: 0,
  })
  const [courses, setCourses] = useState<TeacherCourse[]>([])
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState<'overview' | 'courses' | 'students'>('overview')

  useEffect(() => {
    const loadTeacherData = async () => {
      try {
        // Fetch courses created by teacher
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'
        const response = await fetch(`${apiUrl}/api/v1/courses`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          },
        })
        if (response.ok) {
          const data = await response.json()
          const teacherCourses = data.data || []
          setCourses(teacherCourses)

          // Calculate stats
          const published = teacherCourses.filter((c: any) => c.status === 'published').length
          const totalStudents = teacherCourses.reduce((sum: number, c: any) => sum + (c.students_enrolled || 0), 0)
          const totalLessons = teacherCourses.reduce((sum: number, c: any) => sum + (c.lessons_count || 0), 0)

          setStats({
            total_courses: teacherCourses.length,
            published_courses: published,
            total_students: totalStudents,
            total_lessons: totalLessons,
            average_rating: 4.5, // Placeholder
          })
        }
      } catch (error) {
        console.error('[v0] Failed to load teacher data:', error)
      } finally {
        setLoading(false)
      }
    }

    if (user) {
      loadTeacherData()
    }
  }, [user])

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading your dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-8 pb-8">
      {/* Welcome Header */}
      <div className="bg-gradient-to-r from-primary/10 to-primary/5 rounded-lg p-8 border border-border">
        <h1 className="text-3xl font-bold mb-2">Welcome back, {user?.name || 'Instructor'}!</h1>
        <p className="text-muted-foreground">Manage your courses, track student progress, and create engaging content</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        {[
          { label: 'Total Courses', value: stats.total_courses, icon: '📚' },
          { label: 'Published', value: stats.published_courses, icon: '✅' },
          { label: 'Students', value: stats.total_students, icon: '👥' },
          { label: 'Lessons', value: stats.total_lessons, icon: '📝' },
          { label: 'Rating', value: `${stats.average_rating}⭐`, icon: '⭐' },
        ].map((stat) => (
          <div key={stat.label} className="bg-card rounded-lg p-6 border border-border">
            <p className="text-xs text-muted-foreground uppercase tracking-wide mb-2">{stat.label}</p>
            <p className="text-2xl font-bold">{stat.value}</p>
          </div>
        ))}
      </div>

      {/* Tabs Navigation */}
      <div className="border-b border-border">
        <div className="flex gap-8">
          {(['overview', 'courses', 'students'] as const).map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-4 py-3 border-b-2 font-medium transition-colors capitalize ${
                activeTab === tab
                  ? 'border-primary text-primary'
                  : 'border-transparent text-muted-foreground hover:text-foreground'
              }`}
            >
              {tab}
            </button>
          ))}
        </div>
      </div>

      {/* Content Sections */}
      {activeTab === 'overview' && (
        <div className="space-y-6">
          {/* Quick Actions */}
          <div className="bg-card rounded-lg p-6 border border-border">
            <h3 className="font-semibold mb-4">Quick Actions</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              <Link
                href="/teach/create-course"
                className="flex items-center gap-3 p-3 rounded hover:bg-muted transition-colors border border-border"
              >
                <span className="text-xl">➕</span>
                <span className="font-medium">Create New Course</span>
              </Link>
              <Link
                href="/teach/my-courses"
                className="flex items-center gap-3 p-3 rounded hover:bg-muted transition-colors border border-border"
              >
                <span className="text-xl">📚</span>
                <span className="font-medium">Manage Courses</span>
              </Link>
              <Link
                href="/teach/students"
                className="flex items-center gap-3 p-3 rounded hover:bg-muted transition-colors border border-border"
              >
                <span className="text-xl">👥</span>
                <span className="font-medium">View Students</span>
              </Link>
              <Link
                href="/teach/analytics"
                className="flex items-center gap-3 p-3 rounded hover:bg-muted transition-colors border border-border"
              >
                <span className="text-xl">📊</span>
                <span className="font-medium">Analytics</span>
              </Link>
            </div>
          </div>

          {/* Recent Courses */}
          {courses.length > 0 && (
            <div>
              <h3 className="text-lg font-semibold mb-4">Recent Courses</h3>
              <div className="grid gap-4">
                {courses.slice(0, 3).map((course) => (
                  <div key={course._id} className="bg-card rounded-lg p-6 border border-border hover:shadow-lg transition-shadow">
                    <div className="flex items-start justify-between gap-4">
                      <div className="flex-1">
                        <h4 className="font-semibold line-clamp-2">{course.title}</h4>
                        <p className="text-sm text-muted-foreground mt-1 line-clamp-2">{course.description}</p>
                        <div className="flex gap-4 mt-3 text-sm text-muted-foreground">
                          <span>{course.lessons_count} lessons</span>
                          <span>{course.students_enrolled} students</span>
                          <span className={`px-2 py-1 rounded text-xs font-medium ${
                            course.status === 'published' ? 'bg-green-100 text-green-800' :
                            course.status === 'draft' ? 'bg-yellow-100 text-yellow-800' :
                            'bg-red-100 text-red-800'
                          }`}>
                            {course.status.charAt(0).toUpperCase() + course.status.slice(1)}
                          </span>
                        </div>
                      </div>
                      <Link
                        href={`/teach/courses/${course._id}`}
                        className="flex-shrink-0 text-primary hover:underline font-medium"
                      >
                        Edit →
                      </Link>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {activeTab === 'courses' && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold">My Courses</h3>
            <Link
              href="/teach/create-course"
              className="inline-flex items-center gap-2 bg-primary text-primary-foreground rounded px-4 py-2 text-sm font-medium hover:bg-primary/90 transition-colors"
            >
              <span>➕</span> New Course
            </Link>
          </div>

          {courses.length > 0 ? (
            <div className="grid gap-4">
              {courses.map((course) => (
                <div key={course._id} className="bg-card rounded-lg p-6 border border-border hover:shadow-lg transition-shadow">
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1">
                      <div className="flex items-center gap-3">
                        <h4 className="font-semibold text-lg">{course.title}</h4>
                        <span className={`px-2 py-1 rounded text-xs font-medium ${
                          course.status === 'published' ? 'bg-green-100 text-green-800' :
                          course.status === 'draft' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-red-100 text-red-800'
                        }`}>
                          {course.status.charAt(0).toUpperCase() + course.status.slice(1)}
                        </span>
                      </div>
                      <p className="text-sm text-muted-foreground mt-2 line-clamp-2">{course.description}</p>
                      <div className="flex gap-6 mt-4 text-sm text-muted-foreground">
                        <div className="flex items-center gap-2">
                          <span>📝</span>
                          <span>{course.lessons_count} lessons</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <span>👥</span>
                          <span>{course.students_enrolled} students enrolled</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <span>📅</span>
                          <span>{new Date(course.created_at).toLocaleDateString()}</span>
                        </div>
                      </div>
                    </div>
                    <div className="flex-shrink-0 flex gap-2">
                      <Link
                        href={`/teach/courses/${course._id}`}
                        className="px-3 py-2 bg-primary text-primary-foreground rounded text-sm font-medium hover:bg-primary/90 transition-colors"
                      >
                        Edit
                      </Link>
                      <Link
                        href={`/teach/courses/${course._id}/analytics`}
                        className="px-3 py-2 border border-border rounded text-sm font-medium hover:bg-muted transition-colors"
                      >
                        Analytics
                      </Link>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="bg-muted/30 rounded-lg p-12 text-center border border-border border-dashed">
              <p className="text-muted-foreground mb-4">No courses created yet</p>
              <Link
                href="/teach/create-course"
                className="inline-block bg-primary text-primary-foreground rounded px-6 py-2 font-medium hover:bg-primary/90 transition-colors"
              >
                Create Your First Course
              </Link>
            </div>
          )}
        </div>
      )}

      {activeTab === 'students' && (
        <div className="space-y-4">
          <h3 className="text-lg font-semibold">Student Management</h3>
          <div className="bg-card rounded-lg p-6 border border-border">
            <div className="text-center text-muted-foreground">
              <p className="mb-4">Total students enrolled across all courses: <span className="font-semibold text-foreground">{stats.total_students}</span></p>
              <p className="text-sm">Manage student progress, send messages, and track assignments</p>
            </div>
          </div>

          {courses.length > 0 && (
            <div className="space-y-4">
              <h4 className="font-semibold">Students by Course</h4>
              {courses.map((course) => (
                <div key={course._id} className="bg-card rounded-lg p-4 border border-border">
                  <div className="flex items-center justify-between">
                    <div>
                      <h5 className="font-medium">{course.title}</h5>
                      <p className="text-sm text-muted-foreground mt-1">{course.students_enrolled} enrolled students</p>
                    </div>
                    <Link
                      href={`/teach/courses/${course._id}/students`}
                      className="px-3 py-2 border border-border rounded text-sm font-medium hover:bg-muted transition-colors"
                    >
                      View Students
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )
}
