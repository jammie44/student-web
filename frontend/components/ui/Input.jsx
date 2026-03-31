'use client';
import { forwardRef } from 'react';
import { cn } from '../../lib/utils';

export const Input = forwardRef(({ label, error, hint, icon, className, type = 'text', ...p }, ref) => (
  <div className="space-y-1.5">
    {label && <label className="block text-xs font-semibold text-ink-300 uppercase tracking-wider">{label}</label>}
    <div className="relative">
      {icon && <div className="absolute left-3.5 top-1/2 -translate-y-1/2 text-ink-400 pointer-events-none">{icon}</div>}
      <input
        ref={ref} type={type}
        className={cn(
          'w-full rounded-xl px-4 py-3 text-sm text-ink-100 placeholder:text-ink-500 outline-none transition-all duration-150',
          'bg-white/5 border',
          error
            ? 'border-red-500/60 focus:border-red-400 focus:ring-2 focus:ring-red-500/20'
            : 'border-white/10 hover:border-white/20 focus:border-blue-500/60 focus:ring-2 focus:ring-blue-500/20 focus:bg-white/8',
          icon && 'pl-10', className
        )}
        {...p}
      />
    </div>
    {error && <p className="text-xs text-red-400">⚠ {error}</p>}
    {hint && !error && <p className="text-xs text-ink-500">{hint}</p>}
  </div>
));
Input.displayName = 'Input';
