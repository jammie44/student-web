import { cn } from '../../lib/utils';
const V = {
  blue:    'bg-blue-500/15 text-blue-300 border border-blue-500/30',
  purple:  'bg-purple-500/15 text-purple-300 border border-purple-500/30',
  green:   'bg-emerald-500/15 text-emerald-300 border border-emerald-500/30',
  gold:    'bg-amber-500/15 text-amber-300 border border-amber-500/30',
  red:     'bg-red-500/15 text-red-300 border border-red-500/30',
  neutral: 'bg-white/5 text-ink-300 border border-white/10',
  active:  'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40',
  inactive:'bg-white/5 text-ink-500 border border-white/8',
};
export function Badge({ children, variant = 'neutral', className }) {
  return <span className={cn('inline-flex items-center px-2 py-0.5 rounded-md text-xs font-semibold', V[variant], className)}>{children}</span>;
}
