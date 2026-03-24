'use client';
import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Sidebar } from '../../components/dashboard/Sidebar';
import { ChatWindow } from '../../components/dashboard/ChatWindow';
import { WelcomeScreen } from '../../components/dashboard/WelcomeScreen';
import { Spinner } from '../../components/ui/Spinner';
import { cn } from '../../lib/utils';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

function getHeaders() {
  const token = localStorage.getItem('studyhub_token');
  return {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
}

export default function DashboardPage() {
  const router = useRouter();
  const [mounted, setMounted] = useState(false);
  const [user, setUser] = useState(null);
  const [chats, setChats] = useState([]);
  const [chatsLoading, setChatsLoading] = useState(true);
  const [activeChat, setActiveChat] = useState(null);
  const [activeTool, setActiveTool] = useState('study_assistant');
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false);

  useEffect(() => {
    setMounted(true);
    const token = localStorage.getItem('studyhub_token');
    if (!token) { router.replace('/auth/login'); return; }
    const stored = localStorage.getItem('studyhub_user');
    if (stored) { try { setUser(JSON.parse(stored)); } catch {} }

    // Verify token
    fetch(`${API_BASE}/api/auth/me`, { headers: getHeaders() })
      .then(r => r.ok ? r.json() : Promise.reject())
      .then(d => { setUser(d); localStorage.setItem('studyhub_user', JSON.stringify(d)); })
      .catch(() => { localStorage.removeItem('studyhub_token'); localStorage.removeItem('studyhub_user'); router.replace('/auth/login'); });

    // Load chats
    fetch(`${API_BASE}/api/chats`, { headers: getHeaders() })
      .then(r => r.ok ? r.json() : { chats: [] })
      .then(d => setChats(d.chats || []))
      .catch(() => {})
      .finally(() => setChatsLoading(false));
  }, [router]);

  if (!mounted) return null;

  const handleToolSelect = async (toolId) => {
    setActiveTool(toolId);
    setActiveChat(null);
    setMobileSidebarOpen(false);
    try {
      const res = await fetch(`${API_BASE}/api/chats`, {
        method: 'POST',
        headers: getHeaders(),
        body: JSON.stringify({ tool: toolId }),
      });
      const data = await res.json();
      if (res.ok) {
        setChats(prev => [data.chat, ...prev]);
        setActiveChat(data.chat);
      }
    } catch {}
  };

  const handleSelectChat = (chat) => {
    setActiveChat(chat);
    setActiveTool(chat.tool);
    setMobileSidebarOpen(false);
  };

  const handleDeleteChat = async (chatId) => {
    await fetch(`${API_BASE}/api/chats/${chatId}`, { method: 'DELETE', headers: getHeaders() });
    setChats(prev => prev.filter(c => c.id !== chatId));
    if (activeChat?.id === chatId) setActiveChat(null);
  };

  const updateChatTitle = (chatId, title) => {
    setChats(prev => prev.map(c => c.id === chatId ? { ...c, title } : c));
  };

  const handleLogout = () => {
    localStorage.removeItem('studyhub_token');
    localStorage.removeItem('studyhub_user');
    router.push('/auth/login');
  };

  return (
    <div className="h-screen flex overflow-hidden bg-ink-950">
      {mobileSidebarOpen && (
        <div className="fixed inset-0 bg-black/60 z-40 md:hidden" onClick={() => setMobileSidebarOpen(false)} />
      )}

      {/* Sidebar desktop */}
      <div className="hidden md:flex h-full flex-shrink-0">
        <Sidebar
          chats={chats} loadingChats={chatsLoading}
          activeChatId={activeChat?.id} activeTool={activeTool}
          onSelectChat={handleSelectChat} onToolSelect={handleToolSelect}
          onDeleteChat={handleDeleteChat} collapsed={!sidebarOpen}
        />
      </div>

      {/* Sidebar mobile */}
      <div className={cn('fixed left-0 top-0 h-full z-50 md:hidden transition-transform duration-300 flex-shrink-0',
        mobileSidebarOpen ? 'translate-x-0' : '-translate-x-full')}>
        <Sidebar
          chats={chats} loadingChats={chatsLoading}
          activeChatId={activeChat?.id} activeTool={activeTool}
          onSelectChat={handleSelectChat} onToolSelect={handleToolSelect}
          onDeleteChat={handleDeleteChat} collapsed={false}
        />
      </div>

      <div className="flex-1 flex flex-col min-w-0 h-full">
        <header className="flex items-center gap-3 px-4 py-3 border-b border-ink-800/60 bg-ink-950/90 backdrop-blur-sm flex-shrink-0">
          <button onClick={() => setMobileSidebarOpen(true)}
            className="md:hidden text-ink-400 hover:text-ink-200 p-2 rounded-lg hover:bg-ink-800">☰</button>
          <button onClick={() => setSidebarOpen(p => !p)}
            className="hidden md:flex text-ink-500 hover:text-ink-300 p-2 rounded-lg hover:bg-ink-800 transition-colors">
            {sidebarOpen ? '◀' : '▶'}
          </button>
          <div className="flex-1" />
          {user?.is_admin && (
            <Link href="/admin" className="hidden sm:flex items-center gap-1.5 text-xs text-ink-500 hover:text-gold-400 transition-colors px-2 py-1 rounded-lg hover:bg-gold-500/10">
              <span>⚙️</span><span>Admin</span>
            </Link>
          )}
          {user && (
            <div className="flex items-center gap-2">
              <div className="w-7 h-7 rounded-full bg-gold-500/20 border border-gold-500/30 flex items-center justify-center text-xs font-bold text-gold-400">
                {user.name?.[0]?.toUpperCase() || user.email?.[0]?.toUpperCase()}
              </div>
              <span className="hidden sm:block text-xs text-ink-400 max-w-[120px] truncate">
                {user.name || user.email}
              </span>
            </div>
          )}
          <button onClick={handleLogout}
            className="text-xs text-ink-600 hover:text-coral-400 px-2 py-1 rounded-lg hover:bg-coral-500/10 transition-all">
            Sign out
          </button>
        </header>

        <div className="flex-1 min-h-0 overflow-hidden">
          {activeChat
            ? <ChatWindow chat={activeChat} onTitleUpdate={updateChatTitle} apiBase={API_BASE} />
            : <WelcomeScreen onToolSelect={handleToolSelect} userName={user?.name} />}
        </div>
      </div>
    </div>
  );
}
