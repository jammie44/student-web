/**
 * API client — all calls go through here.
 * Base URL auto-detects: /api in production (Next.js rewrite proxies to backend),
 * or NEXT_PUBLIC_API_URL/api in development.
 */
const BASE = typeof window !== 'undefined' && window.location.hostname !== 'localhost'
  ? '/api'
  : `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api`;

export class APIError extends Error {
  constructor(message, status, headers) {
    super(message);
    this.status = status;
    this.headers = headers || {};
    this.suggestReset = headers?.['x-suggest-reset'] === 'true';
    this.attemptsLeft = parseInt(headers?.['x-attempts-left'] || '0', 10);
  }
}

async function req(method, path, body) {
  const token = typeof window !== 'undefined' ? localStorage.getItem('studyhub_token') : null;
  const headers = { 'Content-Type': 'application/json' };
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const res = await fetch(`${BASE}${path}`, {
    method,
    headers,
    credentials: 'include',
    body: body ? JSON.stringify(body) : undefined,
  });

  const data = await res.json().catch(() => ({}));

  if (!res.ok) {
    const msg = data.detail || data.error || `Request failed (${res.status})`;
    throw new APIError(msg, res.status, Object.fromEntries(res.headers.entries()));
  }
  return data;
}

export const api = {
  // Auth
  register:   (email, password, name) => req('POST', '/auth/register', { email, password, name }),
  login:      (email, password)       => req('POST', '/auth/login',    { email, password }),
  logout:     ()                      => req('POST', '/auth/logout'),
  me:         ()                      => req('GET',  '/auth/me'),

  // Users
  getProfile: ()     => req('GET',   '/users/me'),
  updateProfile: (d) => req('PATCH', '/users/me', d),

  // Chats
  getChats:    ()             => req('GET',    '/chats'),
  createChat:  (tool, title)  => req('POST',   '/chats', { tool, title }),
  getMessages: (id)           => req('GET',    `/chats/${id}/messages`),
  sendMessage: (id, content)  => req('POST',   `/chats/${id}/messages`, { content }),
  deleteChat:  (id)           => req('DELETE', `/chats/${id}`),

  // Admin
  getStats:         ()                  => req('GET',   '/admin/stats'),
  getAdminUsers:    (page, search)      => req('GET',   `/admin/users?page=${page}&search=${encodeURIComponent(search||'')}`),
  toggleUser:       (id)                => req('PATCH', `/admin/users/${id}/toggle`),
  getAdminSubs:     (page)              => req('GET',   `/admin/subscriptions?page=${page}`),
};
