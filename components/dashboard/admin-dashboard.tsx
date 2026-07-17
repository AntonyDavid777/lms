'use client'

import { useAuth } from '@/contexts/auth-context'
import Link from 'next/link'
import { useState, useEffect } from 'react'

interface AdminStats {
  total_users: number
  total_students: number
  total_teachers: number
  total_admins: number
  total_courses: number
  total_enrollments: number
  total_assessments: number
  platform_health: 'good' | 'warning' | 'critical'
}

interface SystemMetrics {
  active_users_today: number
  new_users_this_week: number
  course_completion_rate: number
  average_assessment_score: number
}

export function AdminDashboard() {
  const { user } = useAuth()
  const [stats, setStats] = useState<AdminStats>({
    total_users: 0,
    total_students: 0,
    total_teachers: 0,
    total_admins: 0,
    total_courses: 0,
    total_enrollments: 0,
    total_assessments: 0,
    platform_health: 'good',
  })
  const [metrics, setMetrics] = useState<SystemMetrics>({
    active_users_today: 0,
    new_users_this_week: 0,
    course_completion_rate: 0,
    average_assessment_score: 0,
  })
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState<'overview' | 'users' | 'system' | 'moderation'>('overview')

  useEffect(() => {
    const loadAdminData = async () => {
      try {
        // Fetch analytics data
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'
        const response = await fetch(`${apiUrl}/api/v1/analytics/admin/dashboard`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          },
        })
        if (response.ok) {
          const data = await response.json()
          const analytics = data.data || {}
          
          setStats({
            total_users: analytics.total_users || 0,
            total_students: analytics.total_students || 0,
            total_teachers: analytics.total_teachers || 0,
            total_admins: analytics.total_admins || 0,
            total_courses: analytics.total_courses || 0,
            total_enrollments: analytics.total_enrollments || 0,
            total_assessments: analytics.total_assessments || 0,
            platform_health: analytics.platform_health || 'good',
          })

          setMetrics({
            active_users_today: analytics.active_users_today || 0,
            new_users_this_week: analytics.new_users_this_week || 0,
            course_completion_rate: analytics.course_completion_rate || 0,
            average_assessment_score: analytics.average_assessment_score || 0,
          })
        }
      } catch (error) {
        console.error('[v0] Failed to load admin data:', error)
      } finally {
        setLoading(false)
      }
    }

    if (user) {
      loadAdminData()
    }
  }, [user])

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading admin dashboard...</p>
        </div>
      </div>
    )
  }

  const healthColor = {
    good: 'bg-green-100 text-green-800',
    warning: 'bg-yellow-100 text-yellow-800',
    critical: 'bg-red-100 text-red-800',
  }

  return (
    <div className="space-y-8 pb-8">
      {/* Welcome Header */}
      <div className="bg-gradient-to-r from-primary/10 to-primary/5 rounded-lg p-8 border border-border">
        <h1 className="text-3xl font-bold mb-2">Platform Administration</h1>
        <p className="text-muted-foreground">Monitor system health, manage users, and view platform analytics</p>
      </div>

      {/* System Health Banner */}
      <div className={`rounded-lg p-6 border border-border ${healthColor[stats.platform_health]}`}>
        <div className="flex items-center justify-between">
          <div>
            <h3 className="font-semibold text-lg">System Status</h3>
            <p className="text-sm mt-1 opacity-90">
              {stats.platform_health === 'good' && 'All systems operational'}
              {stats.platform_health === 'warning' && 'Some services may be experiencing delays'}
              {stats.platform_health === 'critical' && 'Urgent attention required'}
            </p>
          </div>
          <span className="text-2xl font-bold capitalize">{stats.platform_health}</span>
        </div>
      </div>

      {/* Key Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { label: 'Total Users', value: stats.total_users, icon: '👥', color: 'bg-blue-100 text-blue-800' },
          { label: 'Students', value: stats.total_students, icon: '🎓', color: 'bg-purple-100 text-purple-800' },
          { label: 'Teachers', value: stats.total_teachers, icon: '👨‍🏫', color: 'bg-green-100 text-green-800' },
          { label: 'Admins', value: stats.total_admins, icon: '🔧', color: 'bg-orange-100 text-orange-800' },
        ].map((stat) => (
          <div key={stat.label} className={`rounded-lg p-6 border border-border ${stat.color}`}>
            <p className="text-xs opacity-75 uppercase tracking-wide mb-2">{stat.label}</p>
            <p className="text-3xl font-bold">{stat.value}</p>
          </div>
        ))}
      </div>

      {/* Platform Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { label: 'Courses', value: stats.total_courses, icon: '📚' },
          { label: 'Enrollments', value: stats.total_enrollments, icon: '📝' },
          { label: 'Assessments', value: stats.total_assessments, icon: '✏️' },
          { label: 'Active Today', value: metrics.active_users_today, icon: '🟢' },
        ].map((metric) => (
          <div key={metric.label} className="bg-card rounded-lg p-6 border border-border">
            <p className="text-xs text-muted-foreground uppercase tracking-wide mb-2">{metric.label}</p>
            <p className="text-2xl font-bold">{metric.value}</p>
            <span className="text-xl ml-2">{metric.icon}</span>
          </div>
        ))}
      </div>

      {/* Tabs Navigation */}
      <div className="border-b border-border">
        <div className="flex gap-8">
          {(['overview', 'users', 'system', 'moderation'] as const).map((tab) => (
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
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
              <Link
                href="/admin/users"
                className="flex items-center gap-3 p-3 rounded hover:bg-muted transition-colors border border-border"
              >
                <span className="text-xl">👥</span>
                <span className="font-medium">Manage Users</span>
              </Link>
              <Link
                href="/admin/courses"
                className="flex items-center gap-3 p-3 rounded hover:bg-muted transition-colors border border-border"
              >
                <span className="text-xl">📚</span>
                <span className="font-medium">Review Courses</span>
              </Link>
              <Link
                href="/admin/reports"
                className="flex items-center gap-3 p-3 rounded hover:bg-muted transition-colors border border-border"
              >
                <span className="text-xl">📊</span>
                <span className="font-medium">View Reports</span>
              </Link>
              <Link
                href="/admin/settings"
                className="flex items-center gap-3 p-3 rounded hover:bg-muted transition-colors border border-border"
              >
                <span className="text-xl">⚙️</span>
                <span className="font-medium">Settings</span>
              </Link>
            </div>
          </div>

          {/* Performance Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-card rounded-lg p-6 border border-border">
              <h4 className="font-semibold mb-4">Weekly Activity</h4>
              <div className="space-y-3">
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>New Users</span>
                    <span className="font-medium">{metrics.new_users_this_week}</span>
                  </div>
                  <div className="w-full bg-muted rounded-full h-2">
                    <div className="bg-primary h-2 rounded-full" style={{ width: '65%' }}></div>
                  </div>
                </div>
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>Active Users</span>
                    <span className="font-medium">{metrics.active_users_today}</span>
                  </div>
                  <div className="w-full bg-muted rounded-full h-2">
                    <div className="bg-green-500 h-2 rounded-full" style={{ width: '45%' }}></div>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-card rounded-lg p-6 border border-border">
              <h4 className="font-semibold mb-4">Quality Metrics</h4>
              <div className="space-y-3">
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>Course Completion Rate</span>
                    <span className="font-medium">{metrics.course_completion_rate}%</span>
                  </div>
                  <div className="w-full bg-muted rounded-full h-2">
                    <div className="bg-blue-500 h-2 rounded-full" style={{ width: `${metrics.course_completion_rate}%` }}></div>
                  </div>
                </div>
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>Avg. Assessment Score</span>
                    <span className="font-medium">{metrics.average_assessment_score.toFixed(1)}%</span>
                  </div>
                  <div className="w-full bg-muted rounded-full h-2">
                    <div className="bg-purple-500 h-2 rounded-full" style={{ width: `${metrics.average_assessment_score}%` }}></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'users' && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold">User Management</h3>
            <Link
              href="/admin/users"
              className="inline-flex items-center gap-2 bg-primary text-primary-foreground rounded px-4 py-2 text-sm font-medium hover:bg-primary/90 transition-colors"
            >
              View All Users
            </Link>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-card rounded-lg p-6 border border-border">
              <h4 className="font-semibold mb-4">User Distribution</h4>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm">Students</span>
                  <span className="font-semibold">{stats.total_students}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">Teachers</span>
                  <span className="font-semibold">{stats.total_teachers}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">Admins</span>
                  <span className="font-semibold">{stats.total_admins}</span>
                </div>
              </div>
            </div>

            <div className="bg-card rounded-lg p-6 border border-border">
              <h4 className="font-semibold mb-4">Permissions</h4>
              <p className="text-sm text-muted-foreground mb-4">
                Manage user roles, permissions, and access levels
              </p>
              <Link
                href="/admin/permissions"
                className="inline-flex items-center gap-2 px-3 py-2 bg-muted hover:bg-muted/80 rounded text-sm font-medium transition-colors"
              >
                Configure Permissions
              </Link>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'system' && (
        <div className="space-y-4">
          <h3 className="text-lg font-semibold">System Configuration</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-card rounded-lg p-6 border border-border">
              <h4 className="font-semibold mb-4">Database Status</h4>
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm">Connection</span>
                  <span className="inline-block px-2 py-1 bg-green-100 text-green-800 rounded text-xs font-medium">Connected</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">Response Time</span>
                  <span className="text-sm font-medium">45ms</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">Health</span>
                  <span className="inline-block px-2 py-1 bg-green-100 text-green-800 rounded text-xs font-medium">Optimal</span>
                </div>
              </div>
            </div>

            <div className="bg-card rounded-lg p-6 border border-border">
              <h4 className="font-semibold mb-4">API Status</h4>
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm">Uptime</span>
                  <span className="text-sm font-medium">99.9%</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">Requests/min</span>
                  <span className="text-sm font-medium">2,340</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">Error Rate</span>
                  <span className="text-sm font-medium">0.1%</span>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-card rounded-lg p-6 border border-border">
            <h4 className="font-semibold mb-4">Maintenance</h4>
            <p className="text-sm text-muted-foreground mb-4">
              Perform system maintenance, backups, and optimizations
            </p>
            <div className="flex gap-3">
              <Link
                href="/admin/maintenance"
                className="inline-flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded text-sm font-medium hover:bg-primary/90 transition-colors"
              >
                Maintenance Panel
              </Link>
              <button className="inline-flex items-center gap-2 px-4 py-2 border border-border rounded text-sm font-medium hover:bg-muted transition-colors">
                Clear Cache
              </button>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'moderation' && (
        <div className="space-y-4">
          <h3 className="text-lg font-semibold">Content Moderation</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-card rounded-lg p-6 border border-border">
              <p className="text-sm text-muted-foreground mb-1">Pending Reviews</p>
              <p className="text-3xl font-bold">12</p>
              <p className="text-xs text-muted-foreground mt-2">Courses awaiting approval</p>
            </div>
            <div className="bg-card rounded-lg p-6 border border-border">
              <p className="text-sm text-muted-foreground mb-1">Flagged Content</p>
              <p className="text-3xl font-bold">3</p>
              <p className="text-xs text-muted-foreground mt-2">Items reported for review</p>
            </div>
            <div className="bg-card rounded-lg p-6 border border-border">
              <p className="text-sm text-muted-foreground mb-1">Active Reports</p>
              <p className="text-3xl font-bold">5</p>
              <p className="text-xs text-muted-foreground mt-2">Under investigation</p>
            </div>
          </div>

          <div className="bg-card rounded-lg p-6 border border-border">
            <h4 className="font-semibold mb-4">Moderation Actions</h4>
            <div className="space-y-3">
              <Link
                href="/admin/reviews/pending"
                className="block p-3 rounded border border-border hover:bg-muted transition-colors text-sm font-medium"
              >
                Review Pending Courses →
              </Link>
              <Link
                href="/admin/reports"
                className="block p-3 rounded border border-border hover:bg-muted transition-colors text-sm font-medium"
              >
                View User Reports →
              </Link>
              <Link
                href="/admin/banned"
                className="block p-3 rounded border border-border hover:bg-muted transition-colors text-sm font-medium"
              >
                Manage Banned Users →
              </Link>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
