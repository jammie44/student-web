'use client';
import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Starfield } from '../../components/layout/Starfield';
import { Button } from '../../components/ui/Button';
import { getToken, getStoredUser } from '../../lib/auth';
import { cn } from '../../lib/utils';

const PLANS = [
  {
    id: 'free',
    name: 'Free',
    price: '$0',
    period: 'forever',
    description: 'Perfect for getting started',
    color: 'blue',
    limits: { study_assistant: 10, plagiarism: 5, cv_generator: 3, assignment: 5, research: 5 },
    features: [
      '10 Study Assistant messages/day',
      '5 Plagiarism checks/day',
      '3 CV generations/day',
      '5 Assignment formats/day',
      '5 Research summaries/day',
      'Chat history saved',
      'All 5 AI tools',
    ],
    cta: 'Get Started Free',
    highlighted: false,
  },
  {
    id: 'pro',
    name: 'Pro',
    price: '$9.99',
    period: '/month',
    description: 'For serious students',
    color: 'purple',
    limits: { study_assistant: 50, plagiarism: 30, cv_generator: 15, assignment: 30, research: 30 },
    features: [
      '50 Study Assistant messages/day',
      '30 Plagiarism checks/day',
      '15 CV generations/day',
      '30 Assignment formats/day',
      '30 Research summaries/day',
      'Priority AI responses',
      'All 5 AI tools',
      'Email support',
    ],
    cta: 'Upgrade to Pro',
    highlighted: true,
    badge: 'Most Popular',
  },
  {
    id: 'unlimited',
    name: 'Unlimited',
    price: '$19.99',
    period: '/month',
    description: 'For power users & educators',
    color: 'gold',
    limits: { study_assistant: '∞', plagiarism: '∞', cv_generator: '∞', assignment: '∞', research: '∞' },
    features: [
      'Unlimited Study Assistant',
      'Unlimited Plagiarism checks',
      'Unlimited CV generations',
      'Unlimited Assignments',
      'Unlimited Research summaries',
      'Fastest AI responses',
      'All 5 AI tools',
      'Priority email support',
      'Early access to new tools',
    ],
    cta: 'Go Unlimited',
    highlighted: false,
    badge: 'Best Value',
  },
];

const TOOLS_LIST = [
  { icon: '🎓', name: 'Study Assistant',    free: '10/day', pro: '50/day', unlimited: 'Unlimited' },
  { icon: '🔍', name: 'Plagiarism Checker', free: '5/day',  pro: '30/day', unlimited: 'Unlimited' },
  { icon: '📄', name: 'CV Generator',       free: '3/day',  pro: '15/day', unlimited: 'Unlimited' },
  { icon: '✏️', name: 'Assignment Helper',  free: '5/day',  pro: '30/day', unlimited: 'Unlimited' },
  { icon: '🔬', name: 'Research Summarizer',free: '5/day',  pro: '30/day', unlimited: 'Unlimited' },
];

export default function PricingPage() {
  const router = useRouter();
  const [user, setUser] = useState(null);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    setReady(true);
    const stored = getStoredUser();
    setUser(stored);
  }, []);

  const handleCTA = (planId) => {
    if (!getToken()) { router.push('/auth/register'); return; }
    if (planId === 'free') { router.push('/dashboard'); return; }
    // For paid plans — redirect to dashboard with upgrade note
    alert(`To upgrade to ${planId} plan, please contact support or set up Stripe billing. Your admin can manually upgrade your account.`);
  };

  if (!ready) return null;

  return (
    <div className="min-h-screen nebula-bg relative overflow-hidden">
      <Starfield />
      <div className="relative z-10">
        {/* Nav */}
        <nav className="flex items-center justify-between px-6 py-4 border-b border-white/5 bg-black/20 backdrop-blur-md">
          <Link href="/" className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-sm">🎓</div>
            <span className="font-display font-bold text-white text-lg">StudyHub</span>
          </Link>
          <div className="flex items-center gap-3">
            {user ? (
              <Link href="/dashboard"><Button variant="outline" size="sm">Dashboard</Button></Link>
            ) : (
              <>
                <Link href="/auth/login"><Button variant="ghost" size="sm">Sign in</Button></Link>
                <Link href="/auth/register"><Button size="sm">Get started free</Button></Link>
              </>
            )}
          </div>
        </nav>

        {/* Hero */}
        <div className="text-center px-6 pt-16 pb-12">
          <div className="inline-flex items-center gap-2 bg-blue-500/10 border border-blue-500/20 rounded-full px-4 py-2 text-sm text-blue-300 font-semibold mb-6">
            ⚡ Simple, transparent pricing
          </div>
          <h1 className="text-4xl sm:text-5xl font-display font-bold text-white mb-4">
            Choose your plan
          </h1>
          <p className="text-ink-400 text-lg max-w-xl mx-auto">
            Start free, upgrade when you need more. All plans include all 5 AI tools.
          </p>
          {user && (
            <div className="mt-4 inline-flex items-center gap-2 bg-white/5 border border-white/10 rounded-xl px-4 py-2 text-sm text-ink-300">
              You're on the <span className="font-bold text-white capitalize ml-1">{user.plan}</span> plan
            </div>
          )}
        </div>

        {/* Pricing Cards */}
        <div className="max-w-6xl mx-auto px-6 pb-16">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-16">
            {PLANS.map(plan => {
              const isCurrent = user?.plan === plan.id;
              const borderColor = plan.color === 'purple' ? 'rgba(139,92,246,0.4)' : plan.color === 'gold' ? 'rgba(245,158,11,0.3)' : 'rgba(255,255,255,0.08)';
              const glowColor = plan.color === 'purple' ? 'rgba(139,92,246,0.15)' : plan.color === 'gold' ? 'rgba(245,158,11,0.1)' : 'transparent';
              const textColor = plan.color === 'purple' ? '#a78bfa' : plan.color === 'gold' ? '#fbbf24' : '#60a5fa';
              return (
                <div
                  key={plan.id}
                  className={cn('relative rounded-2xl p-8 border transition-all duration-300', plan.highlighted ? 'scale-[1.02]' : '')}
                  style={{
                    background: plan.highlighted
                      ? 'linear-gradient(135deg, rgba(20,10,50,0.95) 0%, rgba(10,5,30,0.98) 100%)'
                      : 'linear-gradient(135deg, rgba(10,22,40,0.85) 0%, rgba(6,13,24,0.95) 100%)',
                    borderColor,
                    boxShadow: plan.highlighted ? `0 0 60px ${glowColor}, 0 20px 60px rgba(0,0,0,0.5)` : '0 4px 30px rgba(0,0,0,0.4)',
                  }}
                >
                  {plan.badge && (
                    <div className="absolute -top-3.5 left-1/2 -translate-x-1/2 px-4 py-1 rounded-full text-xs font-bold text-white"
                      style={{ background: plan.color === 'purple' ? 'linear-gradient(135deg,#7c3aed,#a78bfa)' : 'linear-gradient(135deg,#d97706,#fbbf24)' }}>
                      {plan.badge}
                    </div>
                  )}

                  <div className="mb-6">
                    <h3 className="text-xl font-display font-bold text-white mb-1">{plan.name}</h3>
                    <p className="text-ink-500 text-sm mb-4">{plan.description}</p>
                    <div className="flex items-baseline gap-1">
                      <span className="text-4xl font-display font-bold" style={{ color: textColor }}>{plan.price}</span>
                      <span className="text-ink-500 text-sm">{plan.period}</span>
                    </div>
                  </div>

                  <Button
                    onClick={() => handleCTA(plan.id)}
                    className="w-full mb-6"
                    size="lg"
                    variant={plan.highlighted ? 'primary' : isCurrent ? 'secondary' : 'outline'}
                    disabled={isCurrent}
                  >
                    {isCurrent ? '✓ Current Plan' : plan.cta}
                  </Button>

                  <ul className="space-y-3">
                    {plan.features.map((f, i) => (
                      <li key={i} className="flex items-start gap-2.5 text-sm text-ink-300">
                        <span style={{ color: textColor }} className="flex-shrink-0 mt-0.5">✓</span>
                        {f}
                      </li>
                    ))}
                  </ul>
                </div>
              );
            })}
          </div>

          {/* Feature comparison table */}
          <div className="glass-card rounded-2xl overflow-hidden">
            <div className="px-6 py-5 border-b border-white/5">
              <h2 className="text-xl font-display font-bold text-white">Full Feature Comparison</h2>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-white/5">
                    <th className="text-left px-6 py-4 text-ink-400 font-semibold">Tool</th>
                    <th className="text-center px-6 py-4 text-blue-300 font-semibold">Free</th>
                    <th className="text-center px-6 py-4 text-purple-300 font-semibold">Pro</th>
                    <th className="text-center px-6 py-4 text-amber-300 font-semibold">Unlimited</th>
                  </tr>
                </thead>
                <tbody>
                  {TOOLS_LIST.map((tool, i) => (
                    <tr key={i} className={cn('border-b border-white/4 hover:bg-white/2 transition-colors', i % 2 === 0 && 'bg-white/1')}>
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-2.5">
                          <span>{tool.icon}</span>
                          <span className="text-ink-200 font-medium">{tool.name}</span>
                        </div>
                      </td>
                      <td className="text-center px-6 py-4 text-blue-300 font-semibold">{tool.free}</td>
                      <td className="text-center px-6 py-4 text-purple-300 font-semibold">{tool.pro}</td>
                      <td className="text-center px-6 py-4 text-amber-300 font-semibold">{tool.unlimited}</td>
                    </tr>
                  ))}
                  <tr className="border-b border-white/4">
                    <td className="px-6 py-4 text-ink-200 font-medium">Daily limit reset</td>
                    <td className="text-center px-6 py-4 text-ink-300">Midnight</td>
                    <td className="text-center px-6 py-4 text-ink-300">Midnight</td>
                    <td className="text-center px-6 py-4 text-amber-300">No limits</td>
                  </tr>
                  <tr>
                    <td className="px-6 py-4 text-ink-200 font-medium">Chat history</td>
                    <td className="text-center px-6 py-4 text-green-400">✓</td>
                    <td className="text-center px-6 py-4 text-green-400">✓</td>
                    <td className="text-center px-6 py-4 text-green-400">✓</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          {/* FAQ */}
          <div className="mt-16 text-center">
            <h2 className="text-2xl font-display font-bold text-white mb-8">Common Questions</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-left">
              {[
                ['Do daily limits really reset?', 'Yes — every midnight. Your usage counter goes back to zero and you start fresh.'],
                ['Can I use one email for multiple accounts?', 'No — each email address can only have one StudyHub account. This keeps the platform fair for everyone.'],
                ['What AI powers the tools?', 'StudyHub uses a built-in knowledge engine plus optional Hugging Face AI (free). No OpenAI costs required.'],
                ['How do I upgrade to Pro?', 'Contact support or ask your administrator. Stripe billing integration is available for automated upgrades.'],
              ].map(([q, a], i) => (
                <div key={i} className="glass-card rounded-xl p-5">
                  <h3 className="text-white font-semibold mb-2">{q}</h3>
                  <p className="text-ink-400 text-sm leading-relaxed">{a}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
