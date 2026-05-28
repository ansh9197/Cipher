'use client'
import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { isLoggedIn, getProfile, logout, User } from '@/lib/auth'
import api from '@/lib/api'

interface Analysis {
  id: string
  repo: string
  run_id: string
  branch: string
  category: string
  confidence: number
  root_cause: string
  suggestion: string
  method: string
  created_at: string
}

const categoryColor: Record<string, string> = {
  dependency_error: '#f59e0b',
  test_failure: '#ef4444',
  build_error: '#f97316',
  auth_failure: '#8b5cf6',
  infra_error: '#06b6d4',
  timeout: '#6366f1',
  unknown: '#64748b',
}

const categoryEmoji: Record<string, string> = {
  dependency_error: '📦',
  test_failure: '🧪',
  build_error: '🔨',
  auth_failure: '🔐',
  infra_error: '🖥️',
  timeout: '⏰',
  unknown: '❓',
}

export default function DashboardPage() {
  const router = useRouter()
  const [user, setUser] = useState<User | null>(null)
  const [analyses, setAnalyses] = useState<Analysis[]>([])
  const [loading, setLoading] = useState(true)
  const [selected, setSelected] = useState<Analysis | null>(null)

  useEffect(() => {
    if (!isLoggedIn()) { router.push('/login'); return }
    getProfile().then(setUser).catch(() => router.push('/login'))
    api.get('/api/v1/users/analyses')
      .then(r => setAnalyses(r.data || []))
      .catch(() => setAnalyses([]))
      .finally(() => setLoading(false))
  }, [router])

  const stars = (conf: number) => {
    const n = Math.round(conf * 5)
    return '★'.repeat(n) + '☆'.repeat(5 - n)
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
          <button onClick={logout} className="text-sm text-gray-500 hover:text-gray-300">Sign out</button>
        </div>
      </nav>

      <div className="max-w-6xl mx-auto px-6 py-8">
        <h1 className="text-2xl font-bold text-white mb-2">Pipeline Health Dashboard</h1>
        <p className="text-gray-400 text-sm mb-8">CIPHER analyzes every pipeline failure automatically</p>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          {[
            { label: 'Total Analyses', value: analyses.length },
            { label: 'This Month', value: user?.analyses_this_month ?? analyses.length },
            { label: 'Plan', value: (user?.plan || 'free').toUpperCase() },
            { label: 'Status', value: '✓ Active' },
          ].map(s => (
            <div key={s.label} className="card p-5">
              <div className="text-2xl font-bold text-white">{s.value}</div>
              <div className="text-xs text-gray-400 mt-1">{s.label}</div>
            </div>
          ))}
        </div>

        {/* Connect GitHub */}
        <div className="card p-6 mb-6" style={{ borderColor: 'rgba(99,102,241,0.3)' }}>
          <h3 className="text-white font-semibold mb-2">Connect to GitHub</h3>
          <p className="text-gray-400 text-sm mb-4">
            Install the CIPHER GitHub App to automatically analyze pipeline failures.
            Zero configuration needed — works with GitHub Actions instantly.
          </p>
          <div className="flex gap-3 flex-wrap">
            <a href="https://github.com/apps/cipher-ai-ansh9197"
              target="_blank" rel="noopener noreferrer"
              className="inline-block bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-medium px-6 py-2.5 rounded-lg transition-colors">
              Install GitHub App →
            </a>
            <a href="http://13.232.125.216:8004/docs"
              target="_blank" rel="noopener noreferrer"
              className="inline-block border border-white/10 text-gray-300 hover:text-white text-sm px-6 py-2.5 rounded-lg transition-colors">
              Test AI directly →
            </a>
          </div>
          <div className="mt-4 p-3 rounded-lg text-xs"
            style={{ background: 'rgba(16,185,129,0.08)', border: '1px solid rgba(16,185,129,0.2)', color: '#6ee7b7' }}>
            🔒 CIPHER only reads pipeline logs. Never your source code, secrets, or files.
          </div>
        </div>

        {/* Analyses list */}
        {loading ? (
          <div className="card p-12 text-center">
            <div className="text-gray-400">Loading analyses...</div>
          </div>
        ) : analyses.length === 0 ? (
          <div className="card p-12 text-center">
            <div className="text-4xl mb-4">🔍</div>
            <div className="text-white font-medium mb-2">No analyses yet</div>
            <div className="text-gray-400 text-sm">
              Once connected, CIPHER analyzes every pipeline failure automatically within 30 seconds
            </div>
          </div>
        ) : (
          <div>
            <h2 className="text-lg font-semibold text-white mb-4">
              Recent Analyses ({analyses.length})
            </h2>
            <div className="space-y-3">
              {analyses.map(a => (
                <div key={a.id}
                  className="card p-5 cursor-pointer hover:border-indigo-500/50 transition-colors"
                  onClick={() => setSelected(selected?.id === a.id ? null : a)}>
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex items-center gap-3">
                      <span className="text-2xl">{categoryEmoji[a.category] || '❓'}</span>
                      <div>
                        <div className="flex items-center gap-2 flex-wrap">
                          <span className="text-white font-medium text-sm">{a.repo}</span>
                          <span className="text-xs px-2 py-0.5 rounded-full"
                            style={{
                              background: `${categoryColor[a.category]}20`,
                              color: categoryColor[a.category],
                              border: `1px solid ${categoryColor[a.category]}40`
                            }}>
                            {a.category.replace(/_/g, ' ')}
                          </span>
                        </div>
                        <div className="text-xs text-gray-500 mt-1">
                          {a.branch} · run #{a.run_id} · {new Date(a.created_at).toLocaleString()}
                        </div>
                      </div>
                    </div>
                    <div className="text-right shrink-0">
                      <div className="text-yellow-400 text-sm">{stars(a.confidence)}</div>
                      <div className="text-xs text-gray-500">{Math.round(a.confidence * 100)}%</div>
                    </div>
                  </div>

                  {selected?.id === a.id && (
                    <div className="mt-4 pt-4 border-t border-white/5 space-y-3">
                      <div>
                        <div className="text-xs text-gray-500 uppercase tracking-wider mb-1">Root Cause</div>
                        <div className="text-sm text-gray-300">{a.root_cause}</div>
                      </div>
                      <div>
                        <div className="text-xs text-gray-500 uppercase tracking-wider mb-1">Suggested Fix</div>
                        <div className="text-sm text-green-400">{a.suggestion}</div>
                      </div>
                      <div className="text-xs text-gray-600">
                        Analyzed by CIPHER using {a.method}
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Jenkins/GitLab */}
        <div className="card p-5 mt-6">
          <div className="text-white font-medium text-sm mb-2">Using Jenkins or GitLab CI?</div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div>
              <div className="text-gray-500 text-xs mb-1">Jenkins webhook URL</div>
              <div className="font-mono text-xs p-2 rounded" style={{ background: 'rgba(255,255,255,0.04)', color: '#a5b4fc' }}>
                http://13.232.125.216:8002/api/v1/webhooks/jenkins
              </div>
            </div>
            <div>
              <div className="text-gray-500 text-xs mb-1">GitLab CI webhook URL</div>
              <div className="font-mono text-xs p-2 rounded" style={{ background: 'rgba(255,255,255,0.04)', color: '#a5b4fc' }}>
                http://13.232.125.216:8002/api/v1/webhooks/gitlab
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  )
}
