'use client';
import { useState } from 'react';
import Link from 'next/link';
import { cn, TOOLS, formatDate } from '../../lib/utils';

export function Sidebar({ chats, loadingChats, activeChatId, activeTool, onSelectChat, onToolSelect, onDeleteChat, collapsed }) {
  const [deleteConfirm, setDeleteConfirm] = useState(null);
  const [search, setSearch] = useState('');

  const grouped = Object.keys(TOOLS).reduce((acc, t) => { acc[t] = chats.filter(c => c.tool === t); return acc; }, {});
  const filtered = search ? chats.filter(c => c.title.toLowerCase().includes(search.toLowerCase())) : null;

  const handleDelete = async (e, id) => {
    e.stopPropagation();
    if (deleteConfirm === id) { await onDeleteChat(id); setDeleteConfirm(null); }
    else { setDeleteConfirm(id); setTimeout(() => setDeleteConfirm(null), 3000); }
  };

  return (
    <aside className={cn('flex flex-col h-full bg-ink-950 border-r border-ink-800/80 transition-all duration-300', collapsed ? 'w-0 overflow-hidden' : 'w-72')}>
      {/* Logo */}
      <div className="flex items-center gap-3 px-4 py-4 border-b border-ink-800/50">
        <div className="w-8 h-8 rounded-xl bg-gold-500 flex items-center justify-center text-sm shadow-lg shadow-gold-500/30 flex-shrink-0">🎓</div>
        <span className="font-display font-bold text-ink-50 text-lg tracking-tight">StudyHub</span>
      </div>

      {/* Tools */}
      <div className="px-3 py-3 border-b border-ink-800/50">
        <p className="text-[10px] font-bold text-ink-600 uppercase tracking-widest px-2 mb-2">Tools</p>
        {Object.values(TOOLS).map(tool => (
          <button key={tool.id} onClick={() => onToolSelect(tool.id)}
            className={cn('w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-left transition-all duration-150 group mb-0.5',
              activeTool===tool.id && !activeChatId ? 'bg-gold-500/10 border border-gold-500/20 text-gold-300' : 'text-ink-400 hover:text-ink-200 hover:bg-ink-800/60')}>
            <span className="text-base">{tool.icon}</span>
            <span className="text-xs font-semibold flex-1">{tool.label}</span>
            <span className="text-[10px] font-bold px-1.5 py-0.5 rounded-md opacity-0 group-hover:opacity-100 bg-ink-800 text-ink-400">New</span>
          </button>
        ))}
      </div>

      {/* Chat history */}
      <div className="flex-1 overflow-y-auto min-h-0">
        <div className="px-3 py-3">
          <div className="relative mb-3">
            <span className="absolute left-3 top-1/2 -translate-y-1/2 text-ink-600 text-xs">🔍</span>
            <input type="text" placeholder="Search chats…" value={search} onChange={e=>setSearch(e.target.value)}
              className="w-full bg-ink-900/60 border border-ink-800 rounded-lg pl-7 pr-3 py-2 text-xs text-ink-300 placeholder:text-ink-600 outline-none focus:border-gold-500/50"/>
          </div>

          {loadingChats ? (
            <div className="space-y-2">{[1,2,3].map(i=><div key={i} className="h-12 rounded-xl skeleton"/>)}</div>
          ) : filtered ? (
            filtered.length === 0
              ? <p className="text-xs text-ink-600 text-center py-4">No chats found</p>
              : filtered.map(c => <ChatItem key={c.id} chat={c} activeChatId={activeChatId} onSelect={onSelectChat} onDelete={handleDelete} confirm={deleteConfirm}/>)
          ) : (
            Object.entries(grouped).map(([tid, tChats]) => {
              if (!tChats.length) return null;
              const tool = TOOLS[tid];
              return (
                <div key={tid} className="mb-4">
                  <p className="text-[10px] font-bold text-ink-600 uppercase tracking-widest px-2 mb-1.5 flex items-center gap-1.5">
                    <span>{tool.icon}</span>{tool.label}
                  </p>
                  <div className="space-y-0.5">
                    {tChats.map(c => <ChatItem key={c.id} chat={c} activeChatId={activeChatId} onSelect={onSelectChat} onDelete={handleDelete} confirm={deleteConfirm}/>)}
                  </div>
                </div>
              );
            })
          )}

          {!loadingChats && chats.length === 0 && (
            <div className="text-center py-8">
              <p className="text-3xl mb-2">💬</p>
              <p className="text-xs text-ink-600">No chats yet.<br/>Select a tool to start!</p>
            </div>
          )}
        </div>
      </div>

      {/* User footer — imported via prop */}
      <div id="sidebar-footer" className="px-3 py-3 border-t border-ink-800/50"/>
    </aside>
  );
}

function ChatItem({ chat, activeChatId, onSelect, onDelete, confirm }) {
  const tool = TOOLS[chat.tool];
  return (
    <div onClick={() => onSelect(chat)}
      className={cn('group relative flex items-start gap-2 px-3 py-2.5 rounded-xl cursor-pointer transition-all duration-150',
        activeChatId===chat.id ? 'bg-gold-500/10 border border-gold-500/20' : 'hover:bg-ink-800/60 border border-transparent')}>
      <span className="text-sm mt-0.5 flex-shrink-0">{tool?.icon||'💬'}</span>
      <div className="flex-1 min-w-0">
        <p className={cn('text-xs font-medium truncate', activeChatId===chat.id?'text-gold-300':'text-ink-300')}>{chat.title}</p>
        <p className="text-[10px] text-ink-600">{formatDate(chat.updated_at)}</p>
      </div>
      <button onClick={e=>onDelete(e,chat.id)}
        className={cn('flex-shrink-0 w-5 h-5 flex items-center justify-center rounded text-[10px] transition-all opacity-0 group-hover:opacity-100',
          confirm===chat.id ? 'opacity-100 bg-coral-500/20 text-coral-400' : 'text-ink-600 hover:text-coral-400')}
        title={confirm===chat.id?'Click again to confirm':'Delete'}>
        {confirm===chat.id?'✕':'×'}
      </button>
    </div>
  );
}
