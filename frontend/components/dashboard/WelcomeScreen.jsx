'use client';
import { cn, TOOLS } from '../../lib/utils';

export function WelcomeScreen({ onToolSelect, userName }) {
  const hour = new Date().getHours();
  const greeting = hour<12?'Good morning':hour<17?'Good afternoon':'Good evening';
  return (
    <div className="flex-1 flex flex-col items-center justify-center px-6 py-12 overflow-y-auto">
      <div className="max-w-2xl w-full text-center animate-fade-up">
        <div className="mb-2 text-4xl">🎓</div>
        <h1 className="text-3xl font-display font-bold text-ink-50 mb-2">
          {greeting}{userName ? `, ${userName.split(' ')[0]}` : ''}
        </h1>
        <p className="text-ink-400 mb-12 text-base">What would you like to work on today?</p>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {Object.values(TOOLS).map((tool,i)=>(
            <button key={tool.id} onClick={()=>onToolSelect(tool.id)}
              className={cn('group text-left p-5 rounded-2xl border transition-all duration-200 hover:scale-[1.02] hover:shadow-xl active:scale-[0.98] animate-fade-up',
                tool.color==='gold' ?'bg-gold-500/5  border-gold-500/15 hover:bg-gold-500/10 hover:border-gold-500/30 hover:shadow-gold-500/10':
                tool.color==='jade' ?'bg-jade-500/5  border-jade-500/15 hover:bg-jade-500/10 hover:border-jade-500/30 hover:shadow-jade-500/10':
                                     'bg-coral-500/5 border-coral-500/15 hover:bg-coral-500/10 hover:border-coral-500/30 hover:shadow-coral-500/10')}
              style={{animationDelay:`${i*0.07}s`}}>
              <div className="text-2xl mb-3">{tool.icon}</div>
              <h3 className={cn('font-display font-bold text-sm mb-1',
                tool.color==='gold'?'text-gold-300':tool.color==='jade'?'text-jade-300':'text-coral-300')}>
                {tool.label}
              </h3>
              <p className="text-xs text-ink-500 leading-relaxed">{tool.description}</p>
              <div className={cn('mt-4 text-[10px] font-bold uppercase tracking-widest opacity-0 group-hover:opacity-100 transition-opacity',
                tool.color==='gold'?'text-gold-500':tool.color==='jade'?'text-jade-500':'text-coral-400')}>
                Start chatting →
              </div>
            </button>
          ))}
        </div>

        <div className="mt-12 flex items-center justify-center gap-8 text-center">
          {[{icon:'📚',label:'AI-Powered'},{icon:'⚡',label:'Instant Results'},{icon:'🔒',label:'Secure & Private'}].map(item=>(
            <div key={item.label} className="flex flex-col items-center gap-1">
              <span className="text-xl">{item.icon}</span>
              <span className="text-xs text-ink-600 font-medium">{item.label}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
