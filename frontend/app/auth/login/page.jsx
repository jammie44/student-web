'use client';
import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { AuthLayout } from '../../../components/auth/AuthLayout';
import { Input } from '../../../components/ui/Input';
import { Button } from '../../../components/ui/Button';
import { api } from '../../../lib/api';
import { saveAuth } from '../../../lib/auth';

export default function LoginPage() {
  const router = useRouter();
  const [form, setForm] = useState({ email: '', password: '' });
  const [errors, setErrors] = useState({});
  const [serverError, setServerError] = useState(null);
  const [suggestReset, setSuggestReset] = useState(false);
  const [loading, setLoading] = useState(false);
  const [failedCount, setFailedCount] = useState(0);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    if (localStorage.getItem('studyhub_token')) { router.replace('/dashboard'); return; }
    setReady(true);
  }, [router]);

  if (!ready) return null;

  const validate = () => {
    const e = {};
    if (!form.email) e.email = 'Email is required.';
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) e.email = 'Please enter a valid email address.';
    if (!form.password) e.password = 'Password is required.';
    return e;
  };

  const handleSubmit = async (ev) => {
    ev.preventDefault();
    setServerError(null); setSuggestReset(false);
    const errs = validate();
    if (Object.keys(errs).length) { setErrors(errs); return; }
    setErrors({}); setLoading(true);
    try {
      const data = await api.login(form.email, form.password);
      saveAuth(data.access_token, data.user);
      router.push('/dashboard');
    } catch (err) {
      setServerError(err.message || 'Login failed.');
      if (err.status === 401) {
        const c = failedCount + 1;
        setFailedCount(c);
        if (c >= 2) setSuggestReset(true);
      }
    } finally { setLoading(false); }
  };

  return (
    <AuthLayout>
      <h1 className="text-2xl font-display font-bold text-ink-50 mb-1">Welcome back</h1>
      <p className="text-ink-400 text-sm mb-7">
        Don't have an account?{' '}
        <Link href="/auth/register" className="text-gold-400 hover:text-gold-300 font-semibold underline underline-offset-2">Create one</Link>
      </p>

      {serverError && (
        <div className="mb-5 p-4 rounded-xl bg-coral-500/10 border border-coral-500/30 text-coral-300 text-sm">
          <p className="font-semibold">⚠ {serverError}</p>
          {suggestReset && (
            <p className="text-xs mt-2 text-coral-400/80">
              Having trouble? <Link href="/auth/register" className="underline">Create a new account</Link> or double-check your credentials.
            </p>
          )}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-5" noValidate>
        <Input label="Email address" type="email" placeholder="you@university.edu"
          value={form.email} onChange={e => setForm(p => ({ ...p, email: e.target.value }))}
          error={errors.email} autoComplete="email" autoFocus />
        <Input label="Password" type="password" placeholder="••••••••••"
          value={form.password} onChange={e => setForm(p => ({ ...p, password: e.target.value }))}
          error={errors.password} autoComplete="current-password" />
        <Button type="submit" size="lg" className="w-full" loading={loading}>Sign in to StudyHub</Button>
      </form>

      <div className="mt-6 pt-6 border-t border-ink-700/50 text-center">
        <p className="text-xs text-ink-600">Demo: <span className="text-ink-400 font-mono">demo@studyhub.com</span> / <span className="text-ink-400 font-mono">Demo1234</span></p>
      </div>
    </AuthLayout>
  );
}
