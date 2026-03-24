'use client';
import { forwardRef } from 'react';
import { cn } from '../../lib/utils';
export const Input = forwardRef(({label,error,hint,icon,className,type='text',...p},ref)=>(
  <div className="space-y-1.5">
    {label&&<label className="block text-xs font-semibold text-ink-400 uppercase tracking-wider">{label}</label>}
    <div className="relative">
      {icon&&<div className="absolute left-3.5 top-1/2 -translate-y-1/2 text-ink-500 pointer-events-none text-sm">{icon}</div>}
      <input ref={ref} type={type} className={cn('w-full bg-ink-900/80 border rounded-xl px-4 py-3 text-sm text-ink-100 placeholder:text-ink-600 outline-none transition-all duration-150 focus:ring-2',error?'border-coral-500 focus:border-coral-500 focus:ring-coral-500/20':'border-ink-700 hover:border-ink-600 focus:border-gold-500 focus:ring-gold-500/20 focus:bg-ink-900',icon&&'pl-10',className)} {...p}/>
    </div>
    {error&&<p className="text-xs text-coral-400">⚠ {error}</p>}
    {hint&&!error&&<p className="text-xs text-ink-500">{hint}</p>}
  </div>
));
Input.displayName='Input';
