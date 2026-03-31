import { cn } from '../../lib/utils';
export function Spinner({ size = 'md', className }) {
  const S = { sm: 'w-4 h-4', md: 'w-6 h-6', lg: 'w-10 h-10' };
  return <div className={cn('border-2 border-white/10 border-t-blue-400 rounded-full animate-spin', S[size], className)} />;
}
export function LoadingDots() {
  return (
    <div className="flex items-center gap-1.5">
      <div className="loading-dot" />
      <div className="loading-dot" />
      <div className="loading-dot" />
    </div>
  );
}
