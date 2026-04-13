'use client';
import Link from'next/link';
import{cn,TOOLS,TOOL_COLORS}from'../../lib/utils';
export function WelcomeScreen({onToolSelect,userName,usage}){
  const h=new Date().getHours();
  const greeting=h<12?'Good morning':h<17?'Good afternoon':'Good evening';
  const plan=usage?.plan||'free';
  return(
    <div className="flex flex-col items-center justify-center h-full px-6 py-12 overflow-y-auto">
      <div className="max-w-2xl w-full text-center">
        <div className="text-5xl mb-4 animate-float">🎓</div>
        <h1 className="text-3xl font-bold text-white mb-2 animate-fade-up" style={{fontFamily:'Syne,sans-serif'}}>
          {greeting}{userName?`, ${userName.split(' ')[0]}`:''}
        </h1>
        <p className="mb-3 text-base animate-fade-up delay-1" style={{color:'#64748b'}}>What would you like to work on today?</p>
        <div className="inline-flex items-center gap-2 mb-10 px-4 py-2 rounded-xl border animate-fade-up delay-2" style={{background:'rgba(255,255,255,0.03)',borderColor:'rgba(255,255,255,0.08)'}}>
          {plan==='pro'?<span className="text-sm font-bold" style={{color:'#f59e0b'}}>⭐ Pro Plan</span>:plan==='unlimited'?<span className="text-sm font-bold" style={{color:'#a78bfa'}}>♾ Unlimited Plan</span>:<><span className="text-sm" style={{color:'#64748b'}}>🆓 Free Plan</span><span style={{color:'#334155'}}>·</span><Link href="/pricing" className="text-sm font-semibold" style={{color:'#60a5fa'}}>Upgrade →</Link></>}
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {Object.values(TOOLS).map((tool,i)=>{
            const col=TOOL_COLORS[tool.color];
            const u=usage?.usage?.[tool.id];
            const pct=u?Math.min(100,(u.used/u.limit)*100):0;
            return(
              <button key={tool.id} onClick={()=>!u?.exhausted&&onToolSelect(tool.id)} disabled={u?.exhausted}
                className={cn('group text-left p-5 rounded-2xl border transition-all duration-200 relative overflow-hidden animate-fade-up',`delay-${i+1}`,u?.exhausted?'opacity-50 cursor-not-allowed':'hover:scale-[1.02] active:scale-[0.99]')}
                style={{background:col.bg,borderColor:col.border}}>
                <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-2xl" style={{boxShadow:`inset 0 0 30px ${col.glow}`}}/>
                <div className="relative">
                  <div className="text-2xl mb-3">{tool.icon}</div>
                  <h3 className="font-bold text-sm mb-1" style={{fontFamily:'Syne,sans-serif',color:u?.exhausted?'#475569':col.text}}>
                    {tool.label}{u?.exhausted&&<span className="ml-2 text-[10px] font-normal" style={{color:'#ef4444'}}>Limit reached</span>}
                  </h3>
                  <p className="text-xs leading-relaxed mb-3" style={{color:'#475569'}}>{tool.description}</p>
                  {u&&<div className="mb-2"><div className="flex justify-between text-[10px] mb-1" style={{color:'#334155'}}><span>{u.used}/{u.limit} today</span><span>{u.remaining} left</span></div><div className="usage-bar"><div className="usage-bar-fill" style={{width:`${pct}%`,background:pct>=100?'#ef4444':pct>=80?'#f59e0b':col.text}}/></div></div>}
                  <div className="text-[10px] font-bold uppercase tracking-widest opacity-0 group-hover:opacity-100 transition-opacity" style={{color:col.text}}>Start chatting →</div>
                </div>
              </button>
            );
          })}
        </div>
        <p className="mt-8 text-xs animate-fade-up" style={{color:'#334155'}}>All tools powered by AI · Daily limits reset at midnight · <Link href="/pricing" className="hover:underline" style={{color:'#60a5fa'}}>Upgrade for more</Link></p>
      </div>
    </div>
  );
}
