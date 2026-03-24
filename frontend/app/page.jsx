'use client';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
export default function Home() {
  const router = useRouter();
  useEffect(() => {
    router.replace(localStorage.getItem('studyhub_token') ? '/dashboard' : '/auth/login');
  }, [router]);
  return (
    <div style={{minHeight:'100vh',display:'flex',alignItems:'center',justifyContent:'center',background:'#1e1c18'}}>
      <div style={{width:32,height:32,border:'2px solid #524d43',borderTop:'2px solid #fbbf24',borderRadius:'50%',animation:'spin 1s linear infinite'}}/>
      <style>{`@keyframes spin{to{transform:rotate(360deg)}}`}</style>
    </div>
  );
}
