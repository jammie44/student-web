'use client';
import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { api } from '../../lib/api';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { Spinner } from '../../components/ui/Spinner';
import { formatDate, cn } from '../../lib/utils';
import { getToken, getStoredUser, clearAuth } from '../../lib/auth';

function StatCard({ icon, label, value, color }) {
  const colorCls = color==='gold'?'bg-gold-500/5 border-gold-500/15':color==='jade'?'bg-jade-500/5 border-jade-500/15':color==='coral'?'bg-coral-500/5 border-coral-500/15':'bg-ink-900/60 border-ink-800';
  const valCls = color==='gold'?'text-gold-400':color==='jade'?'text-jade-400':color==='coral'?'text-coral-400':'text-ink-100';
  return (
    <div className={cn('p-5 rounded-2xl border animate-fade-up', colorCls)}>
      <p className="text-2xl mb-2">{icon}</p>
      <p className={cn('text-2xl font-display font-bold mb-0.5', valCls)}>{value ?? '—'}</p>
      <p className="text-xs text-ink-500 font-medium">{label}</p>
    </div>
  );
}

export default function AdminPage() {
  const router = useRouter();
  const [user, setUser] = useState(null);
  const [tab, setTab] = useState('users');
  const [stats, setStats] = useState(null);
  const [users, setUsers] = useState([]);
  const [subs, setSubs] = useState([]);
  const [loadingUsers, setLoadingUsers] = useState(false);
  const [loadingSubs, setLoadingSubs] = useState(false);
  const [userPage, setUserPage] = useState(1);
  const [subPage, setSubPage] = useState(1);
  const [userTotal, setUserTotal] = useState(0);
  const [subTotal, setSubTotal] = useState(0);
  const [search, setSearch] = useState('');
  const [togglingId, setTogglingId] = useState(null);

  useEffect(() => {
    const token = getToken();
    if (!token) { router.replace('/auth/login'); return; }
    const stored = getStoredUser();
    if (stored) {
      setUser(stored);
      if (!stored.is_admin) { router.replace('/dashboard'); return; }
    }
    api.me()
      .then(d => { setUser(d); if (!d.is_admin) router.replace('/dashboard'); })
      .catch(() => { clearAuth(); router.replace('/auth/login'); });
  }, [router]);

  useEffect(() => {
    if (!user?.is_admin) return;
    api.getStats().then(setStats).catch(console.error);
  }, [user]);

  const loadUsers = useCallback(async () => {
    if (!user?.is_admin) return;
    setLoadingUsers(true);
    try {
      const d = await api.getAdminUsers(userPage, search);
      setUsers(d.users||[]); setUserTotal(d.total||0);
    } catch {}
    finally { setLoadingUsers(false); }
  }, [user, userPage, search]);

  const loadSubs = useCallback(async () => {
    if (!user?.is_admin) return;
    setLoadingSubs(true);
    try {
      const d = await api.getAdminSubs(subPage);
      setSubs(d.subscriptions||[]); setSubTotal(d.total||0);
    } catch {}
    finally { setLoadingSubs(false); }
  }, [user, subPage]);

  useEffect(() => { if (tab==='users') loadUsers(); }, [tab, loadUsers]);
  useEffect(() => { if (tab==='subs')  loadSubs();  }, [tab, loadSubs]);

  const handleToggle = async (userId) => {
    setTogglingId(userId);
    try {
      const d = await api.toggleUser(userId);
      setUsers(prev => prev.map(u => u.id===userId?{...u,is_active:d.user.is_active}:u));
    } catch (err) { alert(err.message); }
    finally { setTogglingId(null); }
  };

  const handleLogout = () => { clearAuth(); router.push('/auth/login'); };

  if (!user) return <div className="min-h-screen flex items-center justify-center bg-ink-950"><Spinner size="lg"/></div>;

  return (
    <div className="min-h-screen bg-ink-950 text-ink-100">
      {/* Nav */}
      <nav className="border-b border-ink-800/60 px-6 py-4 flex items-center gap-4 bg-ink-950/90 backdrop-blur-sm sticky top-0 z-10">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-xl bg-gold-500 flex items-center justify-center text-sm">🎓</div>
          <span className="font-display font-bold text-ink-50">StudyHub</span>
          <span className="text-ink-700">/</span>
          <span className="text-sm text-ink-400 font-semibold">Admin</span>
        </div>
        <div className="flex-1"/>
        <Link href="/dashboard"><Button variant="ghost" size="sm">← Dashboard</Button></Link>
        <button onClick={handleLogout} className="text-xs text-ink-600 hover:text-coral-400 px-2 py-1 rounded hover:bg-coral-500/10 transition-all">Sign out</button>
      </nav>

      <div className="max-w-6xl mx-auto px-6 py-8">
        <div className="mb-8 animate-fade-up">
          <h1 className="text-2xl font-display font-bold text-ink-50 mb-1">Admin Dashboard</h1>
          <p className="text-ink-500 text-sm">Manage users, subscriptions, and platform metrics.</p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4 mb-8">
          <StatCard icon="👥" label="Total Users"    value={stats?.total_users}    color="gold"/>
          <StatCard icon="✅" label="Active Users"   value={stats?.active_users}   color="jade"/>
          <StatCard icon="💳" label="Subscriptions"  value={stats?.total_subs}     color="gold"/>
          <StatCard icon="💬" label="Total Chats"    value={stats?.total_chats}    color=""/>
          <StatCard icon="📨" label="Messages Sent"  value={stats?.total_messages} color=""/>
        </div>

        {/* Tabs */}
        <div className="flex gap-1 p-1 bg-ink-900/60 rounded-xl border border-ink-800 w-fit mb-6">
          {[['users','👥 Users'],['subs','💳 Subscriptions']].map(([id,label])=>(
            <button key={id} onClick={()=>setTab(id)}
              className={cn('px-5 py-2.5 rounded-lg text-sm font-semibold transition-all',
                tab===id?'bg-gold-500 text-ink-950 shadow':'text-ink-400 hover:text-ink-200')}>
              {label}
            </button>
          ))}
        </div>

        {/* Users tab */}
        {tab==='users' && (
          <div className="animate-fade-in">
            <div className="flex items-center gap-3 mb-4">
              <div className="relative flex-1 max-w-xs">
                <span className="absolute left-3 top-1/2 -translate-y-1/2 text-ink-600 text-sm">🔍</span>
                <input type="text" placeholder="Search by email…" value={search}
                  onChange={e=>{ setSearch(e.target.value); setUserPage(1); }}
                  className="w-full bg-ink-900/80 border border-ink-700 rounded-xl pl-9 pr-4 py-2.5 text-sm text-ink-200 placeholder:text-ink-600 outline-none focus:border-gold-500/50"/>
              </div>
              <span className="text-xs text-ink-600">{userTotal} users</span>
            </div>

            <div className="bg-ink-900/40 border border-ink-800 rounded-2xl overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-ink-800">
                      {['ID','Email','Name','Status','Role','Chats','Plan','Joined','Actions'].map(h=>(
                        <th key={h} className="text-left px-4 py-3 text-[10px] font-bold text-ink-500 uppercase tracking-widest whitespace-nowrap">{h}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {loadingUsers ? (
                      <tr><td colSpan={9} className="px-4 py-12 text-center"><Spinner className="mx-auto"/></td></tr>
                    ) : users.length===0 ? (
                      <tr><td colSpan={9} className="px-4 py-12 text-center text-ink-600 text-sm">No users found</td></tr>
                    ) : users.map((u,i)=>(
                      <tr key={u.id} className={cn('border-b border-ink-800/40 transition-colors hover:bg-ink-800/30',i%2===0&&'bg-ink-900/20')}>
                        <td className="px-4 py-3 font-mono text-[10px] text-ink-600">{u.id.slice(0,8)}…</td>
                        <td className="px-4 py-3 text-ink-200 font-medium max-w-[180px] truncate">{u.email}</td>
                        <td className="px-4 py-3 text-ink-400">{u.name||'—'}</td>
                        <td className="px-4 py-3"><Badge variant={u.is_active?'active':'inactive'}>{u.is_active?'Active':'Inactive'}</Badge></td>
                        <td className="px-4 py-3"><Badge variant={u.is_admin?'gold':'neutral'}>{u.is_admin?'Admin':'User'}</Badge></td>
                        <td className="px-4 py-3 text-ink-500 text-center">{u.chat_count??0}</td>
                        <td className="px-4 py-3"><Badge variant={u.plan==='pro'?'jade':'neutral'}>{u.plan||'free'}</Badge></td>
                        <td className="px-4 py-3 text-ink-500 text-xs whitespace-nowrap">{formatDate(u.created_at)}</td>
                        <td className="px-4 py-3">
                          <Button variant={u.is_active?'danger':'secondary'} size="sm"
                            loading={togglingId===u.id} onClick={()=>handleToggle(u.id)}>
                            {u.is_active?'Disable':'Enable'}
                          </Button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              {userTotal>20&&(
                <div className="flex items-center justify-between px-4 py-3 border-t border-ink-800">
                  <span className="text-xs text-ink-600">Page {userPage} of {Math.ceil(userTotal/20)}</span>
                  <div className="flex gap-2">
                    <Button variant="secondary" size="sm" disabled={userPage===1} onClick={()=>setUserPage(p=>p-1)}>← Prev</Button>
                    <Button variant="secondary" size="sm" disabled={userPage>=Math.ceil(userTotal/20)} onClick={()=>setUserPage(p=>p+1)}>Next →</Button>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Subscriptions tab */}
        {tab==='subs' && (
          <div className="animate-fade-in">
            <div className="flex items-center justify-end mb-4">
              <span className="text-xs text-ink-600">{subTotal} subscriptions</span>
            </div>
            <div className="bg-ink-900/40 border border-ink-800 rounded-2xl overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-ink-800">
                      {['ID','User Email','Plan','Status','Stripe Customer ID','Created'].map(h=>(
                        <th key={h} className="text-left px-4 py-3 text-[10px] font-bold text-ink-500 uppercase tracking-widest whitespace-nowrap">{h}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {loadingSubs ? (
                      <tr><td colSpan={6} className="px-4 py-12 text-center"><Spinner className="mx-auto"/></td></tr>
                    ) : subs.length===0 ? (
                      <tr><td colSpan={6} className="px-4 py-12 text-center text-ink-600 text-sm">No subscriptions found</td></tr>
                    ) : subs.map((s,i)=>(
                      <tr key={s.id} className={cn('border-b border-ink-800/40 hover:bg-ink-800/30 transition-colors',i%2===0&&'bg-ink-900/20')}>
                        <td className="px-4 py-3 font-mono text-[10px] text-ink-600">{s.id.slice(0,8)}…</td>
                        <td className="px-4 py-3 text-ink-200 max-w-[200px] truncate">{s.user_email||'—'}</td>
                        <td className="px-4 py-3"><Badge variant={s.plan==='pro'?'jade':'neutral'}>{s.plan}</Badge></td>
                        <td className="px-4 py-3"><Badge variant={s.status==='active'?'active':'inactive'}>{s.status}</Badge></td>
                        <td className="px-4 py-3 font-mono text-[10px] text-ink-600">{s.stripe_customer_id||'—'}</td>
                        <td className="px-4 py-3 text-ink-500 text-xs whitespace-nowrap">{formatDate(s.created_at)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              {subTotal>20&&(
                <div className="flex items-center justify-between px-4 py-3 border-t border-ink-800">
                  <span className="text-xs text-ink-600">Page {subPage} of {Math.ceil(subTotal/20)}</span>
                  <div className="flex gap-2">
                    <Button variant="secondary" size="sm" disabled={subPage===1} onClick={()=>setSubPage(p=>p-1)}>← Prev</Button>
                    <Button variant="secondary" size="sm" disabled={subPage>=Math.ceil(subTotal/20)} onClick={()=>setSubPage(p=>p+1)}>Next →</Button>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
