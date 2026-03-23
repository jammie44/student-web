'use client';
import { cn } from '../../lib/utils';
const V={ primary:'bg-gold-500 hover:bg-gold-400 text-ink-950 font-semibold shadow-lg shadow-gold-500/20', secondary:'bg-ink-800 hover:bg-ink-700 text-ink-100 border border-ink-700', ghost:'bg-transparent hover:bg-ink-800 text-ink-300 hover:text-ink-100', danger:'bg-coral-500 hover:bg-coral-400 text-white font-semibold', outline:'bg-transparent border border-ink-700 hover:border-gold-500 text-ink-300 hover:text-gold-400' };
const S={ sm:'px-3 py-1.5 text-sm rounded-lg', md:'px-4 py-2.5 text-sm rounded-xl', lg:'px-6 py-3 text-base rounded-xl', xl:'px-8 py-4 text-base rounded-2xl' };
export function Button({ children, variant='primary', size='md', className, loading, disabled, icon, ...p }) {
  return (
    <button disabled={disabled||loading} className={cn('inline-flex items-center justify-center gap-2 font-medium transition-all duration-150 active:scale-[0.97] disabled:opacity-50 disabled:cursor-not-allowed disabled:active:scale-100', V[variant], S[size], className)} {...p}>
      {loading ? <><span className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin"/>{children}</> : <>{icon && <span>{icon}</span>}{children}</>}
    </button>
  );
}
