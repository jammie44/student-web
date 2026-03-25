const getBase = () => process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const getHeaders = () => {
  const token = typeof window !== 'undefined' ? localStorage.getItem('studyhub_token') : '';
  return {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
};

async function req(method, path, body) {
  const res = await fetch(`${getBase()}${path}`, {
    method,
    headers: getHeaders(),
    body: body ? JSON.stringify(body) : undefined,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const err = new Error(data.detail || `Error ${res.status}`);
    err.status = res.status;
    throw err;
  }
  return data;
}

export const api = {
  // Auth
  register:      (email, password, name) => req('POST', '/api/auth/register', { email, password, name }),
  login:         (email, password)       => req('POST', '/api/auth/login',    { email, password }),
  logout:        ()                      => req('POST', '/api/auth/logout'),
  me:            ()                      => req('GET',  '/api/auth/me'),

  // Users
  getProfile:    ()   => req('GET',   '/api/users/me'),
  updateProfile: (d)  => req('PATCH', '/api/users/me', d),

  // Credits
  getCredits:    ()   => req('GET', '/api/credits/balance'),

  // Chats
  getChats:      ()            => req('GET',    '/api/chats'),
  createChat:    (tool, title) => req('POST',   '/api/chats', { tool, title }),
  getMessages:   (id)          => req('GET',    `/api/chats/${id}/messages`),
  sendMessage:   (id, content) => req('POST',   `/api/chats/${id}/messages`, { content }),
  deleteChat:    (id)          => req('DELETE', `/api/chats/${id}`),

  // Admin
  getStats:         ()               => req('GET',   '/api/admin/stats'),
  getAdminUsers:    (page, search)   => req('GET',   `/api/admin/users?page=${page}&search=${encodeURIComponent(search || '')}`),
  toggleUser:       (id)             => req('PATCH', `/api/admin/users/${id}/toggle`),
  getAdminSubs:     (page)           => req('GET',   `/api/admin/subscriptions?page=${page}`),
};
