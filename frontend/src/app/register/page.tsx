'use client'
import { useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { register } from '@/lib/auth'

export default function RegisterPage() {
  const router = useRouter()
  const [name,     setName]     = useState('')
  const [email,    setEmail]    = useState('')
  const [password, setPassword] = useState('')
  const [error,    setError]    = useState('')
  const [loading,  setLoading]  = useState(false)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError('')
    if (password.length < 8) { setError('Password must be at least 8 characters'); return }
    setLoading(true)
    try {
      await register(email, password, name)
      router.push('/dashboard')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Registration failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen flex items-center justify-center px-4" style={{ background: '#0d1117' }}>
      <div className="w-full max-w-sm">
        <div className="text-center mb-8">
          <Link href="/" className="text-2xl font-bold gradient-text">CIPHER</Link>
          <p className="text-gray-400 mt-2 text-sm">Create your free account</p>
        </div>
        <div className="card p-8">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm text-gray-400 mb-1">Full name</label>
              <input type="text" value={name} onChange={e => setName(e.target.value)}
                placeholder="Your name"
                className="w-full rounded-lg px-4 py-2.5 text-white text-sm placeholder-gray-600"
                style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.1)' }}/>
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">Work email</label>
              <input type="email" value={email} onChange={e => setEmail(e.target.value)}
                required placeholder="you@company.com"
                className="w-full rounded-lg px-4 py-2.5 text-white text-sm placeholder-gray-600"
                style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.1)' }}/>
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">Password</label>
              <input type="password" value={password} onChange={e => setPassword(e.target.value)}
                required placeholder="Min 8 characters"
                className="w-full rounded-lg px-4 py-2.5 text-white text-sm placeholder-gray-600"
                style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.1)' }}/>
            </div>
            {error && (
              <div className="text-red-400 text-sm rounded-lg px-3 py-2"
                   style={{ background: 'rgba(248,113,113,0.1)', border: '1px solid rgba(248,113,113,0.2)' }}>
                {error}
              </div>
            )}
            <button type="submit" disabled={loading}
              className="w-full bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white font-medium py-2.5 rounded-lg transition-colors text-sm">
              {loading ? 'Creating account...' : 'Create free account'}
            </button>
          </form>
          <p className="text-center text-sm text-gray-500 mt-6">
            Have an account?{' '}
            <Link href="/login" className="text-indigo-400 hover:text-indigo-300">Sign in</Link>
          </p>
        </div>
      </div>
    </main>
  )
}
