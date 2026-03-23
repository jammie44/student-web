'use client';
export const TOKEN_KEY = 'studyhub_token';
export const USER_KEY  = 'studyhub_user';

export const saveAuth  = (token, user) => { localStorage.setItem(TOKEN_KEY, token); localStorage.setItem(USER_KEY, JSON.stringify(user)); };
export const clearAuth = ()            => { localStorage.removeItem(TOKEN_KEY); localStorage.removeItem(USER_KEY); };
export const getToken  = ()            => (typeof window !== 'undefined' ? localStorage.getItem(TOKEN_KEY) : null);
export const getStoredUser = ()        => {
  if (typeof window === 'undefined') return null;
  try { const u = localStorage.getItem(USER_KEY); return u ? JSON.parse(u) : null; } catch { return null; }
};
