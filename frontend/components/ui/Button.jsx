'use client';
import { cn } from '../../lib/utils';

const VARIANTS = {
  primary:   'bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-500 hover:to-blue-400 text-white font-semibold shadow-lg shadow-blue-500/25',
  secondary: 'bg-white/5 hover:bg-white/10 text-ink-100 border border-white/10 hover:border-white/20',
  ghost:     'bg-transparent hover:bg-white/5 text-ink-300 hover:text-ink-100',
  danger:    'bg-gradient-to-r from-red-600 to-red-500 hover:from-red-500 hover:to-red-400 text-white font-semibold',
  gold:      'bg-gradient-to-r from-amber-600 to-amber-500 hover:from-amber-500 hover:to-amber-400 text-white font-semibold shadow-lg shadow-amber-500/25',
  outline:   'bg-transparent border border-blue-500/40 hover:border-blue-500 text-blue-400 hover:text-blue-300 hover:bg-blue-500/10',
};
const SIZES = {
  sm: 'px-3 py-1.5 text-xs rounded-lg',
  md: 'px-4 py-2.5 text-sm rounded-xl',
  lg: 'px-6 py-3 text-base rounded-xl',
  xl: 'px-8 py-4 text-lg rounded-2xl',
};

export function Button({ children, variant = 'primary', size = 'md', className, loading, disabled, icon, ...p }) {
  return (
    <button
      disabled={disabled || loading}
      className={cn(
        'inline-flex items-center justify-center gap-2 font-medium transition-all duration-150 active:scale-[0.97] disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer',
        VARIANTS[variant], SIZES[size], className
      )}
      {...p}
    >
      {loading ? (
        <><div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />{children}</>
      ) : (
        <>{icon && <span>{icon}</span>}{children}</>
      )}
    </button>
  );
}
