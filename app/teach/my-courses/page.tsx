'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { useAuth } from '@/contexts/auth-context'
import { apiClient } from '@/lib/api-client'
import { UserRole } from '@/types'

export default function MyCoursesPage() {
  const router = useRouter()
  const { user, isAuthenticated, isLoading } = useAuth()
  const [courses, setCourses] = useState<any[]>([])
  const [isLoadingCourses, setIsLoadingCourses] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/auth/login')
    }
  }, [isAuthenticated, isLoading, router])

  useEffect(() => {
    if (!isLoading && isAuthenticated && user?.role === UserRole.TEACHER) {
      loadCourses()
    }
  }, [isLoading, isAuthenticated, user])

  const loadCourses = async () => {
    setIsLoadingCourses(true)
    setError(null)

    try {
      const response = await apiClient.listCourses(1, 100) as any
      setCourses(response?.data || [])
    } catch (err: any) {
      setError(err.message || 'Failed to load courses')
    } finally {
      setIsLoadingCourses(false)
    }
  }

  if (isLoading) {
    return (
      <main className="flex min-h-screen items-center justify-center">
        <div className="text-center">
          <div className="mb-4 inline-block h-8 w-8 animate-spin rounded-full border-4 border-border border-t-primary" />
          <p className="text-muted-foreground">Loading...</p>
        </div>
      </main>
    )
  }

  if (!isAuthenticated || user?.role !== UserRole.TEACHER) {
    return (
      <main className="flex min-h-screen items-center justify-center">
        <div className="text-center">
          <p className="text-red-600">Access denied. Teachers only.</p>
          <Link href="/dashboard" className="mt-4 inline-block text-primary hover:underline">
            Go back to dashboard
          </Link>
        </div>
      </main>
    )
  }

  return (
    <main className="min-h-screen bg-background">
      {/* Navigation */}
      <nav className="flex items-center justify-between border-b border-border px-6 py-4">
        <Link href="/dashboard" className="flex items-center gap-2 hover:opacity-80 transition-opacity">
          <svg
            className="h-8 w-8 text-primary"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={2}
          >
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 6.253v13m0-13C6.228 6.253 2 10.66 2 16s4.228 9.747 10 9.747c5.771 0 10-4.374 10-9.747 0-5.34-4.228-9.747-10-9.747z" />
          </svg>
          <h1 className="text-xl font-bold">TechTots</h1>
        </Link>

        <div className="flex items-center gap-4">
          <Link
            href="/teach/create-course"
            className="inline-flex items-center justify-center rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90 transition-colors"
          >
            Create Course
          </Link>
          <Link
            href="/profile"
            className="inline-flex items-center justify-center rounded-lg border border-border px-4 py-2 text-sm font-medium hover:bg-muted transition-colors"
          >
            Profile
          </Link>
        </div>
      </nav>

      {/* Content */}
      <div className="px-6 py-8">
        <div className="mx-auto max-w-6xl">
          <h2 className="mb-6 text-2xl font-bold">My Courses</h2>

          {error && (
            <div className="mb-4 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700 dark:border-red-900 dark:bg-red-900/20 dark:text-red-400">
              {error}
            </div>
          )}

          {isLoadingCourses ? (
            <div className="flex justify-center py-12">
              <div className="text-center">
                <div className="mb-4 inline-block h-8 w-8 animate-spin rounded-full border-4 border-border border-t-primary" />
                <p className="text-muted-foreground">Loading courses...</p>
              </div>
            </div>
          ) : courses.length === 0 ? (
            <div className="rounded-lg border border-border bg-muted/30 p-12 text-center">
              <p className="mb-4 text-muted-foreground">You haven&apos;t created any courses yet.</p>
              <Link
                href="/teach/create-course"
                className="inline-flex items-center justify-center rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90 transition-colors"
              >
                Create Your First Course
              </Link>
            </div>
          ) : (
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {courses.map((course) => (
                <div key={course._id} className="rounded-lg border border-border bg-background p-6 hover:shadow-lg transition-shadow">
                  {course.thumbnail_url && (
                    <img
                      src={course.thumbnail_url}
                      alt={course.title}
                      className="mb-4 h-40 w-full rounded-lg object-cover"
                    />
                  )}
                  <h3 className="mb-2 text-lg font-semibold">{course.title}</h3>
                  <p className="mb-4 text-sm text-muted-foreground line-clamp-2">{course.description}</p>
                  <div className="mb-4 flex items-center justify-between text-sm">
                    <span className="capitalize text-xs bg-primary/10 text-primary px-2 py-1 rounded">
                      {course.level}
                    </span>
                    <span className="text-muted-foreground">{course.lessons_count || 0} lessons</span>
                  </div>
                  <div className="flex gap-2">
                    <Link
                      href={`/teach/courses/${course._id}`}
                      className="flex-1 rounded-lg bg-primary px-3 py-2 text-center text-sm font-medium text-primary-foreground hover:bg-primary/90 transition-colors"
                    >
                      Manage
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </main>
  )
}
