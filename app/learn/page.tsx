'use client'

import Link from 'next/link'
import { useState, useEffect } from 'react'
import { useAuth } from '@/contexts/auth-context'
import { useRouter } from 'next/navigation'

interface Course {
  id: string
  title: string
  description: string
  category: string
  level: string
  instructor_id: string
  status: string
}

export default function LearnPage() {
  const { isAuthenticated } = useAuth()
  const router = useRouter()
  const [courses, setCourses] = useState<Course[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [selectedLevel, setSelectedLevel] = useState('all')

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/auth/login')
      return
    }

    const loadCourses = async () => {
      try {
        const url = new URL('/api/courses', window.location.origin)
        if (selectedCategory !== 'all') url.searchParams.append('category', selectedCategory)
        if (selectedLevel !== 'all') url.searchParams.append('level', selectedLevel)

        const response = await fetch(url.toString())
        if (response.ok) {
          const data = await response.json()
          setCourses(data.data || [])
        }
      } catch (error) {
        console.error('[v0] Failed to load courses:', error)
      } finally {
        setLoading(false)
      }
    }

    loadCourses()
  }, [isAuthenticated, selectedCategory, selectedLevel, router])

  return (
    <main className="min-h-screen bg-background">
      {/* Header */}
      <div className="border-b border-border bg-card">
        <div className="max-w-6xl mx-auto px-6 py-8">
          <div className="flex items-center justify-between mb-4">
            <h1 className="text-3xl font-bold">Explore Courses</h1>
            <Link
              href="/dashboard"
              className="text-sm font-medium text-primary hover:underline"
            >
              Back to Dashboard
            </Link>
          </div>
          <p className="text-muted-foreground">Choose from our selection of tech courses and start learning</p>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-6xl mx-auto px-6 py-8">
        <div className="grid lg:grid-cols-4 gap-8">
          {/* Filters Sidebar */}
          <div className="lg:col-span-1">
            <div className="sticky top-8 space-y-6">
              {/* Category Filter */}
              <div className="bg-card rounded-lg p-4 border border-border">
                <h3 className="font-semibold mb-3">Category</h3>
                <div className="space-y-2">
                  {['all', 'web', 'mobile', 'data', 'devops', 'security'].map((cat) => (
                    <label key={cat} className="flex items-center gap-2 cursor-pointer hover:opacity-80">
                      <input
                        type="radio"
                        name="category"
                        value={cat}
                        checked={selectedCategory === cat}
                        onChange={(e) => setSelectedCategory(e.target.value)}
                        className="w-4 h-4"
                      />
                      <span className="text-sm capitalize">{cat === 'all' ? 'All Courses' : cat}</span>
                    </label>
                  ))}
                </div>
              </div>

              {/* Level Filter */}
              <div className="bg-card rounded-lg p-4 border border-border">
                <h3 className="font-semibold mb-3">Level</h3>
                <div className="space-y-2">
                  {['all', 'beginner', 'intermediate', 'advanced'].map((lev) => (
                    <label key={lev} className="flex items-center gap-2 cursor-pointer hover:opacity-80">
                      <input
                        type="radio"
                        name="level"
                        value={lev}
                        checked={selectedLevel === lev}
                        onChange={(e) => setSelectedLevel(e.target.value)}
                        className="w-4 h-4"
                      />
                      <span className="text-sm capitalize">{lev === 'all' ? 'All Levels' : lev}</span>
                    </label>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Courses Grid */}
          <div className="lg:col-span-3">
            {loading ? (
              <div className="text-center py-12">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
                <p className="text-muted-foreground">Loading courses...</p>
              </div>
            ) : courses.length > 0 ? (
              <div className="grid md:grid-cols-2 gap-6">
                {courses.map((course) => (
                  <Link
                    key={course.id}
                    href={`/learn/${course.id}`}
                    className="bg-card rounded-lg border border-border overflow-hidden hover:shadow-lg hover:border-primary/50 transition-all group"
                  >
                    {/* Course Header */}
                    <div className="h-40 bg-gradient-to-br from-primary/20 to-primary/5 flex items-center justify-center group-hover:from-primary/30 group-hover:to-primary/10 transition-colors">
                      <div className="text-center">
                        <div className="text-4xl mb-2">📚</div>
                        <p className="text-sm text-muted-foreground">{course.category}</p>
                      </div>
                    </div>

                    {/* Course Content */}
                    <div className="p-6 space-y-4">
                      <div>
                        <h3 className="font-semibold line-clamp-2 mb-2">{course.title}</h3>
                        <p className="text-sm text-muted-foreground line-clamp-2">{course.description}</p>
                      </div>

                      <div className="flex items-center justify-between">
                        <div className="flex gap-2">
                          <span className="inline-block bg-primary/10 text-primary text-xs font-medium rounded px-2 py-1 capitalize">
                            {course.level}
                          </span>
                          {course.status === 'published' && (
                            <span className="inline-block bg-green-100 dark:bg-green-900 text-green-900 dark:text-green-100 text-xs font-medium rounded px-2 py-1">
                              Available
                            </span>
                          )}
                        </div>
                      </div>

                      <button className="w-full bg-primary text-primary-foreground rounded py-2 text-sm font-medium hover:bg-primary/90 transition-colors group-hover:bg-primary/95">
                        View Course
                      </button>
                    </div>
                  </Link>
                ))}
              </div>
            ) : (
              <div className="bg-muted/30 rounded-lg p-12 text-center border border-border border-dashed">
                <p className="text-muted-foreground mb-4">No courses found</p>
                <button
                  onClick={() => {
                    setSelectedCategory('all')
                    setSelectedLevel('all')
                  }}
                  className="text-sm font-medium text-primary hover:underline"
                >
                  Clear filters
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </main>
  )
}
