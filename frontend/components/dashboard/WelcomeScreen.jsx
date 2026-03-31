'use client';
import { cn, TOOLS, TOOL_COLORS } from '../../lib/utils';

export function WelcomeScreen({ onToolSelect, userName, usage }) {
  const hour = new Date().getHours();
  const greeting = hour < 12 ? 'Good morning' : hour < 17 ? 'Good afternoon' : 'Good evening';
  const plan = usage?.plan || 'free';

  return (
    <div className="flex flex-col items-center justify-center h-full px-6 py-12 overflow-y-auto">
      <div className="max-w-2xl w-full text-center">
        {/* Greeting */}
        <div className="text-5xl mb-4 animate-float">🎓</div>
        <h1 className="text-3xl font-display font-bold text-white mb-2 animate-fade-up">
          {greeting}{userName ? `, ${userName.split(' ')[0]}` : ''}
        </h1>
        <p className="text-ink-400 mb-3 text-base animate-fade-up delay-1">What would you like to work on today?</p>

        {/* Plan badge */}
        <div className="inline-flex items-center gap-2 mb-10 px-4 py-2 rounded-xl border bg-white/3 border-white/8 animate-fade-up delay-2">
          {plan === 'pro' ? (
            <span className="text-sm font-bold text-amber-400">⭐ Pro Plan — Enhanced Daily Limits</span>
          ) : plan === 'unlimited' ? (
            <span className="text-sm font-bold text-purple-400">♾ Unlimited Plan — No Limits</span>
          ) : (
            <>
              <span className="text-sm text-ink-400">🆓 Free Plan</span>
              <span className="text-ink-600">·</span>
              <a href="/pricing" className="text-sm text-blue-400 hover:text-blue-300 font-semibold transition-colors">Upgrade for more →</a>
            </>
          )}
        </div>

        {/* Tool grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {Object.values(TOOLS).map((tool, i) => {
            const col = TOOL_COLORS[tool.color];
            const u = usage?.usage?.[tool.id];
            const pct = u ? Math.min(100, (u.used / u.limit) * 100) : 0;
            const exhausted = u?.exhausted;
            return (
              <button
                key={tool.id}
                onClick={() => !exhausted && onToolSelect(tool.id)}
                className={cn(
                  `group text-left p-5 rounded-2xl border transition-all duration-200 animate-fade-up delay-${i + 1} relative overflow-hidden`,
                  exhausted
                    ? 'opacity-50 cursor-not-allowed border-white/5 bg-white/2'
                    : 'hover:scale-[1.02] active:scale-[0.99] cursor-pointer'
                )}
                style={exhausted ? {} : {
                  background: col.bg,
                  borderColor: col.border,
                }}
              >
                {/* Glow on hover */}
                {!exhausted && (
                  <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-2xl"
                    style={{ boxShadow: `inset 0 0 30px ${col.glow}` }} />
                )}
                <div className="relative">
                  <div className="text-2xl mb-3">{tool.icon}</div>
                  <h3 className="font-display font-bold text-sm mb-1" style={{ color: exhausted ? '#475569' : col.text }}>
                    {tool.label}
                    {exhausted && <span className="ml-2 text-[10px] text-red-400 font-normal">Limit reached</span>}
                  </h3>
                  <p className="text-xs text-ink-500 leading-relaxed mb-3">{tool.description}</p>

                  {/* Usage bar */}
                  {u && (
                    <div className="mb-2">
                      <div className="flex justify-between text-[10px] text-ink-600 mb-1">
                        <span>{u.used}/{u.limit} today</span>
                        <span>{u.remaining} left</span>
                      </div>
                      <div className="usage-bar">
                        <div className="usage-bar-fill" style={{
                          width: `${pct}%`,
                          background: pct >= 100 ? '#ef4444' : pct >= 80 ? '#f59e0b' : col.text,
                        }} />
                      </div>
                    </div>
                  )}

                  <div className="text-[10px] font-bold uppercase tracking-widest opacity-0 group-hover:opacity-100 transition-opacity"
                    style={{ color: col.text }}>
                    Start chatting →
                  </div>
                </div>
              </button>
            );
          })}
        </div>

        <p className="mt-8 text-xs text-ink-600 animate-fade-up">
          All tools powered by AI · Daily limits reset at midnight · <a href="/pricing" className="text-blue-400 hover:underline">Upgrade for more</a>
        </p>
      </div>
    </div>
  );
}
