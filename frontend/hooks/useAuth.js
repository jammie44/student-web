'use client';
import { useState, useEffect, useCallback, createContext, useContext } from 'react';
import { useRouter } from 'next/navigation';
import { api } from '../lib/api';
import { saveAuth, clearAuth, getToken, getStoredUser } from '../lib/auth';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const stored = getStoredUser();
    const token  = getToken();
    if (token && stored) {
      setUser(stored);
      api.me()
        .then(d => setUser(d))
        .catch(() => { clearAuth(); setUser(null); })
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const login = useCallback(async (email, password) => {
    const data = await api.login(email, password);
    saveAuth(data.access_token, data.user);
    setUser(data.user);
    return data;
  }, []);

  const register = useCallback(async (email, password, name) => {
    const data = await api.register(email, password, name);
    saveAuth(data.access_token, data.user);
    setUser(data.user);
    return data;
  }, []);

  const logout = useCallback(async () => {
    try { await api.logout(); } catch {}
    clearAuth(); setUser(null);
    router.push('/auth/login');
  }, [router]);

  const updateUser = useCallback((updates) => {
    setUser(prev => {
      const u = { ...prev, ...updates };
      localStorage.setItem('studyhub_user', JSON.stringify(u));
      return u;
    });
  }, []);

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, updateUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used inside AuthProvider');
  return ctx;
}
