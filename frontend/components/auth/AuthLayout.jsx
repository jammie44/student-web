'use client';
export function AuthLayout({children}){
  return(
    <div className="min-h-screen flex items-center justify-center relative overflow-hidden" style={{background:'radial-gradient(ellipse at 20% 50%, #2a1f0a 0%, #1e1c18 50%, #0f0e0c 100%)'}}>
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-96 h-96 bg-gold-500/5 rounded-full blur-3xl"/>
        <div className="absolute -bottom-40 -left-40 w-96 h-96 bg-gold-600/5 rounded-full blur-3xl"/>
        <div className="absolute inset-0 opacity-[0.03]" style={{backgroundImage:'linear-gradient(#fbbf24 1px,transparent 1px),linear-gradient(90deg,#fbbf24 1px,transparent 1px)',backgroundSize:'60px 60px'}}/>
      </div>
      <div className="relative w-full max-w-md mx-auto px-4 py-8">
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-2xl bg-gold-500 flex items-center justify-center text-xl shadow-lg shadow-gold-500/30">🎓</div>
            <span className="text-2xl font-display font-bold text-ink-50 tracking-tight">StudyHub</span>
          </div>
          <p className="text-ink-500 text-sm">Your AI-powered academic companion</p>
        </div>
        <div className="glass-card rounded-2xl p-8 shadow-2xl">{children}</div>
      </div>
    </div>
  );
}
