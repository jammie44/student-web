'use client';
import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Starfield } from '../../components/layout/Starfield';
import { Sidebar } from '../../components/dashboard/Sidebar';
import { ChatWindow } from '../../components/dashboard/ChatWindow';
import { WelcomeScreen } from '../../components/dashboard/WelcomeScreen';
import { Spinner } from '../../components/ui/Spinner';
import { cn } from '../../lib/utils';
import { api } from '../../lib/api';
import { clearAuth, getToken, getStoredUser } from '../../lib/auth';

export default function DashboardPage() {
  const router = useRouter();
  const [ready, setReady] = useState(false);
  const [user, setUser] = useState(null);
  const [chats, setChats] = useState([]);
  const [chatsLoading, setChatsLoading] = useState(true);
  const [activeChat, setActiveChat] = useState(null);
  const [activeTool, setActiveTool] = useState('study_assistant');
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [mobileSidebar, setMobileSidebar] = useState(false);
  const [usage, setUsage] = useState(null);

  useEffect(() => {
    if (!getToken()) { router.replace('/auth/login'); return; }
    const stored = getStoredUser();
    if (stored) setUser(stored);
    setReady(true);

    api.me()
      .then(d => { setUser(d); localStorage.setItem('sh_user', JSON.stringify(d)); })
      .catch(() => { clearAuth(); router.replace('/auth/login'); });

    api.getChats()
      .then(d => setChats(d.chats || []))
      .finally(() => setChatsLoading(false));

    api.getUsage().then(setUsage).catch(() => {});
  }, [router]);

  const refreshUsage = () => api.getUsage().then(setUsage).catch(() => {});

  if (!ready) return (
    <div className="min-h-screen flex items-center justify-center" style={{ background: '#020408' }}>
      <Spinner size="lg" />
    </div>
  );

  const handleToolSelect = async toolId => {
    setActiveTool(toolId); setActiveChat(null); setMobileSidebar(false);
    try {
      const d = await api.createChat(toolId);
      setChats(prev => [d.chat, ...prev]);
      setActiveChat(d.chat);
    } catch {}
  };

  const handleSelectChat = chat => { setActiveChat(chat); setActiveTool(chat.tool); setMobileSidebar(false); };

  const handleDeleteChat = async id => {
    await api.deleteChat(id).catch(() => {});
    setChats(prev => prev.filter(c => c.id !== id));
    if (activeChat?.id === id) setActiveChat(null);
  };

  const updateTitle = (id, title) => setChats(prev => prev.map(c => c.id === id ? { ...c, title } : c));

  const handleLogout = () => { clearAuth(); router.push('/auth/login'); };

  return (
    <div className="h-screen flex overflow-hidden" style={{ background: '#020408' }}>
      <Starfield />

      {/* Mobile overlay */}
      {mobileSidebar && (
        <div className="fixed inset-0 bg-black/70 z-40 md:hidden" onClick={() => setMobileSidebar(false)} />
      )}

      {/* Sidebar desktop */}
      <div className="hidden md:flex h-full flex-shrink-0 relative z-10">
        <Sidebar chats={chats} loadingChats={chatsLoading} activeChatId={activeChat?.id} activeTool={activeTool}
          onSelectChat={handleSelectChat} onToolSelect={handleToolSelect} onDeleteChat={handleDeleteChat}
          collapsed={!sidebarOpen} user={user} onLogout={handleLogout} usage={usage} />
      </div>

      {/* Sidebar mobile */}
      <div className={cn('fixed left-0 top-0 h-full z-50 md:hidden transition-transform duration-300', mobileSidebar ? 'translate-x-0' : '-translate-x-full')}>
        <Sidebar chats={chats} loadingChats={chatsLoading} activeChatId={activeChat?.id} activeTool={activeTool}
          onSelectChat={handleSelectChat} onToolSelect={handleToolSelect} onDeleteChat={handleDeleteChat}
          collapsed={false} user={user} onLogout={handleLogout} usage={usage} />
      </div>

      {/* Main area */}
      <div className="flex-1 flex flex-col min-w-0 h-full relative z-10">
        {/* Top bar */}
        <header className="flex items-center gap-3 px-4 py-3 border-b border-white/5 bg-black/30 backdrop-blur-md flex-shrink-0">
          <button onClick={() => setMobileSidebar(true)} className="md:hidden text-ink-400 hover:text-white p-2 rounded-lg hover:bg-white/5 transition-colors">☰</button>
          <button onClick={() => setSidebarOpen(p => !p)} className="hidden md:flex text-ink-500 hover:text-ink-200 p-2 rounded-lg hover:bg-white/5 transition-colors">
            {sidebarOpen ? '◀' : '▶'}
          </button>
          <div className="flex-1" />

          {/* Daily usage quick view */}
          {usage && (
            <div className="hidden sm:flex items-center gap-3">
              {Object.values({ study_assistant: usage.usage?.study_assistant }).map((u, i) => u && (
                <div key={i} className="flex items-center gap-1.5 text-xs text-ink-500">
                  <div className="w-20 usage-bar">
                    <div className="usage-bar-fill bg-blue-500" style={{ width: `${Math.min(100, (u.used / u.limit) * 100)}%` }} />
                  </div>
                  <span className={u.exhausted ? 'text-red-400' : ''}>{u.remaining} left</span>
                </div>
              ))}
            </div>
          )}

          {user?.is_admin && (
            <Link href="/admin" className="hidden sm:flex items-center gap-1.5 text-xs text-ink-500 hover:text-amber-400 transition-colors px-2 py-1 rounded-lg hover:bg-amber-500/10">
              ⚙️ Admin
            </Link>
          )}
          <Link href="/pricing" className="hidden sm:flex items-center gap-1.5 text-xs text-ink-500 hover:text-blue-400 transition-colors px-2 py-1 rounded-lg hover:bg-blue-500/10">
            💎 {user?.plan === 'free' ? 'Upgrade' : user?.plan}
          </Link>
          {user && (
            <div className="flex items-center gap-2">
              <div className="w-7 h-7 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-xs font-bold text-white">
                {user.name?.[0]?.toUpperCase() || user.email?.[0]?.toUpperCase()}
              </div>
              <span className="hidden sm:block text-xs text-ink-400 max-w-[120px] truncate">{user.name || user.email}</span>
            </div>
          )}
          <button onClick={handleLogout} className="text-xs text-ink-600 hover:text-red-400 px-2 py-1 rounded-lg hover:bg-red-500/10 transition-all">Sign out</button>
        </header>

        {/* Content */}
        <div className="flex-1 min-h-0 overflow-hidden">
          {activeChat
            ? <ChatWindow chat={activeChat} onTitleUpdate={updateTitle} onMessageSent={refreshUsage} />
            : <WelcomeScreen onToolSelect={handleToolSelect} userName={user?.name} usage={usage} />
          }
        </div>
      </div>
    </div>
  );
}
