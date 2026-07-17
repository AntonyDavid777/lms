/**
 * TechTots LMS - API Client
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'
const API_VERSION = 'v1'

export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
    public data?: any,
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

class ApiClient {
  private baseUrl: string
  private apiVersion: string

  constructor(baseUrl = API_BASE_URL, apiVersion = API_VERSION) {
    this.baseUrl = baseUrl
    this.apiVersion = apiVersion
  }

  private getFullUrl(endpoint: string): string {
    return `${this.baseUrl}/api/${this.apiVersion}${endpoint}`
  }

  private async getHeaders(includeAuth = true): Promise<Record<string, string>> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    }

    if (includeAuth) {
      const token = this.getAccessToken()
      if (token) {
        headers['Authorization'] = `Bearer ${token}`
      }
    }

    return headers
  }

  private getAccessToken(): string | null {
    if (typeof window === 'undefined') return null
    return localStorage.getItem('access_token')
  }

  private setAccessToken(token: string): void {
    if (typeof window === 'undefined') return
    localStorage.setItem('access_token', token)
  }

  private getRefreshToken(): string | null {
    if (typeof window === 'undefined') return null
    return localStorage.getItem('refresh_token')
  }

  private setRefreshToken(token: string): void {
    if (typeof window === 'undefined') return
    localStorage.setItem('refresh_token', token)
  }

  private clearTokens(): void {
    if (typeof window === 'undefined') return
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  async request<T>(
    endpoint: string,
    options: RequestInit & { includeAuth?: boolean } = {},
  ): Promise<T> {
    const { includeAuth = true, ...fetchOptions } = options
    const url = this.getFullUrl(endpoint)
    const headers = await this.getHeaders(includeAuth)

    const response = await fetch(url, {
      ...fetchOptions,
      headers: { ...headers, ...(fetchOptions.headers || {}) },
    })

    const data = await response.json()

    if (!response.ok) {
      throw new ApiError(response.status, data.error || 'API Error', data)
    }

    return data as T
  }

  async get<T>(endpoint: string, options?: RequestInit & { includeAuth?: boolean }): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: 'GET' })
  }

  async post<T>(
    endpoint: string,
    body?: any,
    options?: RequestInit & { includeAuth?: boolean },
  ): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'POST',
      body: body ? JSON.stringify(body) : undefined,
    })
  }

  async put<T>(
    endpoint: string,
    body?: any,
    options?: RequestInit & { includeAuth?: boolean },
  ): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'PUT',
      body: body ? JSON.stringify(body) : undefined,
    })
  }

  async delete<T>(endpoint: string, options?: RequestInit & { includeAuth?: boolean }): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: 'DELETE' })
  }

  // Auth endpoints
  async register(email: string, password: string, name: string, role: string = 'student') {
    const response = await this.post('/auth/register', { email, password, name, role }, { includeAuth: false })
    return response as any
  }

  async login(email: string, password: string) {
    const response = await this.post('/auth/login', { email, password }, { includeAuth: false })
    const data = response as any

    if (data.data?.access_token && data.data?.refresh_token) {
      this.setAccessToken(data.data.access_token)
      this.setRefreshToken(data.data.refresh_token)
    }

    return data
  }

  async logout() {
    this.clearTokens()
  }

  async refreshAccessToken() {
    const refreshToken = this.getRefreshToken()
    if (!refreshToken) {
      throw new ApiError(401, 'No refresh token available')
    }

    const response = await this.post('/auth/refresh', { refresh_token: refreshToken }, { includeAuth: false })
    const data = response as any

    if (data.data?.access_token) {
      this.setAccessToken(data.data.access_token)
    }

    return data
  }

  async getCurrentUser() {
    return this.get('/auth/me')
  }

  // User endpoints
  async listUsers(page = 1, pageSize = 10, role?: string, isActive?: boolean, search?: string) {
    const params = new URLSearchParams()
    params.append('page', page.toString())
    params.append('page_size', pageSize.toString())
    if (role) params.append('role', role)
    if (isActive !== undefined) params.append('is_active', isActive.toString())
    if (search) params.append('search', search)

    return this.get(`/users?${params.toString()}`)
  }

  async getUser(userId: string) {
    return this.get(`/users/${userId}`)
  }

  async updateUser(userId: string, data: Record<string, any>) {
    return this.put(`/users/${userId}`, data)
  }

  async getUserCourses(userId: string) {
    return this.get(`/users/${userId}/courses`)
  }

  async changePassword(userId: string, oldPassword: string, newPassword: string) {
    return this.post(`/users/${userId}/change-password`, {
      old_password: oldPassword,
      new_password: newPassword,
    })
  }

  // Course endpoints
  async listCourses(page = 1, pageSize = 10, filters?: Record<string, any>) {
    const params = new URLSearchParams()
    params.append('page', page.toString())
    params.append('page_size', pageSize.toString())
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.append(key, String(value))
        }
      })
    }

    return this.get(`/courses?${params.toString()}`)
  }

  async getCourse(courseId: string) {
    return this.get(`/courses/${courseId}`)
  }

  async createCourse(data: Record<string, any>) {
    return this.post('/courses', data)
  }

  async updateCourse(courseId: string, data: Record<string, any>) {
    return this.put(`/courses/${courseId}`, data)
  }

  async enrollCourse(courseId: string) {
    return this.post(`/courses/${courseId}/enroll`, {})
  }

  async unenrollCourse(courseId: string) {
    return this.delete(`/courses/${courseId}/unenroll`)
  }

  // Health check
  async healthCheck() {
    return this.get('/health', { includeAuth: false })
  }
}

export const apiClient = new ApiClient()
