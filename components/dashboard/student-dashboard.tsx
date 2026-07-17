'use client'

import { useAuth } from '@/contexts/auth-context'
import Link from 'next/link'
import { useState, useEffect } from 'react'

interface CourseProgress {
  id: string
  course_id: string
  total_lessons: number
  completed_lessons: number
  overall_progress: number
  last_accessed: string
}

interface StudentStats {
  total_courses: number
  courses_in_progress: number
  courses_completed: number
  total_points: number
  current_streak: number
  badges_earned: number
}

export function StudentDashboard() {
  const { user } = useAuth()
  const [stats, setStats] = useState<StudentStats>({
    total_courses: 0,
    courses_in_progress: 0,
    courses_completed: 0,
    total_points: 0,
    current_streak: 0,
    badges_earned: 0,
  })
  const [coursesProgress, setCoursesProgress] = useState<CourseProgress[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadDashboardData = async () => {
      try {
        // Fetch courses progress
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'
        const response = await fetch(`${apiUrl}/api/v1/progress/courses`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          },
        })
        if (response.ok) {
          const data = await response.json()
          setCoursesProgress(data.data || [])

          // Calculate stats from courses
          const total = data.data?.length || 0
          const inProgress = data.data?.filter((c: any) => c.overall_progress < 100).length || 0
          const completed = data.data?.filter((c: any) => c.overall_progress === 100).length || 0

          setStats((prev) => ({
            ...prev,
            total_courses: total,
            courses_in_progress: inProgress,
            courses_completed: completed,
          }))
        }
      } catch (error) {
        console.error('[v0] Failed to load dashboard data:', error)
      } finally {
        setLoading(false)
      }
    }

    if (user) {
      loadDashboardData()
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
        <h1 className="text-3xl font-bold mb-2">Welcome back, {user?.name || 'Learner'}!</h1>
        <p className="text-muted-foreground">Keep up the momentum and continue your learning journey</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {[
          { label: 'Total Courses', value: stats.total_courses, icon: '📚' },
          { label: 'In Progress', value: stats.courses_in_progress, icon: '🚀' },
          { label: 'Completed', value: stats.courses_completed, icon: '✅' },
          { label: 'Total Points', value: stats.total_points, icon: '⭐' },
          { label: 'Current Streak', value: `${stats.current_streak} days`, icon: '🔥' },
          { label: 'Badges Earned', value: stats.badges_earned, icon: '🏆' },
        ].map((stat) => (
          <div key={stat.label} className="bg-card rounded-lg p-6 border border-border">
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm text-muted-foreground mb-1">{stat.label}</p>
                <p className="text-2xl font-bold">{stat.value}</p>
              </div>
              <span className="text-3xl">{stat.icon}</span>
            </div>
          </div>
        ))}
      </div>

      {/* Courses Section */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-2xl font-bold">My Courses</h2>
          <Link
            href="/learn"
            className="text-sm font-medium text-primary hover:underline"
          >
            Browse all courses
          </Link>
        </div>

        {coursesProgress.length > 0 ? (
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {coursesProgress.map((course) => (
              <div key={course.id} className="bg-card rounded-lg border border-border overflow-hidden hover:shadow-lg transition-shadow">
                <div className="p-6 space-y-4">
                  <div>
                    <h3 className="font-semibold line-clamp-2">Course {course.course_id.slice(0, 8)}</h3>
                    <p className="text-sm text-muted-foreground mt-1">
                      {course.completed_lessons} of {course.total_lessons} lessons completed
                    </p>
                  </div>

                  {/* Progress Bar */}
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-medium">Progress</span>
                      <span className="text-xs text-muted-foreground">{course.overall_progress}%</span>
                    </div>
                    <div className="w-full bg-muted rounded-full h-2">
                      <div
                        className="bg-primary h-2 rounded-full transition-all duration-300"
                        style={{ width: `${course.overall_progress}%` }}
                      />
                    </div>
                  </div>

                  <div className="text-xs text-muted-foreground">
                    Last accessed: {new Date(course.last_accessed).toLocaleDateString()}
                  </div>

                  <Link
                    href={`/learn/${course.course_id}`}
                    className="block w-full text-center bg-primary text-primary-foreground rounded px-4 py-2 text-sm font-medium hover:bg-primary/90 transition-colors"
                  >
                    Continue Learning
                  </Link>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="bg-muted/30 rounded-lg p-12 text-center border border-border border-dashed">
            <p className="text-muted-foreground mb-4">No courses enrolled yet</p>
            <Link
              href="/learn"
              className="inline-block bg-primary text-primary-foreground rounded px-6 py-2 font-medium hover:bg-primary/90 transition-colors"
            >
              Explore Courses
            </Link>
          </div>
        )}
      </div>

      {/* Quick Actions */}
      <div className="bg-card rounded-lg p-6 border border-border">
        <h3 className="font-semibold mb-4">Quick Actions</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          <Link
            href="/learn"
            className="flex items-center gap-3 p-3 rounded hover:bg-muted transition-colors"
          >
            <span className="text-xl">🔍</span>
            <span className="text-sm font-medium">Explore Courses</span>
          </Link>
          <Link
            href="/profile"
            className="flex items-center gap-3 p-3 rounded hover:bg-muted transition-colors"
          >
            <span className="text-xl">👤</span>
            <span className="text-sm font-medium">My Profile</span>
          </Link>
          <Link
            href="/profile"
            className="flex items-center gap-3 p-3 rounded hover:bg-muted transition-colors"
          >
            <span className="text-xl">📊</span>
            <span className="text-sm font-medium">My Analytics</span>
          </Link>
        </div>
      </div>
    </div>
  )
}
