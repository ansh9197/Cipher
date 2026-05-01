import api from './api'

export interface User {
  id:                  string
  email:               string
  full_name:           string | null
  company:             string | null
  plan:                string
  is_active:           boolean
  github_username:     string | null
  analyses_this_month: number
  created_at:          string
}

export async function login(email: string, password: string) {
  const res = await api.post('/api/v1/auth/login', { email, password })
  localStorage.setItem('cipher_token', res.data.access_token)
  localStorage.setItem('cipher_plan',  res.data.plan)
  return res.data
}

export async function register(email: string, password: string, full_name?: string) {
  const res = await api.post('/api/v1/auth/register', { email, password, full_name })
  localStorage.setItem('cipher_token', res.data.access_token)
  localStorage.setItem('cipher_plan',  res.data.plan)
  return res.data
}

export function logout() {
  localStorage.removeItem('cipher_token')
  localStorage.removeItem('cipher_plan')
  window.location.href = '/login'
}

export function isLoggedIn(): boolean {
  if (typeof window === 'undefined') return false
  return !!localStorage.getItem('cipher_token')
}

export async function getProfile(): Promise<User> {
  const res = await api.get('/api/v1/users/me')
  return res.data
}
