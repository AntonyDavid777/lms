'use client'

import { useAuth } from '@/contexts/auth-context'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { StudentDashboard } from '@/components/dashboard/student-dashboard'
import { TeacherDashboard } from '@/components/dashboard/teacher-dashboard'
import { AdminDashboard } from '@/components/dashboard/admin-dashboard'
import { UserRole } from '@/types'

export default function DashboardPage() {
  const { user, isAuthenticated, isLoading } = useAuth()
  const router = useRouter()

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

  if (!isAuthenticated) {
    router.push('/auth/login')
    return null
  }

  return (
    <main className="min-h-screen bg-background">
      {/* Top Navigation */}
      <nav className="flex items-center justify-between border-b border-border px-6 py-4">
        <Link href="/" className="flex items-center gap-2 hover:opacity-80 transition-opacity">
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

        <div className="flex items-center gap-2 sm:gap-4">
          <span className="text-sm text-muted-foreground hidden sm:inline">{user?.name}</span>
          {user?.role === UserRole.TEACHER && (
            <>
              <Link
                href="/teach/my-courses"
                className="inline-flex items-center justify-center rounded-lg border border-border px-4 py-2 text-sm font-medium hover:bg-muted transition-colors"
              >
                My Courses
              </Link>
              <Link
                href="/teach/students"
                className="inline-flex items-center justify-center rounded-lg border border-border px-4 py-2 text-sm font-medium hover:bg-muted transition-colors"
              >
                Students
              </Link>
            </>
          )}
          <Link
            href="/profile"
            className="inline-flex items-center justify-center rounded-lg border border-border px-4 py-2 text-sm font-medium hover:bg-muted transition-colors"
          >
            Profile
          </Link>
        </div>
      </nav>

      {/* Main Content */}
      <div className="px-6 py-8">
        <div className="mx-auto max-w-6xl">
          {/* Render role-specific dashboard */}
          {user?.role === UserRole.STUDENT && <StudentDashboard />}
          {user?.role === UserRole.TEACHER && <TeacherDashboard />}
          {user?.role === UserRole.ADMIN && <AdminDashboard />}
        </div>
      </div>
    </main>
  )
}
