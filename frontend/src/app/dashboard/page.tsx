'use client'
import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { isLoggedIn, getProfile, logout, User } from '@/lib/auth'

export default function DashboardPage() {
  const router  = useRouter()
  const [user,    setUser]    = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!isLoggedIn()) { router.push('/login'); return }
    getProfile()
      .then(setUser)
      .catch(() => router.push('/login'))
      .finally(() => setLoading(false))
  }, [router])

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center" style={{ background: '#0d1117' }}>
        <div className="text-gray-400 text-sm">Loading...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen" style={{ background: '#0d1117' }}>
      <nav className="flex items-center justify-between px-6 py-4 border-b border-white/5">
        <span className="text-lg font-bold gradient-text">CIPHER</span>
        <div className="flex items-center gap-4">
          <span className="text-xs px-3 py-1 rounded-full"
                style={{ background: 'rgba(99,102,241,0.1)', border: '1px solid rgba(99,102,241,0.3)', color: '#a5b4fc' }}>
            {(user?.plan || 'free').toUpperCase()}
          </span>
          <span className="text-sm text-gray-400">{user?.email}</span>
          <button onClick={logout}
            className="text-sm text-gray-500 hover:text-gray-300 transition-colors">
            Sign out
          </button>
        </div>
      </nav>

      <div className="max-w-5xl mx-auto px-6 py-8">
        <h1 className="text-2xl font-bold text-white mb-2">
          Welcome back{user?.full_name ? `, ${user.full_name}` : ''} 👋
        </h1>
        <p className="text-gray-400 text-sm mb-8">Your pipeline health overview</p>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          {[
            { label: 'Analyses this month', value: user?.analyses_this_month ?? 0 },
            { label: 'Current plan',        value: user?.plan || 'free' },
            { label: 'GitHub',              value: user?.github_username || 'Not connected' },
            { label: 'Account',             value: user?.is_active ? '✓ Active' : 'Inactive' },
          ].map((s) => (
            <div key={s.label} className="card p-5">
              <div className="text-xl font-bold text-white">{s.value}</div>
              <div className="text-xs text-gray-400 mt-1">{s.label}</div>
            </div>
          ))}
        </div>

        {!user?.github_username && (
          <div className="card p-5 mb-6 flex items-center justify-between"
               style={{ borderColor: 'rgba(99,102,241,0.3)' }}>
            <div>
              <div className="text-white font-medium text-sm">Connect your GitHub organisation</div>
              <div className="text-gray-400 text-xs mt-1">
                Install the CIPHER GitHub App to start analyzing failures automatically
              </div>
            </div>
            <a href="https://github.com/apps/cipher-ai/installations/new"
               target="_blank" rel="noopener noreferrer"
               className="ml-4 shrink-0 text-sm bg-indigo-600 hover:bg-indigo-500 text-white px-5 py-2 rounded-lg transition-colors">
              Connect GitHub
            </a>
          </div>
        )}

        <div className="card p-12 text-center mb-6">
          <div className="text-4xl mb-4">🔍</div>
          <div className="text-white font-medium mb-2">No analyses yet</div>
          <div className="text-gray-400 text-sm">
            Connect GitHub and let a pipeline fail — CIPHER will analyze it automatically
          </div>
        </div>

        {user?.plan === 'free' && (
          <div className="card p-6 text-center"
               style={{ background: 'linear-gradient(135deg,rgba(99,102,241,0.08),rgba(139,92,246,0.08))', borderColor: 'rgba(99,102,241,0.2)' }}>
            <div className="text-white font-semibold mb-2">Unlock unlimited analyses</div>
            <div className="text-gray-400 text-sm mb-4">
              Upgrade to Starter for $29/month — 500 analyses, 5 repos, Slack integration
            </div>
            <a href="/pricing"
               className="inline-block bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-medium px-6 py-2.5 rounded-lg transition-colors">
              View pricing
            </a>
          </div>
        )}
      </div>
    </div>
  )
}
