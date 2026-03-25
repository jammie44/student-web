'use client';
import { cn, TOOLS } from '../../lib/utils';

export function WelcomeScreen({ onToolSelect, userName, credits }) {
  const hour = new Date().getHours();
  const greeting = hour < 12 ? 'Good morning' : hour < 17 ? 'Good afternoon' : 'Good evening';

  const costs = { study_assistant: 2, plagiarism: 3, cv_generator: 5, assignment: 4, research: 3 };

  return (
    <div className="flex-1 flex flex-col items-center justify-center px-6 py-12 overflow-y-auto">
      <div className="max-w-2xl w-full text-center">

        {/* Greeting */}
        <div className="mb-2 text-4xl">🎓</div>
        <h1 className="text-3xl font-display font-bold text-ink-50 mb-2">
          {greeting}{userName ? `, ${userName.split(' ')[0]}` : ''}
        </h1>
        <p className="text-ink-400 mb-3 text-base">What would you like to work on today?</p>

        {/* Credits badge */}
        {credits !== null && credits !== undefined && (
          <div className="inline-flex items-center gap-2 mb-10 px-4 py-2 rounded-xl border bg-ink-900/60 border-ink-800">
            <span className={cn('text-sm font-bold', credits > 20 ? 'text-gold-400' : credits > 5 ? 'text-amber-400' : 'text-coral-400')}>
              ⚡ {credits} credits remaining
            </span>
            {credits < 10 && (
              <span className="text-xs text-ink-500">· Running low</span>
            )}
          </div>
        )}

        {/* Tool grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {Object.values(TOOLS).map((tool, i) => (
            <button
              key={tool.id}
              onClick={() => onToolSelect(tool.id)}
              className={cn(
                'group text-left p-5 rounded-2xl border transition-all duration-200 hover:scale-[1.02] active:scale-[0.98] relative overflow-hidden',
                tool.color === 'gold'  ? 'bg-gold-500/5  border-gold-500/15 hover:bg-gold-500/10 hover:border-gold-500/40 hover:shadow-lg hover:shadow-gold-500/10' :
                tool.color === 'jade'  ? 'bg-jade-500/5  border-jade-500/15 hover:bg-jade-500/10 hover:border-jade-500/40 hover:shadow-lg hover:shadow-jade-500/10' :
                                         'bg-coral-500/5 border-coral-500/15 hover:bg-coral-500/10 hover:border-coral-500/40 hover:shadow-lg hover:shadow-coral-500/10'
              )}
            >
              <div className="text-2xl mb-3">{tool.icon}</div>
              <h3 className={cn(
                'font-display font-bold text-sm mb-1',
                tool.color === 'gold'  ? 'text-gold-300' :
                tool.color === 'jade'  ? 'text-jade-300' : 'text-coral-300'
              )}>
                {tool.label}
              </h3>
              <p className="text-xs text-ink-500 leading-relaxed mb-3">{tool.description}</p>

              {/* Cost badge */}
              <div className={cn(
                'inline-flex items-center gap-1 text-[10px] font-bold px-2 py-0.5 rounded-md',
                tool.color === 'gold'  ? 'bg-gold-500/15 text-gold-500' :
                tool.color === 'jade'  ? 'bg-jade-500/15 text-jade-500' :
                'bg-coral-500/15 text-coral-400'
              )}>
                ⚡ {costs[tool.id]} credits per message
              </div>

              <div className={cn(
                'absolute bottom-4 right-4 text-[10px] font-bold uppercase tracking-widest opacity-0 group-hover:opacity-100 transition-opacity',
                tool.color === 'gold'  ? 'text-gold-500' :
                tool.color === 'jade'  ? 'text-jade-500' : 'text-coral-400'
              )}>
                Start →
              </div>
            </button>
          ))}
        </div>

        <p className="mt-8 text-xs text-ink-700">
          All tools powered by Claude AI · Responses are real, specific, and professional
        </p>
      </div>
    </div>
  );
}
