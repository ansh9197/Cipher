'use client'
import Link from 'next/link'

export default function Home() {
  return (
    <main className="min-h-screen" style={{ background: '#0d1117' }}>
      <nav className="flex items-center justify-between px-8 py-5 border-b border-white/5">
        <span className="text-xl font-bold gradient-text">CIPHER</span>
        <div className="flex items-center gap-4">
          <Link href="/login" className="text-sm text-gray-400 hover:text-white">Sign in</Link>
          <Link href="/register" className="text-sm bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded-lg transition-colors">
            Get started free
          </Link>
        </div>
      </nav>

      <section className="text-center px-6 py-24 max-w-4xl mx-auto">
        <div className="inline-block px-4 py-1 rounded-full text-xs font-medium mb-6"
          style={{ background: 'rgba(99,102,241,0.15)', border: '1px solid rgba(99,102,241,0.3)', color: '#a5b4fc' }}>
          Works with GitHub Actions · Jenkins · GitLab CI · Any pipeline
        </div>
        <h1 className="text-5xl font-bold mb-6 leading-tight text-white">
          Stop reading logs.<br />
          <span className="gradient-text">Let CIPHER explain them.</span>
        </h1>
        <p className="text-lg text-gray-400 mb-10 max-w-2xl mx-auto">
          CIPHER automatically analyzes CI/CD pipeline failures and posts a plain-English
          root cause and fix as a PR comment — within 30 seconds, automatically.
        </p>
        <div className="flex items-center justify-center gap-4 flex-wrap">
          <Link href="/register"
            className="bg-indigo-600 hover:bg-indigo-500 text-white font-semibold px-8 py-3 rounded-xl transition-colors text-lg">
            Start free →
          </Link>
          <Link href="/login"
            className="text-gray-400 hover:text-white border border-white/10 px-8 py-3 rounded-xl transition-colors">
            Sign in
          </Link>
        </div>
      </section>

      <section className="px-8 py-8 max-w-5xl mx-auto">
        <div className="card p-6 text-center" style={{ borderColor: 'rgba(16,185,129,0.2)' }}>
          <p className="text-white font-semibold mb-2">Your code stays yours. Always.</p>
          <p className="text-gray-400 text-sm mb-3">CIPHER only reads pipeline logs — never your source code, secrets, or files.</p>
          <div className="flex justify-center gap-6 text-xs text-gray-500 flex-wrap">
            <span>🔒 No source code access</span>
            <span>🗑️ Logs discarded after analysis</span>
            <span>🇮🇳 Data stored in India</span>
            <span>⚡ Revoke access anytime</span>
          </div>
        </div>
      </section>

      <section className="px-8 py-12 max-w-5xl mx-auto">
        <h2 className="text-2xl font-bold text-center text-white mb-10">How CIPHER works</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          {[
            { step: '1', title: 'Pipeline fails', desc: 'GitHub Actions, Jenkins, or GitLab CI pipeline fails on your repo' },
            { step: '2', title: 'CIPHER detects it', desc: 'Webhook received in milliseconds. Log downloaded automatically' },
            { step: '3', title: 'AI analyzes', desc: 'ML model classifies failure type with root cause explanation' },
            { step: '4', title: 'PR comment posted', desc: 'Fix suggestion posted on your PR within 30 seconds' },
          ].map(item => (
            <div key={item.step} className="card p-6 text-center">
              <div className="w-10 h-10 rounded-full flex items-center justify-center mx-auto mb-3 text-white font-bold"
                style={{ background: '#6366f1' }}>{item.step}</div>
              <h3 className="font-semibold text-white mb-2">{item.title}</h3>
              <p className="text-gray-400 text-sm">{item.desc}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="px-8 py-12 max-w-5xl mx-auto">
        <h2 className="text-2xl font-bold text-center text-white mb-10">Simple pricing</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {[
            { name: 'Free', price: '₹0', analyses: '50 analyses/month', repos: '1 repository', color: '' },
            { name: 'Starter', price: '₹2,400', analyses: '500 analyses/month', repos: '5 repositories', color: 'rgba(99,102,241,0.5)' },
            { name: 'Pro', price: '₹8,200', analyses: 'Unlimited analyses', repos: 'Unlimited repos', color: '' },
          ].map(p => (
            <div key={p.name} className="card p-6"
              style={p.color ? { borderColor: p.color } : {}}>
              <div className="text-lg font-bold text-white mb-1">{p.name}</div>
              <div className="text-3xl font-bold text-white mb-4">{p.price}<span className="text-base font-normal text-gray-400">/mo</span></div>
              <div className="text-sm text-gray-400 mb-1">✓ {p.analyses}</div>
              <div className="text-sm text-gray-400 mb-4">✓ {p.repos}</div>
              <Link href="/register" className="block text-center py-2 rounded-lg text-sm font-medium transition-colors bg-indigo-600 hover:bg-indigo-500 text-white">
                Get started
              </Link>
            </div>
          ))}
        </div>
      </section>

      <footer className="text-center py-8 border-t border-white/5 text-gray-500 text-sm">
        <span className="gradient-text font-bold">CIPHER</span>
        {' · '}
        <Link href="/privacy" className="hover:text-gray-300">Privacy</Link>
        {' · '}
        <Link href="/security" className="hover:text-gray-300">Security</Link>
        {' · Made in India 🇮🇳'}
      </footer>
    </main>
  )
}
