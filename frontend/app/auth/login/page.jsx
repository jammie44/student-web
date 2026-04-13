'use client';
import{useState,useEffect}from'react';
import{useRouter}from'next/navigation';
import Link from'next/link';
import{AuthLayout}from'../../../components/auth/AuthLayout';
import{Input}from'../../../components/ui/Input';
import{Button}from'../../../components/ui/Button';
import{api}from'../../../lib/api';
import{saveAuth,getToken}from'../../../lib/auth';

export default function LoginPage(){
  const router=useRouter();
  const[form,setForm]=useState({email:'',password:''});
  const[errors,setErrors]=useState({});
  const[serverError,setServerError]=useState(null);
  const[loading,setLoading]=useState(false);
  const[ready,setReady]=useState(false);

  useEffect(()=>{if(getToken()){router.replace('/dashboard');return;}setReady(true);},[router]);
  if(!ready)return null;

  const validate=()=>{
    const e={};
    if(!form.email)e.email='Email is required.';
    else if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email))e.email='Enter a valid email.';
    if(!form.password)e.password='Password is required.';
    return e;
  };

  const handleSubmit=async ev=>{
    ev.preventDefault();setServerError(null);
    const errs=validate();if(Object.keys(errs).length){setErrors(errs);return;}
    setErrors({});setLoading(true);
    try{const data=await api.login(form.email,form.password);saveAuth(data.access_token,data.user);router.push('/dashboard');}
    catch(err){setServerError(err.message||'Login failed. Please try again.');}
    finally{setLoading(false);}
  };

  return(
    <AuthLayout>
      <h1 className="text-2xl font-bold text-white mb-1" style={{fontFamily:'Syne,sans-serif'}}>Welcome back</h1>
      <p className="text-sm mb-7" style={{color:'#64748b'}}>
        No account?{' '}
        <Link href="/auth/register" className="font-semibold underline underline-offset-2" style={{color:'#60a5fa'}}>Create one free</Link>
      </p>

      {serverError&&(
        <div className="mb-5 p-4 rounded-xl text-sm" style={{background:'rgba(239,68,68,0.1)',border:'1px solid rgba(239,68,68,0.25)',color:'#fca5a5'}}>
          ⚠ {serverError}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-5" noValidate>
        <Input label="Email address" type="email" placeholder="you@university.edu"
          value={form.email} onChange={e=>setForm(p=>({...p,email:e.target.value}))}
          error={errors.email} autoComplete="email" autoFocus/>
        <Input label="Password" type="password" placeholder="••••••••••"
          value={form.password} onChange={e=>setForm(p=>({...p,password:e.target.value}))}
          error={errors.password} autoComplete="current-password"/>
        <Button type="submit" size="lg" className="w-full" loading={loading}>Sign in to StudyHub</Button>
      </form>

      <div className="mt-6 pt-5 text-center" style={{borderTop:'1px solid rgba(255,255,255,0.08)'}}>
        <p className="text-xs" style={{color:'#334155'}}>
          Demo: <span className="font-mono" style={{color:'#64748b'}}>demo@studyhub.com</span>{' / '}
          <span className="font-mono" style={{color:'#64748b'}}>Demo1234</span>
        </p>
      </div>
    </AuthLayout>
  );
}
