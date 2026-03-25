'use client';
import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Sidebar } from '../../components/dashboard/Sidebar';
import { ChatWindow } from '../../components/dashboard/ChatWindow';
import { WelcomeScreen } from '../../components/dashboard/WelcomeScreen';
import { Spinner } from '../../components/ui/Spinner';
import { cn } from '../../lib/utils';
import { api } from '../../lib/api';
import { clearAuth, getStoredUser, getToken } from '../../lib/auth';

export default function DashboardPage() {
  const router = useRouter();
  const [ready, setReady] = useState(false);
  const [user, setUser] = useState(null);
  const [chats, setChats] = useState([]);
  const [chatsLoading, setChatsLoading] = useState(true);
  const [activeChat, setActiveChat] = useState(null);
  const [activeTool, setActiveTool] = useState('study_assistant');
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false);
  const [credits, setCredits] = useState(null);

  useEffect(() => {
    if (!getToken()) { router.replace('/auth/login'); return; }
    const stored = getStoredUser();
    if (stored) setUser(stored);
    setReady(true);

    api.me()
      .then(d => { setUser(d); localStorage.setItem('studyhub_user', JSON.stringify(d)); })
      .catch(() => { clearAuth(); router.replace('/auth/login'); });

    api.getChats()
      .then(d => setChats(d.chats || []))
      .catch(() => {})
      .finally(() => setChatsLoading(false));

    api.getCredits()
      .then(d => setCredits(d.credits))
      .catch(() => setCredits(null));
  }, [router]);

  const refreshCredits = () => {
    api.getCredits().then(d => setCredits(d.credits)).catch(() => {});
  };

  if (!ready) return (
    <div className="min-h-screen flex items-center justify-center bg-ink-950">
      <Spinner size="lg" />
    </div>
  );

  const handleToolSelect = async (toolId) => {
    setActiveTool(toolId); setActiveChat(null); setMobileSidebarOpen(false);
    try {
      const d = await api.createChat(toolId);
      setChats(prev => [d.chat, ...prev]);
      setActiveChat(d.chat);
    } catch {}
  };

  const handleSelectChat = (chat) => {
    setActiveChat(chat); setActiveTool(chat.tool); setMobileSidebarOpen(false);
  };

  const handleDeleteChat = async (chatId) => {
    await api.deleteChat(chatId);
    setChats(prev => prev.filter(c => c.id !== chatId));
    if (activeChat?.id === chatId) setActiveChat(null);
  };

  const updateChatTitle = (chatId, title) =>
    setChats(prev => prev.map(c => c.id === chatId ? { ...c, title } : c));

  const handleLogout = () => { clearAuth(); router.push('/auth/login'); };

  return (
    <div className="h-screen flex overflow-hidden bg-ink-950">
      {mobileSidebarOpen && (
        <div className="fixed inset-0 bg-black/70 z-40 md:hidden" onClick={() => setMobileSidebarOpen(false)} />
      )}

      {/* Sidebar desktop */}
      <div className="hidden md:flex h-full flex-shrink-0">
        <Sidebar
          chats={chats} loadingChats={chatsLoading}
          activeChatId={activeChat?.id} activeTool={activeTool}
          onSelectChat={handleSelectChat} onToolSelect={handleToolSelect}
          onDeleteChat={handleDeleteChat} collapsed={!sidebarOpen}
          user={user} onLogout={handleLogout} credits={credits}
        />
      </div>

      {/* Sidebar mobile */}
      <div className={cn(
        'fixed left-0 top-0 h-full z-50 md:hidden transition-transform duration-300 flex-shrink-0',
        mobileSidebarOpen ? 'translate-x-0' : '-translate-x-full'
      )}>
        <Sidebar
          chats={chats} loadingChats={chatsLoading}
          activeChatId={activeChat?.id} activeTool={activeTool}
          onSelectChat={handleSelectChat} onToolSelect={handleToolSelect}
          onDeleteChat={handleDeleteChat} collapsed={false}
          user={user} onLogout={handleLogout} credits={credits}
        />
      </div>

      <div className="flex-1 flex flex-col min-w-0 h-full">
        {/* Top bar */}
        <header className="flex items-center gap-3 px-4 py-3 border-b border-ink-800/60 bg-ink-950/95 backdrop-blur-sm flex-shrink-0">
          <button
            onClick={() => setMobileSidebarOpen(true)}
            className="md:hidden text-ink-400 hover:text-ink-200 p-2 rounded-lg hover:bg-ink-800"
          >☰</button>
          <button
            onClick={() => setSidebarOpen(p => !p)}
            className="hidden md:flex text-ink-500 hover:text-ink-300 p-2 rounded-lg hover:bg-ink-800 transition-colors"
          >{sidebarOpen ? '◀' : '▶'}</button>

          <div className="flex-1" />

          {/* Credits pill */}
          {credits !== null && (
            <div className={cn(
              'flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold border',
              credits > 20
                ? 'bg-gold-500/10 border-gold-500/30 text-gold-400'
                : credits > 5
                  ? 'bg-amber-500/10 border-amber-500/30 text-amber-400'
                  : 'bg-coral-500/10 border-coral-500/30 text-coral-400'
            )}>
              <span>⚡</span>
              <span>{credits} credits</span>
            </div>
          )}

          {user?.is_admin && (
            <Link href="/admin" className="hidden sm:flex items-center gap-1.5 text-xs text-ink-500 hover:text-gold-400 transition-colors px-2 py-1 rounded-lg hover:bg-gold-500/10">
              <span>⚙️</span><span>Admin</span>
            </Link>
          )}

          {user && (
            <div className="flex items-center gap-2">
              <div className="w-7 h-7 rounded-full bg-gradient-to-br from-gold-400 to-gold-600 flex items-center justify-center text-xs font-bold text-ink-950">
                {user.name?.[0]?.toUpperCase() || user.email?.[0]?.toUpperCase()}
              </div>
              <span className="hidden sm:block text-xs text-ink-400 max-w-[120px] truncate">
                {user.name || user.email}
              </span>
            </div>
          )}
          <button
            onClick={handleLogout}
            className="text-xs text-ink-600 hover:text-coral-400 px-2 py-1 rounded-lg hover:bg-coral-500/10 transition-all"
          >Sign out</button>
        </header>

        <div className="flex-1 min-h-0 overflow-hidden">
          {activeChat
            ? <ChatWindow chat={activeChat} onTitleUpdate={updateChatTitle} onMessageSent={refreshCredits} />
            : <WelcomeScreen onToolSelect={handleToolSelect} userName={user?.name} credits={credits} />}
        </div>
      </div>
    </div>
  );
}
