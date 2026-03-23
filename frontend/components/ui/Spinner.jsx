import { cn } from '../../lib/utils';
const S={ sm:'w-4 h-4', md:'w-6 h-6', lg:'w-8 h-8', xl:'w-12 h-12' };
export function Spinner({ size='md', className }) {
  return <div className={cn('border-2 border-ink-700 border-t-gold-500 rounded-full animate-spin', S[size], className)}/>;
}
export function LoadingDots() {
  return <div className="flex items-center gap-1">{[0,1,2].map(i=><div key={i} className="w-2 h-2 rounded-full bg-gold-400 loading-dot" style={{animationDelay:`${i*0.2}s`}}/>)}</div>;
}
