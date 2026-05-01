'use client'
import Link from 'next/link'

const features = [
  { icon: '⚡', title: 'Instant analysis',  desc: 'Root cause on your PR within 30 seconds of a failure.' },
  { icon: '🧠', title: 'Learns your stack', desc: 'Fine-tunes on your failure history. Gets smarter weekly.' },
  { icon: '🔁', title: 'Self-improving',    desc: 'Engineer feedback trains the model. No manual labeling.' },
  { icon: '🔒', title: 'Your data stays',   desc: 'Logs never leave your AWS account.' },
]

const plans = [
  { name: 'Free',    price: 0,  analyses: 50,  repos: 1,  features: ['50 analyses/month','1 repository','GitHub PR comments'] },
  { name: 'Starter', price: 29, analyses: 500, repos: 5,  features: ['500 analyses/month','5 repositories','Slack integration','Email alerts'], popular: true },
  { name: 'Pro',     price: 99, analyses: -1,  repos: -1, features: ['Unlimited analyses','Unlimited repos','Custom model','API access','Priority support'] },
]

export default function Home() {
  return (
    <main className="min-h-screen" style={{ background: '#0d1117' }}>

      <nav className="flex items-center justify-between px-8 py-5 border-b border-white/5">
        <span className="text-xl font-bold gradient-text">CIPHER</span>
        <div className="flex items-center gap-4">
          <Link href="/login"    className="text-sm text-gray-400 hover:text-white transition-colors">Sign in</Link>
          <Link href="/register" className="text-sm bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded-lg transition-colors">
            Get started free
          </Link>
        </div>
      </nav>

      <section className="text-center px-6 py-24 max-w-4xl mx-auto">
        <div className="inline-block px-4 py-1 rounded-full text-xs font-medium mb-6"
             style={{ background: 'rgba(99,102,241,0.15)', border: '1px solid rgba(99,102,241,0.3)', color: '#a5b4fc' }}>
          AI-powered DevOps · Self-improving · Always-on
        </div>
        <h1 className="text-5xl font-bold mb-6 leading-tight text-white">
          Stop reading logs.<br />
          <span className="gradient-text">Let CIPHER explain them.</span>
        </h1>
        <p className="text-lg text-gray-400 mb-10 max-w-xl mx-auto">
          CIPHER automatically analyzes CI/CD pipeline failures and posts a plain-English
          root cause and fix as a PR comment — within 30 seconds.
        </p>
        <div className="flex items-center justify-center gap-4 flex-wrap">
          <Link href="/register" className="bg-indigo-600 hover:bg-indigo-500 text-white font-medium px-8 py-3 rounded-xl transition-colors">
            Start free — no credit card
          </Link>
          <Link href="/login" className="text-gray-400 hover:text-white border border-white/10 px-8 py-3 rounded-xl transition-colors">
            Sign in
          </Link>
        </div>
      </section>

      <section className="px-8 py-16 max-w-5xl mx-auto">
        <h2 className="text-2xl font-bold text-center text-white mb-12">Everything your team needs</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {features.map((f) => (
            <div key={f.title} className="card p-6">
              <div className="text-3xl mb-4">{f.icon}</div>
              <h3 className="font-semibold text-white mb-2">{f.title}</h3>
              <p className="text-gray-400 text-sm leading-relaxed">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="px-8 py-16 max-w-5xl mx-auto">
        <h2 className="text-2xl font-bold text-center text-white mb-4">Simple pricing</h2>
        <p className="text-gray-400 text-center mb-12">Start free. Upgrade when you grow.</p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {plans.map((p) => (
            <div key={p.name} className="card p-6 flex flex-col"
                 style={p.popular ? { borderColor: 'rgba(99,102,241,0.5)' } : {}}>
              {p.popular && <div className="text-xs font-semibold text-indigo-400 mb-3 uppercase tracking-wider">Most popular</div>}
              <div className="text-lg font-bold text-white mb-1">{p.name}</div>
              <div className="text-3xl font-bold text-white mb-4">
                ${p.price}<span className="text-base font-normal text-gray-400">/mo</span>
              </div>
              <ul className="space-y-2 mb-8 flex-1">
                {p.features.map((f) => (
                  <li key={f} className="text-sm text-gray-400 flex items-start gap-2">
                    <span className="text-indigo-400 mt-0.5">✓</span>{f}
                  </li>
                ))}
              </ul>
              <Link href="/register"
                    className={`text-center py-2 rounded-lg text-sm font-medium transition-colors
                      ${p.popular ? 'bg-indigo-600 hover:bg-indigo-500 text-white' : 'border border-white/10 text-gray-300 hover:border-white/20'}`}>
                Get started
              </Link>
            </div>
          ))}
        </div>
      </section>

      <footer className="text-center py-10 border-t border-white/5 text-gray-500 text-sm">
        <span className="gradient-text font-bold">CIPHER</span> · Built on AWS · Powered by AI
      </footer>
    </main>
  )
}
