const BASE = () => process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const headers = () => {
  const t = typeof window !== 'undefined' ? localStorage.getItem('sh_token') : '';
  return { 'Content-Type': 'application/json', ...(t ? { Authorization: `Bearer ${t}` } : {}) };
};

async function req(method, path, body) {
  const res = await fetch(`${BASE()}${path}`, {
    method, headers: headers(),
    body: body ? JSON.stringify(body) : undefined,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) { const e = new Error(data.detail || `Error ${res.status}`); e.status = res.status; throw e; }
  return data;
}

export const api = {
  register:      (email, password, name) => req('POST', '/api/auth/register', { email, password, name }),
  login:         (email, password)       => req('POST', '/api/auth/login',    { email, password }),
  me:            ()                      => req('GET',  '/api/auth/me'),
  getUsage:      ()                      => req('GET',  '/api/usage/today'),
  getChats:      ()                      => req('GET',  '/api/chats'),
  createChat:    (tool, title)           => req('POST', '/api/chats', { tool, title }),
  getMessages:   (id)                    => req('GET',  `/api/chats/${id}/messages`),
  sendMessage:   (id, content)           => req('POST', `/api/chats/${id}/messages`, { content }),
  deleteChat:    (id)                    => req('DELETE', `/api/chats/${id}`),
  getStats:      ()                      => req('GET',  '/api/admin/stats'),
  getAdminUsers: (page, search)          => req('GET',  `/api/admin/users?page=${page}&search=${encodeURIComponent(search || '')}`),
  toggleUser:    (id)                    => req('PATCH', `/api/admin/users/${id}/toggle`),
  changePlan:    (id, plan)              => req('PATCH', `/api/admin/users/${id}/plan`, { plan }),
};
