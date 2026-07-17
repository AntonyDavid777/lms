/**
 * TechTots LMS - Frontend Types
 */

export enum UserRole {
  STUDENT = 'student',
  TEACHER = 'teacher',
  ADMIN = 'admin',
}

export interface User {
  _id: string
  email: string
  name: string
  role: UserRole
  bio?: string
  profile_picture_url?: string
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface AuthTokens {
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
}

export interface AuthResponse {
  user: User
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
}

export interface Course {
  _id: string
  title: string
  description: string
  category: string
  instructor_id: string
  instructor_name?: string
  level: 'beginner' | 'intermediate' | 'advanced'
  thumbnail_url?: string
  status: 'draft' | 'published' | 'archived'
  lessons_count?: number
  created_at: string
  updated_at: string
}

export interface Lesson {
  _id: string
  title: string
  description: string
  course_id: string
  order: number
  content_type: 'video' | 'text' | 'interactive' | 'quiz'
  content: string
  video_url?: string
  duration?: number
  learning_objectives?: string[]
  resources_url?: string[]
  created_at: string
  updated_at: string
}

export interface Assessment {
  _id: string
  title: string
  description: string
  course_id: string
  instructor_id: string
  pass_score: number
  time_limit?: number
  questions_count?: number
  total_points?: number
  created_at: string
  updated_at: string
}

export interface Question {
  _id: string
  type: 'multiple_choice' | 'short_answer' | 'essay'
  text: string
  options?: string[]
  correct_answer?: string
  points?: number
  explanation?: string
}

export interface QuizResult {
  _id: string
  user_id: string
  assessment_id: string
  score: number
  total_points: number
  percentage: number
  answers: Record<string, string>
  status: 'in_progress' | 'submitted' | 'graded'
  submitted_at: string
  time_taken?: number
}

export interface Progress {
  _id: string
  user_id: string
  course_id: string
  lesson_id?: string
  status: 'not_started' | 'in_progress' | 'completed'
  completion_percentage: number
  last_accessed: string
  time_spent: number
  notes?: string
}

export interface Badge {
  _id: string
  name: string
  description: string
  icon_url?: string
  criteria: string
  rarity: 'common' | 'rare' | 'epic' | 'legendary'
}

export interface UserBadge {
  badge_id: string
  badge_name: string
  earned_at: string
  icon_url?: string
}

export interface UserPoints {
  _id: string
  user_id: string
  points_balance: number
  points_earned: number
  points_spent: number
  updated_at: string
}

export interface LeaderboardEntry {
  user_id: string
  user_name: string
  position: number
  points: number
  courses_completed: number
}

export interface Enrollment {
  _id: string
  user_id: string
  course_id: string
  enrolled_at: string
  completed_at?: string
  progress_percentage: number
}

export interface ApiResponse<T> {
  success: boolean
  data?: T
  message?: string
  error?: string
  status_code: number
}

export interface PaginatedResponse<T> {
  success: boolean
  data: T[]
  pagination: {
    total: number
    page: number
    page_size: number
    total_pages: number
  }
  message: string
  status_code: number
}
