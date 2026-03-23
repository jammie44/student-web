'use client';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function Home() {
  const router = useRouter();
  useEffect(() => {
    const token = typeof window !== 'undefined' && localStorage.getItem('studyhub_token');
    router.replace(token ? '/dashboard' : '/auth/login');
  }, [router]);
  return (
    <div className="min-h-screen flex items-center justify-center bg-ink-950">
      <div className="w-8 h-8 border-2 border-ink-700 border-t-gold-500 rounded-full animate-spin" />
    </div>
  );
}
