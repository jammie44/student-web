'use client';
import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { AuthLayout } from '../../../components/auth/AuthLayout';
import { Input } from '../../../components/ui/Input';
import { Button } from '../../../components/ui/Button';
import { api } from '../../../lib/api';
import { saveAuth } from '../../../lib/auth';

function StrengthBar({ password }) {
  const checks = [password.length >= 8, /[A-Z]/.test(password), /[0-9]/.test(password), /[^A-Za-z0-9]/.test(password)];
  const score = checks.filter(Boolean).length;
  const cols = ['', 'bg-coral-500', 'bg-gold-500', 'bg-gold-400', 'bg-jade-500'];
  const txts = ['', 'text-coral-400', 'text-gold-500', 'text-gold-400', 'text-jade-400'];
  const lbls = ['', 'Weak', 'Fair', 'Good', 'Strong'];
  return password ? (
    <div className="space-y-1">
      <div className="flex gap-1">{[1,2,3,4].map(i => <div key={i} className={`h-1 flex-1 rounded-full transition-all ${i<=score?cols[score]:'bg-ink-800'}`}/>)}</div>
      <p className={`text-xs ${txts[score]}`}>{lbls[score]}</p>
    </div>
  ) : null;
}

export default function RegisterPage() {
  const router = useRouter();
  const [form, setForm] = useState({ name: '', email: '', password: '', confirm: '' });
  const [errors, setErrors] = useState({});
  const [serverError, setServerError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    if (localStorage.getItem('studyhub_token')) { router.replace('/dashboard'); return; }
    setReady(true);
  }, [router]);

  if (!ready) return null;

  const validate = () => {
    const e = {};
    if (!form.name.trim()) e.name = 'Name is required.';
    if (!form.email) e.email = 'Email is required.';
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) e.email = 'Please enter a valid email.';
    if (!form.password) e.password = 'Password is required.';
    else if (form.password.length < 8) e.password = 'At least 8 characters.';
    else if (!/[A-Z]/.test(form.password)) e.password = 'Include an uppercase letter.';
    else if (!/[0-9]/.test(form.password)) e.password = 'Include a number.';
    if (form.password !== form.confirm) e.confirm = 'Passwords do not match.';
    return e;
  };

  const handleSubmit = async (ev) => {
    ev.preventDefault();
    setServerError(null);
    const errs = validate();
    if (Object.keys(errs).length) { setErrors(errs); return; }
    setErrors({}); setLoading(true);
    try {
      const data = await api.register(form.email, form.password, form.name);
      saveAuth(data.access_token, data.user);
      router.push('/dashboard');
    } catch (err) {
      if (err.status === 409) setErrors({ email: 'This email is already registered.' });
      setServerError(err.message || 'Registration failed.');
    } finally { setLoading(false); }
  };

  return (
    <AuthLayout>
      <h1 className="text-2xl font-display font-bold text-ink-50 mb-1">Create your account</h1>
      <p className="text-ink-400 text-sm mb-7">
        Already have an account?{' '}
        <Link href="/auth/login" className="text-gold-400 hover:text-gold-300 font-semibold underline underline-offset-2">Sign in</Link>
      </p>

      {serverError && (
        <div className="mb-5 p-4 rounded-xl bg-coral-500/10 border border-coral-500/30 text-coral-300 text-sm">⚠ {serverError}</div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4" noValidate>
        <Input label="Full name" type="text" placeholder="Alex Johnson"
          value={form.name} onChange={e => setForm(p => ({ ...p, name: e.target.value }))} error={errors.name} autoFocus />
        <Input label="Email address" type="email" placeholder="you@university.edu"
          value={form.email} onChange={e => setForm(p => ({ ...p, email: e.target.value }))} error={errors.email} autoComplete="email" />
        <div className="space-y-1.5">
          <Input label="Password" type="password" placeholder="••••••••••"
            value={form.password} onChange={e => setForm(p => ({ ...p, password: e.target.value }))} error={errors.password} autoComplete="new-password" />
          <StrengthBar password={form.password} />
        </div>
        <Input label="Confirm password" type="password" placeholder="••••••••••"
          value={form.confirm} onChange={e => setForm(p => ({ ...p, confirm: e.target.value }))} error={errors.confirm} autoComplete="new-password" />
        <div className="pt-1">
          <Button type="submit" size="lg" className="w-full" loading={loading}>Create account</Button>
        </div>
      </form>
      <p className="text-xs text-ink-600 text-center mt-5">By registering you agree to our terms of service.</p>
    </AuthLayout>
  );
}
