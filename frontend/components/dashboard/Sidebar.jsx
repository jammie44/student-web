'use client';
import { useState } from 'react';
import Link from 'next/link';
import { cn, TOOLS, TOOL_COLORS, formatDate } from '../../lib/utils';

export function Sidebar({ chats, loadingChats, activeChatId, activeTool, onSelectChat, onToolSelect, onDeleteChat, collapsed, user, onLogout, usage }) {
  const [deleteConfirm, setDeleteConfirm] = useState(null);
  const [search, setSearch] = useState('');
  const [toolsExpanded, setToolsExpanded] = useState(true);
  const [historyExpanded, setHistoryExpanded] = useState(true);

  const filtered = search
    ? chats.filter(c => c.title.toLowerCase().includes(search.toLowerCase()))
    : chats;

  const grouped = Object.keys(TOOLS).reduce((acc, t) => {
    acc[t] = filtered.filter(c => c.tool === t);
    return acc;
  }, {});

  const handleDelete = async (e, id) => {
    e.stopPropagation();
    if (deleteConfirm === id) { await onDeleteChat(id); setDeleteConfirm(null); }
    else { setDeleteConfirm(id); setTimeout(() => setDeleteConfirm(null), 3000); }
  };

  const planColor = user?.plan === 'pro' ? 'text-amber-400' : user?.plan === 'unlimited' ? 'text-purple-400' : 'text-ink-400';
  const planLabel = user?.plan === 'pro' ? '⭐ Pro' : user?.plan === 'unlimited' ? '♾ Unlimited' : '🆓 Free';

  return (
    <aside className={cn(
      'flex flex-col h-full glass-sidebar transition-all duration-300 overflow-hidden',
      collapsed ? 'w-0' : 'w-72'
    )}>
      {/* Header */}
      <div className="flex items-center gap-3 px-4 py-4 border-b border-white/5 flex-shrink-0">
        <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-sm shadow-lg flex-shrink-0">🎓</div>
        <div className="flex-1 min-w-0">
          <span className="font-display font-bold text-white text-base tracking-tight">StudyHub</span>
          <span className={cn('ml-2 text-xs font-semibold', planColor)}>{planLabel}</span>
        </div>
      </div>

      {/* Daily Usage Panel */}
      {usage && (
        <div className="px-3 py-3 border-b border-white/5 flex-shrink-0">
          <button
            onClick={() => setToolsExpanded(p => !p)}
            className="flex items-center justify-between w-full mb-2 group"
          >
            <span className="text-[10px] font-bold text-ink-500 uppercase tracking-widest">Daily Usage</span>
            <span className="text-ink-600 group-hover:text-ink-400 text-xs transition-colors">{toolsExpanded ? '▲' : '▼'}</span>
          </button>
          {toolsExpanded && (
            <div className="space-y-2.5">
              {Object.values(TOOLS).map(tool => {
                const u = usage?.usage?.[tool.id];
                if (!u) return null;
                const pct = Math.min(100, (u.used / u.limit) * 100);
                const col = TOOL_COLORS[tool.color];
                const barColor = pct >= 100 ? '#ef4444' : pct >= 80 ? '#f59e0b' : col.text;
                return (
                  <div key={tool.id}>
                    <div className="flex items-center justify-between mb-1">
                      <button
                        onClick={() => onToolSelect(tool.id)}
                        className="flex items-center gap-1.5 text-xs text-ink-400 hover:text-ink-200 transition-colors"
                      >
                        <span>{tool.icon}</span>
                        <span className="truncate max-w-[110px]">{tool.label}</span>
                      </button>
                      <span className={cn('text-[10px] font-bold tabular-nums', u.exhausted ? 'text-red-400' : 'text-ink-500')}>
                        {u.used}/{u.limit}
                      </span>
                    </div>
                    <div className="usage-bar">
                      <div
                        className="usage-bar-fill"
                        style={{ width: `${pct}%`, background: barColor }}
                      />
                    </div>
                  </div>
                );
              })}
              {usage?.plan === 'free' && (
                <Link href="/pricing" className="block mt-2 text-center text-[10px] font-semibold text-blue-400 hover:text-blue-300 bg-blue-500/10 hover:bg-blue-500/15 border border-blue-500/20 rounded-lg py-1.5 transition-all">
                  ⚡ Upgrade to Pro →
                </Link>
              )}
            </div>
          )}
        </div>
      )}

      {/* Search */}
      <div className="px-3 py-2.5 border-b border-white/5 flex-shrink-0">
        <div className="relative">
          <span className="absolute left-3 top-1/2 -translate-y-1/2 text-ink-500 text-xs">🔍</span>
          <input
            type="text"
            placeholder="Search chats…"
            value={search}
            onChange={e => setSearch(e.target.value)}
            className="w-full bg-white/5 border border-white/8 rounded-lg pl-7 pr-3 py-2 text-xs text-ink-200 placeholder:text-ink-600 outline-none focus:border-blue-500/40 transition-colors"
          />
        </div>
      </div>

      {/* Chat History */}
      <div className="flex-1 overflow-y-auto min-h-0">
        <div className="px-3 py-2">
          <button
            onClick={() => setHistoryExpanded(p => !p)}
            className="flex items-center justify-between w-full mb-2 group"
          >
            <span className="text-[10px] font-bold text-ink-500 uppercase tracking-widest">Recent Chats</span>
            <span className="text-ink-600 group-hover:text-ink-400 text-xs transition-colors">{historyExpanded ? '▲' : '▼'}</span>
          </button>

          {historyExpanded && (
            loadingChats ? (
              <div className="space-y-2">
                {[1,2,3].map(i => <div key={i} className="h-11 rounded-xl skeleton" />)}
              </div>
            ) : filtered.length === 0 ? (
              <div className="text-center py-8">
                <p className="text-2xl mb-2">💬</p>
                <p className="text-xs text-ink-600">{search ? 'No chats match' : 'No chats yet — pick a tool!'}</p>
              </div>
            ) : search ? (
              <div className="space-y-0.5">
                {filtered.map(c => <ChatItem key={c.id} chat={c} activeChatId={activeChatId} onSelect={onSelectChat} onDelete={handleDelete} confirm={deleteConfirm} />)}
              </div>
            ) : (
              Object.entries(grouped).map(([tid, tChats]) => {
                if (!tChats.length) return null;
                const tool = TOOLS[tid];
                const col = TOOL_COLORS[tool.color];
                return (
                  <div key={tid} className="mb-4">
                    <div className="flex items-center gap-1.5 px-2 mb-1.5">
                      <span className="text-xs">{tool.icon}</span>
                      <span className="text-[10px] font-bold uppercase tracking-widest" style={{ color: col.text }}>{tool.label}</span>
                    </div>
                    <div className="space-y-0.5">
                      {tChats.map(c => <ChatItem key={c.id} chat={c} activeChatId={activeChatId} onSelect={onSelectChat} onDelete={handleDelete} confirm={deleteConfirm} />)}
                    </div>
                  </div>
                );
              })
            )
          )}
        </div>
      </div>

      {/* Footer */}
      <div className="px-3 py-3 border-t border-white/5 flex-shrink-0 space-y-1">
        {user?.is_admin && (
          <Link href="/admin" className="flex items-center gap-2 px-3 py-2 rounded-xl text-xs font-semibold text-ink-400 hover:text-amber-400 hover:bg-amber-500/10 transition-all">
            <span>⚙️</span> Admin Dashboard
          </Link>
        )}
        <Link href="/pricing" className="flex items-center gap-2 px-3 py-2 rounded-xl text-xs font-semibold text-ink-400 hover:text-blue-400 hover:bg-blue-500/10 transition-all">
          <span>💎</span> Plans & Pricing
        </Link>
        <div className="flex items-center gap-3 px-3 py-2.5 rounded-xl bg-white/3 border border-white/5 mt-1">
          <div className="w-7 h-7 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-xs font-bold text-white flex-shrink-0">
            {user?.name?.[0]?.toUpperCase() || user?.email?.[0]?.toUpperCase() || '?'}
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-xs font-semibold text-ink-100 truncate">{user?.name || 'Student'}</p>
            <p className="text-[10px] text-ink-500 truncate">{user?.email}</p>
          </div>
          <button onClick={onLogout} title="Sign out" className="text-ink-600 hover:text-red-400 transition-colors p-1 text-sm">⇥</button>
        </div>
      </div>
    </aside>
  );
}

function ChatItem({ chat, activeChatId, onSelect, onDelete, confirm }) {
  const tool = TOOLS[chat.tool];
  const col = TOOL_COLORS[tool?.color || 'blue'];
  const active = activeChatId === chat.id;
  return (
    <div
      onClick={() => onSelect(chat)}
      className={cn(
        'group relative flex items-start gap-2 px-3 py-2.5 rounded-xl cursor-pointer transition-all duration-150 border',
        active
          ? 'border-opacity-50 text-white'
          : 'border-transparent hover:border-white/8 hover:bg-white/4'
      )}
      style={active ? { background: col.bg, borderColor: col.border } : {}}
    >
      <span className="text-sm mt-0.5 flex-shrink-0">{tool?.icon || '💬'}</span>
      <div className="flex-1 min-w-0">
        <p className={cn('text-xs font-medium truncate', active ? 'text-white' : 'text-ink-300')}>{chat.title}</p>
        <p className="text-[10px] text-ink-600 mt-0.5">{formatDate(chat.updated_at)}</p>
      </div>
      <button
        onClick={e => onDelete(e, chat.id)}
        className={cn(
          'flex-shrink-0 w-5 h-5 flex items-center justify-center rounded text-[10px] transition-all',
          confirm === chat.id
            ? 'opacity-100 bg-red-500/20 text-red-400'
            : 'opacity-0 group-hover:opacity-100 text-ink-600 hover:text-red-400'
        )}
      >
        {confirm === chat.id ? '✕' : '×'}
      </button>
    </div>
  );
}
