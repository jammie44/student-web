'use client';
import{forwardRef}from'react';
import{cn}from'../../lib/utils';
export const Input=forwardRef(({label,error,className,type='text',...p},ref)=>(
  <div className="space-y-1.5">
    {label&&<label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider">{label}</label>}
    <input ref={ref} type={type} className={cn('w-full rounded-xl px-4 py-3 text-sm text-slate-100 placeholder:text-slate-500 outline-none transition-all bg-white/5 border',error?'border-red-500/60 focus:border-red-400 focus:ring-2 focus:ring-red-500/20':'border-white/10 hover:border-white/20 focus:border-blue-500/60 focus:ring-2 focus:ring-blue-500/20',className)} {...p}/>
    {error&&<p className="text-xs text-red-400">⚠ {error}</p>}
  </div>
));
Input.displayName='Input';
