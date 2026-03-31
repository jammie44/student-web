'use client';
import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Starfield } from '../../components/layout/Starfield';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { Spinner } from '../../components/ui/Spinner';
import { formatDate, cn } from '../../lib/utils';
import { api } from '../../lib/api';
import { clearAuth, getToken, getStoredUser } from '../../lib/auth';

function StatCard({ icon, label, value, color }) {
  const bg = color === 'gold' ? 'rgba(245,158,11,0.08)' : color === 'green' ? 'rgba(16,185,129,0.08)' : color === 'purple' ? 'rgba(139,92,246,0.08)' : 'rgba(255,255,255,0.04)';
  const border = color === 'gold' ? 'rgba(245,158,11,0.2)' : color === 'green' ? 'rgba(16,185,129,0.2)' : color === 'purple' ? 'rgba(139,92,246,0.2)' : 'rgba(255,255,255,0.08)';
  const text = color === 'gold' ? '#fbbf24' : color === 'green' ? '#34d399' : color === 'purple' ? '#a78bfa' : '#e2e8f0';
  return (
    <div className="p-5 rounded-2xl border" style={{ background: bg, borderColor: border }}>
      <p className="text-2xl mb-2">{icon}</p>
      <p className="text-2xl font-display font-bold mb-0.5" style={{ color }}>{value ?? '—'}</p>
      <p className="text-xs text-ink-500 font-medium">{label}</p>
    </div>
  );
}

export default function AdminPage() {
  const router = useRouter();
  const [ready, setReady] = useState(false);
  const [user, setUser] = useState(null);
  const [tab, setTab] = useState('users');
  const [stats, setStats] = useState(null);
  const [users, setUsers] = useState([]);
  const [loadingUsers, setLoadingUsers] = useState(false);
  const [userTotal, setUserTotal] = useState(0);
  const [userPage, setUserPage] = useState(1);
  const [search, setSearch] = useState('');
  const [togglingId, setTogglingId] = useState(null);
  const [changingPlanId, setChangingPlanId] = useState(null);

  useEffect(() => {
    if (!getToken()) { router.replace('/auth/login'); return; }
    const stored = getStoredUser();
    if (stored) { setUser(stored); if (!stored.is_admin) { router.replace('/dashboard'); return; } }
    setReady(true);
    api.me().then(d => { setUser(d); if (!d.is_admin) router.replace('/dashboard'); }).catch(() => { clearAuth(); router.replace('/auth/login'); });
    api.getStats().then(setStats).catch(() => {});
  }, [router]);

  const loadUsers = useCallback(() => {
    setLoadingUsers(true);
    api.getAdminUsers(userPage, search)
      .then(d => { setUsers(d.users || []); setUserTotal(d.total || 0); })
      .finally(() => setLoadingUsers(false));
  }, [userPage, search]);

  useEffect(() => { if (ready) loadUsers(); }, [ready, loadUsers]);

  const handleToggle = async id => {
    setTogglingId(id);
    try { const d = await api.toggleUser(id); setUsers(prev => prev.map(u => u.id === id ? { ...u, is_active: d.user.is_active } : u)); }
    catch (e) { alert(e.message); }
    finally { setTogglingId(null); }
  };

  const handlePlanChange = async (id, plan) => {
    setChangingPlanId(id);
    try { const d = await api.changePlan(id, plan); setUsers(prev => prev.map(u => u.id === id ? { ...u, plan: d.user.plan } : u)); }
    catch (e) { alert(e.message); }
    finally { setChangingPlanId(null); }
  };

  const handleLogout = () => { clearAuth(); router.push('/auth/login'); };

  if (!ready) return <div className="min-h-screen flex items-center justify-center" style={{ background: '#020408' }}><Spinner size="lg" /></div>;

  return (
    <div className="min-h-screen" style={{ background: '#020408' }}>
      <Starfield />
      <div className="relative z-10">
        <nav className="border-b border-white/5 px-6 py-4 flex items-center gap-4 bg-black/30 backdrop-blur-md sticky top-0 z-10">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-sm">🎓</div>
            <span className="font-display font-bold text-white">StudyHub</span>
            <span className="text-ink-600">/</span>
            <span className="text-sm text-ink-400 font-semibold">Admin</span>
          </div>
          <div className="flex-1" />
          <Link href="/dashboard"><Button variant="ghost" size="sm">← Dashboard</Button></Link>
          <button onClick={handleLogout} className="text-xs text-ink-600 hover:text-red-400 px-2 py-1 rounded hover:bg-red-500/10 transition-all">Sign out</button>
        </nav>

        <div className="max-w-6xl mx-auto px-6 py-8">
          <div className="mb-8">
            <h1 className="text-2xl font-display font-bold text-white mb-1">Admin Dashboard</h1>
            <p className="text-ink-500 text-sm">Manage users, plans, and platform stats.</p>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4 mb-8">
            <StatCard icon="👥" label="Total Users"   value={stats?.total_users}    color="blue"   />
            <StatCard icon="✅" label="Active Users"  value={stats?.active_users}   color="green"  />
            <StatCard icon="⭐" label="Pro Users"     value={stats?.pro_users}      color="gold"   />
            <StatCard icon="💬" label="Total Chats"   value={stats?.total_chats}    color=""       />
            <StatCard icon="📨" label="Messages"      value={stats?.total_messages} color="purple" />
          </div>

          {/* Users table */}
          <div>
            <div className="flex items-center gap-3 mb-4">
              <div className="relative flex-1 max-w-xs">
                <span className="absolute left-3 top-1/2 -translate-y-1/2 text-ink-500 text-sm">🔍</span>
                <input type="text" placeholder="Search by email…" value={search}
                  onChange={e => { setSearch(e.target.value); setUserPage(1); }}
                  className="w-full bg-white/5 border border-white/10 rounded-xl pl-9 pr-4 py-2.5 text-sm text-ink-200 placeholder:text-ink-600 outline-none focus:border-blue-500/40" />
              </div>
              <span className="text-xs text-ink-600">{userTotal} users total</span>
            </div>

            <div className="glass-card rounded-2xl overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-white/5">
                      {['Email', 'Name', 'Status', 'Plan', 'Chats', 'Joined', 'Actions'].map(h => (
                        <th key={h} className="text-left px-4 py-3 text-[10px] font-bold text-ink-500 uppercase tracking-widest whitespace-nowrap">{h}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {loadingUsers ? (
                      <tr><td colSpan={7} className="px-4 py-12 text-center"><Spinner className="mx-auto" /></td></tr>
                    ) : users.length === 0 ? (
                      <tr><td colSpan={7} className="px-4 py-12 text-center text-ink-600">No users found</td></tr>
                    ) : users.map((u, i) => (
                      <tr key={u.id} className={cn('border-b border-white/4 hover:bg-white/2 transition-colors', i % 2 === 0 && 'bg-white/1')}>
                        <td className="px-4 py-3 text-ink-200 font-medium max-w-[180px] truncate">{u.email}{u.is_admin && <span className="ml-1 text-[10px] text-amber-400">admin</span>}</td>
                        <td className="px-4 py-3 text-ink-400">{u.name || '—'}</td>
                        <td className="px-4 py-3"><Badge variant={u.is_active ? 'active' : 'inactive'}>{u.is_active ? 'Active' : 'Inactive'}</Badge></td>
                        <td className="px-4 py-3">
                          <select value={u.plan}
                            onChange={e => handlePlanChange(u.id, e.target.value)}
                            disabled={changingPlanId === u.id}
                            className="bg-white/5 border border-white/10 rounded-lg px-2 py-1 text-xs text-ink-200 outline-none focus:border-blue-500/40 cursor-pointer">
                            <option value="free">Free</option>
                            <option value="pro">Pro</option>
                            <option value="unlimited">Unlimited</option>
                          </select>
                        </td>
                        <td className="px-4 py-3 text-ink-500 text-center">{u.chat_count ?? 0}</td>
                        <td className="px-4 py-3 text-ink-500 text-xs whitespace-nowrap">{formatDate(u.created_at)}</td>
                        <td className="px-4 py-3">
                          <Button variant={u.is_active ? 'danger' : 'secondary'} size="sm"
                            loading={togglingId === u.id} onClick={() => handleToggle(u.id)}>
                            {u.is_active ? 'Disable' : 'Enable'}
                          </Button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              {userTotal > 20 && (
                <div className="flex items-center justify-between px-4 py-3 border-t border-white/5">
                  <span className="text-xs text-ink-600">Page {userPage} of {Math.ceil(userTotal / 20)}</span>
                  <div className="flex gap-2">
                    <Button variant="secondary" size="sm" disabled={userPage === 1} onClick={() => setUserPage(p => p - 1)}>← Prev</Button>
                    <Button variant="secondary" size="sm" disabled={userPage >= Math.ceil(userTotal / 20)} onClick={() => setUserPage(p => p + 1)}>Next →</Button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
