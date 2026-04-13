'use client';
import{useState,useEffect,useCallback}from'react';
import{useRouter}from'next/navigation';
import Link from'next/link';
import{Starfield}from'../../components/layout/Starfield';
import{Badge}from'../../components/ui/Badge';
import{Button}from'../../components/ui/Button';
import{Spinner}from'../../components/ui/Spinner';
import{cn,formatDate}from'../../lib/utils';
import{api}from'../../lib/api';
import{clearAuth,getToken,getStoredUser}from'../../lib/auth';

function StatCard({icon,label,value,textColor}){
  return(
    <div className="p-5 rounded-2xl" style={{background:'rgba(255,255,255,0.03)',border:'1px solid rgba(255,255,255,0.08)'}}>
      <p className="text-2xl mb-2">{icon}</p>
      <p className="text-2xl font-bold mb-0.5" style={{fontFamily:'Syne,sans-serif',color:textColor||'#e2e8f0'}}>{value??'—'}</p>
      <p className="text-xs font-medium" style={{color:'#475569'}}>{label}</p>
    </div>
  );
}

export default function AdminPage(){
  const router=useRouter();
  const[ready,setReady]=useState(false);
  const[user,setUser]=useState(null);
  const[stats,setStats]=useState(null);
  const[users,setUsers]=useState([]);
  const[loadingUsers,setLoadingUsers]=useState(false);
  const[total,setTotal]=useState(0);
  const[page,setPage]=useState(1);
  const[search,setSearch]=useState('');
  const[togglingId,setTogglingId]=useState(null);
  const[planId,setPlanId]=useState(null);

  useEffect(()=>{
    if(!getToken()){router.replace('/auth/login');return;}
    const stored=getStoredUser();
    if(stored){setUser(stored);if(!stored.is_admin){router.replace('/dashboard');return;}}
    setReady(true);
    api.me().then(d=>{setUser(d);if(!d.is_admin)router.replace('/dashboard');}).catch(()=>{clearAuth();router.replace('/auth/login');});
    api.getStats().then(setStats).catch(()=>{});
  },[router]);

  const loadUsers=useCallback(()=>{
    setLoadingUsers(true);
    api.getAdminUsers(page,search)
      .then(d=>{setUsers(d.users||[]);setTotal(d.total||0);})
      .catch(()=>{})
      .finally(()=>setLoadingUsers(false));
  },[page,search]);

  useEffect(()=>{if(ready)loadUsers();},[ready,loadUsers]);

  const handleToggle=async id=>{
    setTogglingId(id);
    try{const d=await api.toggleUser(id);setUsers(p=>p.map(u=>u.id===id?{...u,is_active:d.user.is_active}:u));}
    catch(e){alert(e.message);}finally{setTogglingId(null);}
  };

  const handlePlan=async(id,plan)=>{
    setPlanId(id);
    try{const d=await api.changePlan(id,plan);setUsers(p=>p.map(u=>u.id===id?{...u,plan:d.user.plan}:u));}
    catch(e){alert(e.message);}finally{setPlanId(null);}
  };

  const handleLogout=()=>{clearAuth();router.push('/auth/login');};
  const totalPages=Math.ceil(total/20);

  if(!ready)return(<div className="min-h-screen flex items-center justify-center" style={{background:'#020408'}}><Spinner size="lg"/></div>);

  return(
    <div className="min-h-screen" style={{background:'#020408'}}>
      <Starfield/>
      <div className="relative z-10">
        <nav className="border-b px-6 py-4 flex items-center gap-4 sticky top-0 z-10" style={{background:'rgba(0,0,0,0.3)',backdropFilter:'blur(12px)',borderColor:'rgba(255,255,255,0.05)'}}>
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-xl flex items-center justify-center text-sm" style={{background:'linear-gradient(135deg,#3b82f6,#7c3aed)'}}>🎓</div>
            <span className="font-bold text-white" style={{fontFamily:'Syne,sans-serif'}}>StudyHub</span>
            <span style={{color:'#334155'}}>/</span>
            <span className="text-sm font-semibold" style={{color:'#64748b'}}>Admin</span>
          </div>
          <div className="flex-1"/>
          <Link href="/dashboard"><Button variant="ghost" size="sm">← Dashboard</Button></Link>
          <button onClick={handleLogout} className="text-xs px-2 py-1 rounded transition-all" style={{color:'#334155'}}>Sign out</button>
        </nav>

        <div className="max-w-6xl mx-auto px-6 py-8">
          <div className="mb-8">
            <h1 className="text-2xl font-bold text-white mb-1" style={{fontFamily:'Syne,sans-serif'}}>Admin Dashboard</h1>
            <p className="text-sm" style={{color:'#475569'}}>Manage users, plans, and platform stats.</p>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4 mb-10">
            <StatCard icon="👥" label="Total Users"   value={stats?.total_users}    textColor="#60a5fa"/>
            <StatCard icon="✅" label="Active Users"  value={stats?.active_users}   textColor="#34d399"/>
            <StatCard icon="⭐" label="Pro Users"     value={stats?.pro_users}      textColor="#fbbf24"/>
            <StatCard icon="💬" label="Total Chats"   value={stats?.total_chats}    textColor="#e2e8f0"/>
            <StatCard icon="📨" label="Messages Sent" value={stats?.total_messages} textColor="#a78bfa"/>
          </div>

          <div>
            <div className="flex flex-col sm:flex-row items-start sm:items-center gap-3 mb-4">
              <div className="relative flex-1 max-w-xs">
                <span className="absolute left-3 top-1/2 -translate-y-1/2 text-sm" style={{color:'#475569'}}>🔍</span>
                <input type="text" placeholder="Search by email…" value={search}
                  onChange={e=>{setSearch(e.target.value);setPage(1);}}
                  className="w-full rounded-xl pl-9 pr-4 py-2.5 text-sm outline-none"
                  style={{background:'rgba(255,255,255,0.05)',border:'1px solid rgba(255,255,255,0.1)',color:'#e2e8f0'}}/>
              </div>
              <span className="text-xs" style={{color:'#334155'}}>{total} users total</span>
              <Button variant="secondary" size="sm" onClick={loadUsers}>↺ Refresh</Button>
            </div>

            <div className="glass-card rounded-2xl overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b" style={{borderColor:'rgba(255,255,255,0.05)'}}>
                      {['Email','Name','Status','Plan','Chats','Joined','Actions'].map(h=>(
                        <th key={h} className="text-left px-4 py-3 whitespace-nowrap" style={{fontSize:'10px',fontWeight:700,color:'#475569',textTransform:'uppercase',letterSpacing:'0.1em'}}>{h}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {loadingUsers?(<tr><td colSpan={7} className="px-4 py-12 text-center"><Spinner className="mx-auto"/></td></tr>):
                    users.length===0?(<tr><td colSpan={7} className="px-4 py-12 text-center" style={{color:'#334155'}}>No users found</td></tr>):
                    users.map((u,i)=>(
                      <tr key={u.id} className="border-b transition-colors" style={{borderColor:'rgba(255,255,255,0.04)',background:i%2===0?'rgba(255,255,255,0.01)':'transparent'}}>
                        <td className="px-4 py-3 max-w-[180px]">
                          <span className="font-medium truncate block" style={{color:'#e2e8f0'}}>{u.email}</span>
                          {u.is_admin&&<span className="text-[10px] font-semibold" style={{color:'#fbbf24'}}>admin</span>}
                        </td>
                        <td className="px-4 py-3 max-w-[120px] truncate" style={{color:'#94a3b8'}}>{u.name||'—'}</td>
                        <td className="px-4 py-3"><Badge variant={u.is_active?'active':'inactive'}>{u.is_active?'Active':'Inactive'}</Badge></td>
                        <td className="px-4 py-3">
                          <select value={u.plan} onChange={e=>handlePlan(u.id,e.target.value)} disabled={planId===u.id}
                            className="rounded-lg px-2 py-1 text-xs outline-none cursor-pointer disabled:opacity-50"
                            style={{background:'rgba(255,255,255,0.05)',border:'1px solid rgba(255,255,255,0.1)',color:'#e2e8f0'}}>
                            <option value="free">Free</option>
                            <option value="pro">Pro</option>
                            <option value="unlimited">Unlimited</option>
                          </select>
                        </td>
                        <td className="px-4 py-3 text-center" style={{color:'#475569'}}>{u.chat_count??0}</td>
                        <td className="px-4 py-3 whitespace-nowrap text-xs" style={{color:'#475569'}}>{formatDate(u.created_at)}</td>
                        <td className="px-4 py-3">
                          <Button variant={u.is_active?'danger':'secondary'} size="sm" loading={togglingId===u.id} onClick={()=>handleToggle(u.id)}>
                            {u.is_active?'Disable':'Enable'}
                          </Button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              {totalPages>1&&(
                <div className="flex items-center justify-between px-4 py-3 border-t" style={{borderColor:'rgba(255,255,255,0.05)'}}>
                  <span className="text-xs" style={{color:'#334155'}}>Page {page} of {totalPages}</span>
                  <div className="flex gap-2">
                    <Button variant="secondary" size="sm" disabled={page===1} onClick={()=>setPage(p=>p-1)}>← Prev</Button>
                    <Button variant="secondary" size="sm" disabled={page>=totalPages} onClick={()=>setPage(p=>p+1)}>Next →</Button>
                  </div>
                </div>
              )}
            </div>

            <div className="mt-8 glass-card rounded-xl p-5">
              <h3 className="text-sm font-semibold text-white mb-3">⚙️ Quick Reference</h3>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs" style={{color:'#64748b'}}>
                <div>
                  <p className="font-semibold mb-1" style={{color:'#e2e8f0'}}>Make yourself admin (SQL)</p>
                  <code className="block font-mono px-2 py-1 rounded text-xs" style={{background:'rgba(0,0,0,0.3)',color:'#93c5fd'}}>
                    UPDATE users SET is_admin = true<br/>WHERE email = 'you@email.com';
                  </code>
                </div>
                <div>
                  <p className="font-semibold mb-1" style={{color:'#e2e8f0'}}>Demo credentials</p>
                  <p>Admin: admin@studyhub.com / Admin123</p>
                  <p>User: demo@studyhub.com / Demo1234</p>
                </div>
                <div>
                  <p className="font-semibold mb-1" style={{color:'#e2e8f0'}}>Daily limits</p>
                  <p>Free: 10/5/3/5/5 per tool</p>
                  <p>Pro: 50/30/15/30/30</p>
                  <p>Unlimited: ∞ on everything</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
