'use client';
import{Starfield}from'../layout/Starfield';
export function AuthLayout({children}){
  return(
    <div className="min-h-screen flex items-center justify-center relative overflow-hidden nebula-bg">
      <Starfield/>
      <div className="relative z-10 w-full max-w-md mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-3 mb-3">
            <div className="w-11 h-11 rounded-2xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-xl shadow-lg animate-float">🎓</div>
            <span className="text-2xl font-bold text-white tracking-tight" style={{fontFamily:'Syne,sans-serif'}}>StudyHub</span>
          </div>
          <p className="text-sm" style={{color:'#64748b'}}>Your AI-powered academic companion</p>
        </div>
        <div className="glass-card rounded-2xl p-8 shadow-2xl">{children}</div>
        <p className="text-center text-xs mt-5" style={{color:'#334155'}}>Free to use · No credit card required · AI-powered</p>
      </div>
    </div>
  );
}
