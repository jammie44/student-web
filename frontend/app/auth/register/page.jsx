'use client';
import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { AuthLayout } from '../../../components/auth/AuthLayout';
import { Input } from '../../../components/ui/Input';
import { Button } from '../../../components/ui/Button';
import { api } from '../../../lib/api';
import { saveAuth, getToken } from '../../../lib/auth';

function StrengthBar({ pw }) {
  const score = [pw.length >= 8, /[A-Z]/.test(pw), /[0-9]/.test(pw), /[^A-Za-z0-9]/.test(pw)].filter(Boolean).length;
  const colors = ['', '#ef4444', '#f59e0b', '#fbbf24', '#10b981'];
  const labels = ['', 'Weak', 'Fair', 'Good', 'Strong'];
  return pw ? (
    <div className="space-y-1">
      <div className="flex gap-1">{[1,2,3,4].map(i => (
        <div key={i} className="h-1 flex-1 rounded-full transition-all duration-300"
          style={{ background: i <= score ? colors[score] : 'rgba(255,255,255,0.08)' }} />
      ))}</div>
      <p className="text-xs" style={{ color: colors[score] || '#475569' }}>{labels[score]}</p>
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
    if (getToken()) { router.replace('/dashboard'); return; }
    setReady(true);
  }, [router]);

  if (!ready) return null;

  const validate = () => {
    const e = {};
    if (!form.name.trim()) e.name = 'Name is required.';
    if (!form.email) e.email = 'Email is required.';
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) e.email = 'Enter a valid email.';
    if (!form.password) e.password = 'Password is required.';
    else if (form.password.length < 8) e.password = 'At least 8 characters.';
    else if (!/[A-Z]/.test(form.password)) e.password = 'Include an uppercase letter.';
    else if (!/[0-9]/.test(form.password)) e.password = 'Include a number.';
    if (form.password !== form.confirm) e.confirm = 'Passwords do not match.';
    return e;
  };

  const handleSubmit = async ev => {
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
      if (err.status === 409) setErrors({ email: 'This email already has an account. Please sign in.' });
      else setServerError(err.message || 'Registration failed.');
    } finally { setLoading(false); }
  };

  return (
    <AuthLayout>
      <h1 className="text-2xl font-display font-bold text-white mb-1">Create your account</h1>
      <p className="text-ink-400 text-sm mb-7">
        Already registered?{' '}
        <Link href="/auth/login" className="text-blue-400 hover:text-blue-300 font-semibold underline underline-offset-2 transition-colors">
          Sign in
        </Link>
      </p>

      {serverError && (
        <div className="mb-5 p-4 rounded-xl bg-red-500/10 border border-red-500/25 text-red-300 text-sm">⚠ {serverError}</div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4" noValidate>
        <Input label="Full name" type="text" placeholder="Alex Johnson"
          value={form.name} onChange={e => setForm(p => ({ ...p, name: e.target.value }))}
          error={errors.name} autoFocus />
        <Input label="Email address" type="email" placeholder="you@university.edu"
          value={form.email} onChange={e => setForm(p => ({ ...p, email: e.target.value }))}
          error={errors.email} autoComplete="email" />
        <div className="space-y-1.5">
          <Input label="Password" type="password" placeholder="••••••••••"
            value={form.password} onChange={e => setForm(p => ({ ...p, password: e.target.value }))}
            error={errors.password} autoComplete="new-password" />
          <StrengthBar pw={form.password} />
        </div>
        <Input label="Confirm password" type="password" placeholder="••••••••••"
          value={form.confirm} onChange={e => setForm(p => ({ ...p, confirm: e.target.value }))}
          error={errors.confirm} autoComplete="new-password" />
        <div className="pt-1">
          <Button type="submit" size="lg" className="w-full" loading={loading}>Create free account</Button>
        </div>
      </form>
      <p className="text-xs text-ink-600 text-center mt-5">
        One account per email address · No credit card required
      </p>
    </AuthLayout>
  );
}
