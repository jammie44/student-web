import { cn } from '../../lib/utils';
const V={gold:'bg-gold-500/15 text-gold-300 border border-gold-500/30',jade:'bg-jade-500/15 text-jade-400 border border-jade-500/30',coral:'bg-coral-500/15 text-coral-400 border border-coral-500/30',neutral:'bg-ink-800 text-ink-400 border border-ink-700',active:'bg-jade-500/20 text-jade-400 border border-jade-500/40',inactive:'bg-ink-800 text-ink-500 border border-ink-700'};
export function Badge({children,variant='neutral',className}){
  return <span className={cn('inline-flex items-center px-2 py-0.5 rounded-md text-xs font-semibold',V[variant],className)}>{children}</span>;
}
