'use client'

import Link from 'next/link'
import { useAuth } from '@/contexts/auth-context'

export default function Page() {
  const { isAuthenticated, user } = useAuth()

  return (
    <main className="min-h-screen bg-background">
      {/* Navigation */}
      <nav className="flex items-center justify-between border-b border-border px-4 py-4 sm:px-6 lg:px-8">
        <div className="flex items-center gap-2">
          <svg
            className="h-8 w-8 text-primary"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={2}
          >
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 6.253v13m0-13C6.228 6.253 2 10.66 2 16s4.228 9.747 10 9.747c5.771 0 10-4.374 10-9.747 0-5.34-4.228-9.747-10-9.747z" />
          </svg>
          <h1 className="text-2xl font-bold">TechTots</h1>
        </div>

        <div className="flex gap-4">
          {isAuthenticated ? (
            <>
              <Link
                href="/dashboard"
                className="inline-flex items-center justify-center rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90 transition-colors"
              >
                Dashboard
              </Link>
              <Link
                href="/profile"
                className="inline-flex items-center justify-center rounded-lg border border-border px-4 py-2 text-sm font-medium hover:bg-muted transition-colors"
              >
                {user?.name || 'Profile'}
              </Link>
            </>
          ) : (
            <>
              <Link
                href="/auth/login"
                className="inline-flex items-center justify-center rounded-lg border border-border px-4 py-2 text-sm font-medium hover:bg-muted transition-colors"
              >
                Sign In
              </Link>
              <Link
                href="/auth/register"
                className="inline-flex items-center justify-center rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90 transition-colors"
              >
                Sign Up
              </Link>
            </>
          )}
        </div>
      </nav>

      {/* Hero Section */}
      <section className="flex flex-col items-center justify-center px-4 py-24 sm:py-32 lg:py-40">
        <div className="max-w-2xl text-center">
          <h2 className="mb-6 text-4xl font-bold tracking-tight sm:text-5xl lg:text-6xl">
            Learn, Grow, and Excel with TechTots
          </h2>
          <p className="mb-8 text-lg text-muted-foreground">
            Discover an innovative learning platform designed for tech enthusiasts. Access world-class courses, track your progress, earn badges, and join a thriving community of learners.
          </p>

          <div className="flex flex-col gap-4 sm:flex-row sm:justify-center">
            {!isAuthenticated && (
              <>
                <Link
                  href="/auth/register"
                  className="inline-flex items-center justify-center rounded-lg bg-primary px-6 py-3 text-base font-medium text-primary-foreground hover:bg-primary/90 transition-colors"
                >
                  Get Started Free
                </Link>
                <Link
                  href="/auth/login"
                  className="inline-flex items-center justify-center rounded-lg border border-border px-6 py-3 text-base font-medium hover:bg-muted transition-colors"
                >
                  Sign In
                </Link>
              </>
            )}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="border-t border-border bg-muted/30 px-4 py-24 sm:py-32 lg:px-8">
        <div className="mx-auto max-w-6xl">
          <h3 className="mb-12 text-center text-3xl font-bold">Why Choose TechTots?</h3>

          <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
            {features.map((feature) => (
              <div key={feature.title} className="rounded-lg border border-border bg-background p-6">
                <div className="mb-4 h-12 w-12 rounded-lg bg-primary/10 flex items-center justify-center text-2xl">
                  {feature.icon}
                </div>
                <h4 className="mb-2 text-lg font-semibold">{feature.title}</h4>
                <p className="text-sm text-muted-foreground">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="border-t border-border px-4 py-24 sm:py-32 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h3 className="mb-4 text-3xl font-bold">Ready to Start Learning?</h3>
          <p className="mb-8 text-lg text-muted-foreground">
            Join thousands of learners already on their journey to mastery.
          </p>
          {!isAuthenticated && (
            <Link
              href="/auth/register"
              className="inline-flex items-center justify-center rounded-lg bg-primary px-8 py-3 text-base font-medium text-primary-foreground hover:bg-primary/90 transition-colors"
            >
              Start Learning Today
            </Link>
          )}
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border bg-muted/50 px-4 py-8 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-6xl text-center text-sm text-muted-foreground">
          <p>&copy; {new Date().getFullYear()} TechTots LMS. All rights reserved.</p>
        </div>
      </footer>
    </main>
  )
}

const features = [
  {
    title: 'Comprehensive Courses',
    description: 'Access a wide range of tech courses covering everything from basics to advanced topics.',
    icon: '📚',
  },
  {
    title: 'Progress Tracking',
    description: 'Monitor your learning journey with detailed progress analytics and completion metrics.',
    icon: '📊',
  },
  {
    title: 'Gamification',
    description: 'Earn points, unlock badges, and climb leaderboards to stay motivated.',
    icon: '🏆',
  },
  {
    title: 'Interactive Quizzes',
    description: 'Test your knowledge with interactive assessments and get instant feedback.',
    icon: '✅',
  },
  {
    title: 'Community Support',
    description: 'Connect with fellow learners and instructors in our vibrant community.',
    icon: '👥',
  },
  {
    title: 'Flexible Learning',
    description: 'Learn at your own pace with flexible scheduling and on-demand content.',
    icon: '⏰',
  },
]
