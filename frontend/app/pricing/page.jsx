'use client';
import{useState,useEffect}from'react';
import Link from'next/link';
import{Starfield}from'../../components/layout/Starfield';
import{Button}from'../../components/ui/Button';
import{cn}from'../../lib/utils';
import{getToken,getStoredUser}from'../../lib/auth';

const PLANS=[
  {id:'free',name:'Free',price:'$0',period:'forever',desc:'Perfect for getting started',textColor:'#60a5fa',borderColor:'rgba(59,130,246,0.2)',bg:'rgba(10,22,40,0.85)',features:['10 Study Assistant/day','5 Plagiarism checks/day','3 CV generations/day','5 Assignment formats/day','5 Research summaries/day','Full chat history','All 5 AI tools'],cta:'Get Started Free',highlighted:false},
  {id:'pro',name:'Pro',price:'$9.99',period:'/month',desc:'For serious students',textColor:'#a78bfa',borderColor:'rgba(139,92,246,0.45)',bg:'rgba(20,10,50,0.95)',badge:'Most Popular',features:['50 Study Assistant/day','30 Plagiarism checks/day','15 CV generations/day','30 Assignment formats/day','30 Research summaries/day','Priority AI responses','All 5 AI tools','Email support'],cta:'Upgrade to Pro',highlighted:true},
  {id:'unlimited',name:'Unlimited',price:'$19.99',period:'/month',desc:'For power users & educators',textColor:'#fbbf24',borderColor:'rgba(245,158,11,0.3)',bg:'rgba(10,22,40,0.85)',badge:'Best Value',features:['Unlimited Study Assistant','Unlimited Plagiarism','Unlimited CV Generator','Unlimited Assignments','Unlimited Research','Fastest responses','All 5 AI tools','Priority support','Early access to new tools'],cta:'Go Unlimited',highlighted:false},
];

const COMPARE=[
  {icon:'🎓',name:'Study Assistant',free:'10/day',pro:'50/day',unlimited:'Unlimited'},
  {icon:'🔍',name:'Plagiarism Checker',free:'5/day',pro:'30/day',unlimited:'Unlimited'},
  {icon:'📄',name:'CV Generator',free:'3/day',pro:'15/day',unlimited:'Unlimited'},
  {icon:'✏️',name:'Assignment Helper',free:'5/day',pro:'30/day',unlimited:'Unlimited'},
  {icon:'🔬',name:'Research Summarizer',free:'5/day',pro:'30/day',unlimited:'Unlimited'},
  {icon:'💾',name:'Chat History',free:'✓',pro:'✓',unlimited:'✓'},
  {icon:'⏰',name:'Daily Reset',free:'Midnight',pro:'Midnight',unlimited:'No limits'},
];

const FAQ=[
  ['Do daily limits really reset?','Yes — every day at midnight your usage resets automatically. You start fresh every morning.'],
  ['One email, one account?','Correct — each email address can only have one StudyHub account, keeping the platform fair.'],
  ['What AI powers the tools?','A built-in knowledge engine covering maths, science, history, philosophy, CS, and more. No external API fees.'],
  ['How do I upgrade?','Contact support or ask your administrator to update your plan from the admin dashboard.'],
];

export default function PricingPage(){
  const[user,setUser]=useState(null);
  useEffect(()=>{const s=getStoredUser();if(s)setUser(s);},[]);

  const handleCTA=plan=>{
    if(!getToken()){window.location.href='/auth/register';return;}
    if(plan==='free'){window.location.href='/dashboard';return;}
    alert(`To upgrade to ${plan}, ask your administrator to change your plan from the admin dashboard.`);
  };

  return(
    <div className="min-h-screen nebula-bg relative overflow-hidden">
      <Starfield/>
      <div className="relative z-10">
        <nav className="flex items-center justify-between px-6 py-4 border-b" style={{background:'rgba(0,0,0,0.2)',backdropFilter:'blur(12px)',borderColor:'rgba(255,255,255,0.05)'}}>
          <Link href="/" className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-xl flex items-center justify-center text-sm" style={{background:'linear-gradient(135deg,#3b82f6,#7c3aed)'}}>🎓</div>
            <span className="font-bold text-white text-lg" style={{fontFamily:'Syne,sans-serif'}}>StudyHub</span>
          </Link>
          <div className="flex items-center gap-3">
            {user?<Link href="/dashboard"><Button variant="outline" size="sm">Dashboard</Button></Link>:
            <><Link href="/auth/login"><Button variant="ghost" size="sm">Sign in</Button></Link><Link href="/auth/register"><Button size="sm">Get started free</Button></Link></>}
          </div>
        </nav>

        <div className="text-center px-6 pt-16 pb-12">
          <div className="inline-flex items-center gap-2 mb-6 px-4 py-2 rounded-full text-sm font-semibold" style={{background:'rgba(59,130,246,0.1)',border:'1px solid rgba(59,130,246,0.2)',color:'#93c5fd'}}>⚡ Simple, transparent pricing</div>
          <h1 className="text-4xl sm:text-5xl font-bold text-white mb-4" style={{fontFamily:'Syne,sans-serif'}}>Choose your plan</h1>
          <p className="text-lg max-w-xl mx-auto mb-4" style={{color:'#64748b'}}>Start free. Upgrade when you need more. All plans include all 5 AI tools.</p>
          {user&&<div className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-sm" style={{background:'rgba(255,255,255,0.05)',border:'1px solid rgba(255,255,255,0.1)',color:'#94a3b8'}}>You're on the <span className="font-bold text-white capitalize mx-1">{user.plan}</span> plan</div>}
        </div>

        <div className="max-w-5xl mx-auto px-6 pb-16">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-16">
            {PLANS.map(plan=>{
              const isCurrent=user?.plan===plan.id;
              return(
                <div key={plan.id} className={cn('relative rounded-2xl p-8 border transition-all duration-300',plan.highlighted&&'scale-[1.02]')}
                  style={{background:plan.bg,borderColor:plan.borderColor,boxShadow:plan.highlighted?'0 0 60px rgba(139,92,246,0.18),0 20px 60px rgba(0,0,0,0.5)':'0 4px 30px rgba(0,0,0,0.4)'}}>
                  {plan.badge&&(
                    <div className="absolute -top-3.5 left-1/2 -translate-x-1/2 px-4 py-1 rounded-full text-xs font-bold text-white"
                      style={{background:plan.id==='pro'?'linear-gradient(135deg,#7c3aed,#a78bfa)':'linear-gradient(135deg,#d97706,#fbbf24)'}}>
                      {plan.badge}
                    </div>
                  )}
                  <div className="mb-6">
                    <h3 className="text-xl font-bold text-white mb-1" style={{fontFamily:'Syne,sans-serif'}}>{plan.name}</h3>
                    <p className="text-sm mb-4" style={{color:'#475569'}}>{plan.desc}</p>
                    <div className="flex items-baseline gap-1">
                      <span className="text-4xl font-bold" style={{fontFamily:'Syne,sans-serif',color:plan.textColor}}>{plan.price}</span>
                      <span className="text-sm" style={{color:'#475569'}}>{plan.period}</span>
                    </div>
                  </div>
                  <Button onClick={()=>handleCTA(plan.id)} className="w-full mb-6" size="lg"
                    variant={plan.highlighted?'primary':isCurrent?'secondary':'outline'} disabled={isCurrent}>
                    {isCurrent?'✓ Current Plan':plan.cta}
                  </Button>
                  <ul className="space-y-3">
                    {plan.features.map((f,i)=>(
                      <li key={i} className="flex items-start gap-2.5 text-sm" style={{color:'#94a3b8'}}>
                        <span className="flex-shrink-0 mt-0.5" style={{color:plan.textColor}}>✓</span>{f}
                      </li>
                    ))}
                  </ul>
                </div>
              );
            })}
          </div>

          <div className="rounded-2xl overflow-hidden mb-16 glass-card">
            <div className="px-6 py-5 border-b" style={{borderColor:'rgba(255,255,255,0.05)'}}>
              <h2 className="text-xl font-bold text-white" style={{fontFamily:'Syne,sans-serif'}}>Full Comparison</h2>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b" style={{borderColor:'rgba(255,255,255,0.05)'}}>
                    <th className="text-left px-6 py-4 font-semibold" style={{color:'#64748b'}}>Feature</th>
                    <th className="text-center px-6 py-4 font-semibold" style={{color:'#93c5fd'}}>Free</th>
                    <th className="text-center px-6 py-4 font-semibold" style={{color:'#c4b5fd'}}>Pro</th>
                    <th className="text-center px-6 py-4 font-semibold" style={{color:'#fcd34d'}}>Unlimited</th>
                  </tr>
                </thead>
                <tbody>
                  {COMPARE.map((row,i)=>(
                    <tr key={i} className="border-b" style={{borderColor:'rgba(255,255,255,0.04)',background:i%2===0?'rgba(255,255,255,0.01)':'transparent'}}>
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-2.5"><span>{row.icon}</span><span className="font-medium" style={{color:'#e2e8f0'}}>{row.name}</span></div>
                      </td>
                      <td className="text-center px-6 py-4 font-semibold" style={{color:'#93c5fd'}}>{row.free}</td>
                      <td className="text-center px-6 py-4 font-semibold" style={{color:'#c4b5fd'}}>{row.pro}</td>
                      <td className="text-center px-6 py-4 font-semibold" style={{color:'#fcd34d'}}>{row.unlimited}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <h2 className="text-2xl font-bold text-white mb-8 text-center" style={{fontFamily:'Syne,sans-serif'}}>Common Questions</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {FAQ.map(([q,a],i)=>(
              <div key={i} className="glass-card rounded-xl p-5">
                <h3 className="text-white font-semibold mb-2">{q}</h3>
                <p className="text-sm leading-relaxed" style={{color:'#64748b'}}>{a}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
