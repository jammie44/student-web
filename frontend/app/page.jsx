'use client';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
export default function Home() {
  const router = useRouter();
  useEffect(() => {
    router.replace(typeof window !== 'undefined' && localStorage.getItem('sh_token') ? '/dashboard' : '/auth/login');
  }, [router]);
  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#020408' }}>
      <div style={{ width: 32, height: 32, border: '2px solid #1e3a5f', borderTop: '2px solid #4f8ef7', borderRadius: '50%', animation: 'spin 1s linear infinite' }} />
      <style>{`@keyframes spin{to{transform:rotate(360deg)}}`}</style>
    </div>
  );
}
