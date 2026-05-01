'use client'
import { useState } from 'react'
import Link from 'next/link'
import api from '@/lib/api'
import { isLoggedIn } from '@/lib/auth'

const plans = [
  {
    id: 'starter', name: 'Starter', price: 29, analyses: 500, repos: 5,
    features: ['500 analyses/month','5 repositories','Slack integration','30-day history','Email alerts'],
  },
  {
    id: 'pro', name: 'Pro', price: 99, analyses: -1, repos: -1, popular: true,
    features: ['Unlimited analyses','Unlimited repos','Custom fine-tuned model','API access','90-day history','Priority support'],
  },
]

export default function PricingPage() {
  const [loading, setLoading] = useState<string | null>(null)

  async function checkout(planId: string) {
    if (!isLoggedIn()) { window.location.href = '/register'; return }
    setLoading(planId)
    try {
      const res = await api.post(`/api/v1/billing/create-checkout?plan=${planId}`)
      window.location.href = res.data.checkout_url
    } catch {
      alert('Could not start checkout. Try again.')
    } finally {
      setLoading(null)
    }
  }

  return (
    <main className="min-h-screen px-6 py-16" style={{ background: '#0d1117' }}>
      <nav className="flex items-center justify-between max-w-4xl mx-auto mb-16">
        <Link href="/" className="text-xl font-bold gradient-text">CIPHER</Link>
        <Link href="/dashboard" className="text-sm text-gray-400 hover:text-white">Dashboard</Link>
      </nav>
      <div className="max-w-3xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-3xl font-bold text-white mb-3">Choose your plan</h1>
          <p className="text-gray-400">Cancel anytime. No hidden fees.</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {plans.map((p) => (
            <div key={p.id} className="card p-7 flex flex-col"
                 style={p.popular ? { borderColor: 'rgba(99,102,241,0.5)' } : {}}>
              {p.popular && (
                <div className="text-xs text-indigo-400 font-semibold uppercase tracking-wider mb-3">Most popular</div>
              )}
              <div className="text-xl font-bold text-white mb-1">{p.name}</div>
              <div className="text-4xl font-bold text-white mb-4">
                ${p.price}<span className="text-base font-normal text-gray-400">/month</span>
              </div>
              <ul className="space-y-3 mb-8 flex-1">
                {p.features.map((f) => (
                  <li key={f} className="flex items-start gap-2 text-sm text-gray-300">
                    <span className="text-indigo-400 mt-0.5 shrink-0">✓</span>{f}
                  </li>
                ))}
              </ul>
              <button onClick={() => checkout(p.id)} disabled={loading === p.id}
                className={`w-full py-3 rounded-xl font-medium text-sm transition-colors disabled:opacity-50
                  ${p.popular ? 'bg-indigo-600 hover:bg-indigo-500 text-white' : 'border border-white/10 text-gray-300 hover:border-white/20'}`}>
                {loading === p.id ? 'Redirecting...' : `Upgrade to ${p.name}`}
              </button>
            </div>
          ))}
        </div>
        <div className="text-center mt-10">
          <Link href="/" className="text-sm text-gray-500 hover:text-gray-400">← Back to home</Link>
        </div>
      </div>
    </main>
  )
}
