'use client';
import{useState,useEffect,useRef}from'react';
import{useRouter}from'next/navigation';
import Link from'next/link';
import{Starfield}from'../../components/layout/Starfield';
import{Sidebar}from'../../components/dashboard/Sidebar';
import{ChatWindow}from'../../components/dashboard/ChatWindow';
import{WelcomeScreen}from'../../components/dashboard/WelcomeScreen';
import{Spinner}from'../../components/ui/Spinner';
import{cn}from'../../lib/utils';
import{api}from'../../lib/api';
import{clearAuth,getToken,getStoredUser,refreshExpiry}from'../../lib/auth';

export default function DashboardPage(){
  const router=useRouter();
  const[ready,setReady]=useState(false);
  const[user,setUser]=useState(null);
  const[chats,setChats]=useState([]);
  const[chatsLoading,setChatsLoading]=useState(true);
  const[activeChat,setActiveChat]=useState(null);
  const[activeTool,setActiveTool]=useState('study_assistant');
  const[sidebarOpen,setSidebarOpen]=useState(true);
  const[mobileSidebar,setMobileSidebar]=useState(false);
  const[usage,setUsage]=useState(null);
  const booted=useRef(false);

  useEffect(()=>{
    if(booted.current)return;
    booted.current=true;
    const token=getToken();
    if(!token){router.replace('/auth/login');return;}
    // Refresh 7-day expiry on every load — keeps active users logged in
    refreshExpiry();
    // Show stored user instantly (no flash)
    const stored=getStoredUser();
    if(stored)setUser(stored);
    setReady(true);
    // Validate token in background
    api.me()
      .then(d=>{setUser(d);localStorage.setItem('sh_user',JSON.stringify(d));})
      .catch(()=>{clearAuth();router.replace('/auth/login');});
    // Load full chat history
    api.getChats()
      .then(d=>setChats(d.chats||[]))
      .catch(()=>setChats([]))
      .finally(()=>setChatsLoading(false));
    // Load daily usage
    api.getUsage().then(setUsage).catch(()=>{});
  },[router]);

  const refreshUsage=()=>api.getUsage().then(setUsage).catch(()=>{});

  if(!ready)return(
    <div className="min-h-screen flex items-center justify-center" style={{background:'#020408'}}>
      <Spinner size="lg"/>
    </div>
  );

  const handleToolSelect=async toolId=>{
    setActiveTool(toolId);setActiveChat(null);setMobileSidebar(false);
    try{const d=await api.createChat(toolId);setChats(p=>[d.chat,...p]);setActiveChat(d.chat);}catch{}
  };

  const handleSelectChat=chat=>{
    setActiveChat(chat);setActiveTool(chat.tool);setMobileSidebar(false);
  };

  const handleDeleteChat=async id=>{
    try{await api.deleteChat(id);}catch{}
    setChats(p=>p.filter(c=>c.id!==id));
    if(activeChat?.id===id)setActiveChat(null);
  };

  const updateTitle=(id,title)=>setChats(p=>p.map(c=>c.id===id?{...c,title}:c));
  const handleLogout=()=>{clearAuth();router.push('/auth/login');};

  return(
    <div className="h-screen flex overflow-hidden" style={{background:'#020408'}}>
      <Starfield/>

      {mobileSidebar&&<div className="fixed inset-0 z-40 md:hidden" style={{background:'rgba(0,0,0,0.7)'}} onClick={()=>setMobileSidebar(false)}/>}

      {/* Desktop sidebar */}
      <div className="hidden md:flex h-full flex-shrink-0 relative z-10">
        <Sidebar chats={chats} loadingChats={chatsLoading} activeChatId={activeChat?.id} activeTool={activeTool}
          onSelectChat={handleSelectChat} onToolSelect={handleToolSelect} onDeleteChat={handleDeleteChat}
          collapsed={!sidebarOpen} user={user} onLogout={handleLogout} usage={usage}/>
      </div>

      {/* Mobile sidebar */}
      <div className={cn('fixed left-0 top-0 h-full z-50 md:hidden transition-transform duration-300',mobileSidebar?'translate-x-0':'-translate-x-full')}>
        <Sidebar chats={chats} loadingChats={chatsLoading} activeChatId={activeChat?.id} activeTool={activeTool}
          onSelectChat={handleSelectChat} onToolSelect={handleToolSelect} onDeleteChat={handleDeleteChat}
          collapsed={false} user={user} onLogout={handleLogout} usage={usage}/>
      </div>

      {/* Main */}
      <div className="flex-1 flex flex-col min-w-0 h-full relative z-10">
        {/* Top bar */}
        <header className="flex items-center gap-3 px-4 py-3 border-b flex-shrink-0" style={{background:'rgba(0,0,0,0.3)',backdropFilter:'blur(12px)',borderColor:'rgba(255,255,255,0.05)'}}>
          <button onClick={()=>setMobileSidebar(true)} className="md:hidden p-2 rounded-lg transition-colors" style={{color:'#64748b'}}>☰</button>
          <button onClick={()=>setSidebarOpen(p=>!p)} className="hidden md:flex p-2 rounded-lg transition-colors" style={{color:'#475569'}}>
            {sidebarOpen?'◀':'▶'}
          </button>
          <div className="flex-1"/>
          {user?.is_admin&&(
            <Link href="/admin" className="hidden sm:flex items-center gap-1.5 text-xs px-2 py-1 rounded-lg transition-all" style={{color:'#64748b'}}>⚙️ Admin</Link>
          )}
          <Link href="/pricing" className="hidden sm:flex items-center gap-1.5 text-xs px-2 py-1 rounded-lg transition-all" style={{color:'#64748b'}}>
            💎 {user?.plan==='free'?'Upgrade':user?.plan}
          </Link>
          {user&&(
            <div className="flex items-center gap-2">
              <div className="w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold text-white" style={{background:'linear-gradient(135deg,#3b82f6,#7c3aed)'}}>
                {user.name?.[0]?.toUpperCase()||user.email?.[0]?.toUpperCase()}
              </div>
              <span className="hidden sm:block text-xs max-w-[140px] truncate" style={{color:'#64748b'}}>{user.name||user.email}</span>
            </div>
          )}
          <button onClick={handleLogout} className="text-xs px-2 py-1 rounded-lg transition-all" style={{color:'#334155'}}>Sign out</button>
        </header>

        {/* Content — key prop on ChatWindow forces remount + reloads messages when switching chats */}
        <div className="flex-1 min-h-0 overflow-hidden">
          {activeChat
            ?<ChatWindow key={activeChat.id} chat={activeChat} onTitleUpdate={updateTitle} onMessageSent={refreshUsage}/>
            :<WelcomeScreen onToolSelect={handleToolSelect} userName={user?.name} usage={usage}/>
          }
        </div>
      </div>
    </div>
  );
}
