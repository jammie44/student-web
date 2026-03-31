'use client';
import { Starfield } from '../layout/Starfield';

export function AuthLayout({ children }) {
  return (
    <div className="min-h-screen flex items-center justify-center relative overflow-hidden nebula-bg">
      <Starfield />
      <div className="relative z-10 w-full max-w-md mx-auto px-4 py-8">
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-3 mb-3">
            <div className="w-11 h-11 rounded-2xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-xl shadow-lg shadow-blue-500/30 animate-float">
              🎓
            </div>
            <span className="text-2xl font-display font-bold text-white tracking-tight">StudyHub</span>
          </div>
          <p className="text-ink-400 text-sm">Your AI-powered academic companion</p>
        </div>
        {/* Card */}
        <div className="glass-card rounded-2xl p-8 shadow-2xl">
          {children}
        </div>
        <p className="text-center text-xs text-ink-500 mt-6">
          Powered by AI · Free to use · No credit card required
        </p>
      </div>
    </div>
  );
}
