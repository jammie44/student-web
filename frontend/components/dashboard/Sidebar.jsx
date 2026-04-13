'use client';
import{useState}from'react';
import Link from'next/link';
import{cn,TOOLS,TOOL_COLORS,formatDate}from'../../lib/utils';

export function Sidebar({chats,loadingChats,activeChatId,activeTool,onSelectChat,onToolSelect,onDeleteChat,collapsed,user,onLogout,usage}){
  const[confirm,setConfirm]=useState(null);
  const[search,setSearch]=useState('');
  const[usageOpen,setUsageOpen]=useState(true);
  const[histOpen,setHistOpen]=useState(true);
  const filtered=search?chats.filter(c=>c.title.toLowerCase().includes(search.toLowerCase())):chats;
  const grouped=Object.keys(TOOLS).reduce((a,t)=>{a[t]=filtered.filter(c=>c.tool===t);return a;},{});
  const del=async(e,id)=>{e.stopPropagation();if(confirm===id){await onDeleteChat(id);setConfirm(null);}else{setConfirm(id);setTimeout(()=>setConfirm(null),3000);}};
  const planLabel=user?.plan==='pro'?'⭐ Pro':user?.plan==='unlimited'?'♾ Unlimited':'🆓 Free';
  const planColor=user?.plan==='pro'?'#f59e0b':user?.plan==='unlimited'?'#a78bfa':'#475569';
  return(
    <aside className={cn('flex flex-col h-full glass-sidebar transition-all duration-300 overflow-hidden',collapsed?'w-0':'w-72')}>
      <div className="flex items-center gap-3 px-4 py-4 border-b flex-shrink-0" style={{borderColor:'rgba(255,255,255,0.05)'}}>
        <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-sm flex-shrink-0">🎓</div>
        <div className="flex-1 min-w-0">
          <span className="font-bold text-white text-base" style={{fontFamily:'Syne,sans-serif'}}>StudyHub</span>
          <span className="ml-2 text-xs font-semibold" style={{color:planColor}}>{planLabel}</span>
        </div>
      </div>

      {usage&&(
        <div className="px-3 py-3 border-b flex-shrink-0" style={{borderColor:'rgba(255,255,255,0.05)'}}>
          <button onClick={()=>setUsageOpen(p=>!p)} className="flex items-center justify-between w-full mb-2">
            <span className="text-[10px] font-bold uppercase tracking-widest" style={{color:'#475569'}}>Daily Usage</span>
            <span className="text-xs" style={{color:'#334155'}}>{usageOpen?'▲':'▼'}</span>
          </button>
          {usageOpen&&<div className="space-y-2.5">
            {Object.values(TOOLS).map(tool=>{
              const u=usage?.usage?.[tool.id];if(!u)return null;
              const pct=Math.min(100,(u.used/u.limit)*100);
              const col=TOOL_COLORS[tool.color];
              const bar=pct>=100?'#ef4444':pct>=80?'#f59e0b':col.text;
              return(
                <div key={tool.id}>
                  <div className="flex items-center justify-between mb-1">
                    <button onClick={()=>onToolSelect(tool.id)} className="flex items-center gap-1.5 text-xs transition-colors" style={{color:'#64748b'}}>
                      <span>{tool.icon}</span><span className="truncate max-w-[110px]">{tool.label}</span>
                    </button>
                    <span className="text-[10px] font-bold tabular-nums" style={{color:u.exhausted?'#ef4444':'#475569'}}>{u.used}/{u.limit}</span>
                  </div>
                  <div className="usage-bar"><div className="usage-bar-fill" style={{width:`${pct}%`,background:bar}}/></div>
                </div>
              );
            })}
            {usage?.plan==='free'&&<Link href="/pricing" className="block mt-2 text-center text-[10px] font-semibold rounded-lg py-1.5 transition-all" style={{color:'#60a5fa',background:'rgba(59,130,246,0.1)',border:'1px solid rgba(59,130,246,0.2)'}}>⚡ Upgrade to Pro →</Link>}
          </div>}
        </div>
      )}

      <div className="px-3 py-2.5 border-b flex-shrink-0" style={{borderColor:'rgba(255,255,255,0.05)'}}>
        <div className="relative">
          <span className="absolute left-3 top-1/2 -translate-y-1/2 text-xs" style={{color:'#475569'}}>🔍</span>
          <input type="text" placeholder="Search chats…" value={search} onChange={e=>setSearch(e.target.value)}
            className="w-full rounded-lg pl-7 pr-3 py-2 text-xs outline-none transition-colors"
            style={{background:'rgba(255,255,255,0.05)',border:'1px solid rgba(255,255,255,0.08)',color:'#cbd5e1'}}/>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto min-h-0">
        <div className="px-3 py-2">
          <button onClick={()=>setHistOpen(p=>!p)} className="flex items-center justify-between w-full mb-2">
            <span className="text-[10px] font-bold uppercase tracking-widest" style={{color:'#475569'}}>Chat History</span>
            <span className="text-xs" style={{color:'#334155'}}>{histOpen?'▲':'▼'}</span>
          </button>
          {histOpen&&(loadingChats?<div className="space-y-2">{[1,2,3].map(i=><div key={i} className="h-11 rounded-xl skeleton"/>)}</div>:
            filtered.length===0?<div className="text-center py-8"><p className="text-2xl mb-2">💬</p><p className="text-xs" style={{color:'#334155'}}>{search?'No chats match':'No chats yet'}</p></div>:
            search?filtered.map(c=><CI key={c.id} chat={c} active={activeChatId===c.id} onSelect={onSelectChat} onDel={del} confirm={confirm}/>):
            Object.entries(grouped).map(([tid,tChats])=>{
              if(!tChats.length)return null;
              const tool=TOOLS[tid];const col=TOOL_COLORS[tool.color];
              return(
                <div key={tid} className="mb-4">
                  <div className="flex items-center gap-1.5 px-2 mb-1.5">
                    <span className="text-xs">{tool.icon}</span>
                    <span className="text-[10px] font-bold uppercase tracking-widest" style={{color:col.text}}>{tool.label}</span>
                  </div>
                  {tChats.map(c=><CI key={c.id} chat={c} active={activeChatId===c.id} onSelect={onSelectChat} onDel={del} confirm={confirm}/>)}
                </div>
              );
            })
          )}
        </div>
      </div>

      <div className="px-3 py-3 border-t flex-shrink-0 space-y-1" style={{borderColor:'rgba(255,255,255,0.05)'}}>
        {user?.is_admin&&<Link href="/admin" className="flex items-center gap-2 px-3 py-2 rounded-xl text-xs font-semibold transition-all" style={{color:'#64748b'}}>⚙️ Admin Dashboard</Link>}
        <Link href="/pricing" className="flex items-center gap-2 px-3 py-2 rounded-xl text-xs font-semibold transition-all" style={{color:'#64748b'}}>💎 Plans & Pricing</Link>
        <div className="flex items-center gap-3 px-3 py-2.5 rounded-xl mt-1" style={{background:'rgba(255,255,255,0.03)',border:'1px solid rgba(255,255,255,0.05)'}}>
          <div className="w-7 h-7 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-xs font-bold text-white flex-shrink-0">
            {user?.name?.[0]?.toUpperCase()||user?.email?.[0]?.toUpperCase()||'?'}
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-xs font-semibold text-white truncate">{user?.name||'Student'}</p>
            <p className="text-[10px] truncate" style={{color:'#475569'}}>{user?.email}</p>
          </div>
          <button onClick={onLogout} className="p-1 text-sm transition-colors" style={{color:'#334155'}}>⇥</button>
        </div>
      </div>
    </aside>
  );
}

function CI({chat,active,onSelect,onDel,confirm}){
  const tool=TOOLS[chat.tool];const col=TOOL_COLORS[tool?.color||'blue'];
  return(
    <div onClick={()=>onSelect(chat)}
      className="group relative flex items-start gap-2 px-3 py-2.5 rounded-xl cursor-pointer transition-all mb-0.5"
      style={active?{background:col.bg,border:`1px solid ${col.border}`}:{border:'1px solid transparent'}}>
      <span className="text-sm mt-0.5 flex-shrink-0">{tool?.icon||'💬'}</span>
      <div className="flex-1 min-w-0">
        <p className="text-xs font-medium truncate" style={{color:active?'#fff':'#94a3b8'}}>{chat.title}</p>
        <p className="text-[10px] mt-0.5" style={{color:'#334155'}}>{formatDate(chat.updated_at)}</p>
      </div>
      <button onClick={e=>onDel(e,chat.id)}
        className="flex-shrink-0 w-5 h-5 flex items-center justify-center rounded text-[10px] opacity-0 group-hover:opacity-100 transition-all"
        style={confirm===chat.id?{opacity:1,background:'rgba(239,68,68,0.2)',color:'#f87171'}:{color:'#334155'}}>
        {confirm===chat.id?'✕':'×'}
      </button>
    </div>
  );
}
