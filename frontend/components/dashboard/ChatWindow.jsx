'use client';
import { useState, useEffect, useRef, useCallback } from 'react';
import { TOOLS, TOOL_COLORS, formatMarkdown, cn } from '../../lib/utils';
import { api } from '../../lib/api';
import { Spinner, LoadingDots } from '../ui/Spinner';

export function ChatWindow({ chat, onTitleUpdate, onMessageSent }) {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const [input, setInput] = useState('');
  const [error, setError] = useState(null);
  const bottomRef = useRef(null);
  const textareaRef = useRef(null);
  const tool = TOOLS[chat?.tool] || TOOLS.study_assistant;
  const col = TOOL_COLORS[tool.color];

  const loadMessages = useCallback(async () => {
    if (!chat?.id) return;
    setLoading(true); setError(null);
    try {
      const d = await api.getMessages(chat.id);
      setMessages(d.messages || []);
    } catch { setError('Failed to load messages.'); }
    finally { setLoading(false); }
  }, [chat?.id]);

  useEffect(() => { loadMessages(); }, [loadMessages]);
  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [messages, sending]);

  const handleSend = async () => {
    const content = input.trim();
    if (!content || sending) return;
    setInput(''); setSending(true); setError(null);
    // reset textarea height
    if (textareaRef.current) textareaRef.current.style.height = 'auto';
    const tempId = `tmp-${Date.now()}`;
    setMessages(prev => [...prev, { id: tempId, role: 'user', content, created_at: new Date().toISOString() }]);
    try {
      const d = await api.sendMessage(chat.id, content);
      setMessages(prev => prev.filter(m => m.id !== tempId).concat([d.user_message, d.ai_message]));
      if (onTitleUpdate) onTitleUpdate(chat.id, content.slice(0, 50) + (content.length > 50 ? '…' : ''));
      if (onMessageSent) onMessageSent();
    } catch (err) {
      setMessages(prev => prev.filter(m => m.id !== tempId));
      setError(err.message || 'Failed to send. Please try again.');
    } finally {
      setSending(false);
      textareaRef.current?.focus();
    }
  };

  const handleKey = e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSend(); } };
  const autoResize = e => { e.target.style.height = 'auto'; e.target.style.height = Math.min(e.target.scrollHeight, 160) + 'px'; };

  const TIPS = {
    study_assistant: ['What is the pH of a neutral solution?', 'Explain osmosis with examples', "Explain Newton's second law", 'What is the basic unit of life?'],
    plagiarism:      ['Paste your essay text here to check originality', 'Check this paragraph for plagiarism'],
    cv_generator:    ['Create a CV for a cybersecurity professional with 3 years experience', 'Write a CV for a software engineer', 'Generate a CV for a data scientist'],
    assignment:      ['Format and improve my biology assignment on cells', 'Help structure my essay on climate change'],
    research:        ['Summarise this research paper on AI', 'Extract key findings from this article'],
  };
  const tips = TIPS[tool.id] || TIPS.study_assistant;

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="flex items-center gap-3 px-5 py-3.5 border-b border-white/5 bg-black/20 backdrop-blur-sm flex-shrink-0">
        <div className="w-9 h-9 rounded-xl flex items-center justify-center text-lg border flex-shrink-0"
          style={{ background: col.bg, borderColor: col.border }}>
          {tool.icon}
        </div>
        <div>
          <h2 className="text-sm font-semibold text-white leading-tight">{chat.title}</h2>
          <p className="text-xs text-ink-500">{tool.label} · AI-powered</p>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-5 space-y-1 min-h-0">
        {loading ? (
          <div className="flex items-center justify-center h-40"><Spinner /></div>
        ) : messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center px-4 py-12 animate-fade-up">
            <div className="w-16 h-16 rounded-2xl flex items-center justify-center text-3xl mb-4 border"
              style={{ background: col.bg, borderColor: col.border }}>
              {tool.icon}
            </div>
            <h3 className="font-display font-bold text-white text-lg mb-2">{tool.label}</h3>
            <p className="text-ink-400 text-sm mb-2 max-w-sm">{tool.description}</p>
            <p className="text-xs text-ink-600 mb-8">Responses are real, specific, and detailed — not generic templates</p>
            <div className="space-y-2 w-full max-w-sm">
              <p className="text-[10px] text-ink-600 uppercase tracking-widest font-bold mb-3">Try asking</p>
              {tips.map((tip, i) => (
                <button key={i} onClick={() => { setInput(tip); textareaRef.current?.focus(); }}
                  className="w-full text-left px-4 py-3 rounded-xl bg-white/3 border border-white/8 text-xs text-ink-400 hover:text-ink-200 hover:border-white/20 hover:bg-white/6 transition-all">
                  "{tip}"
                </button>
              ))}
            </div>
          </div>
        ) : (
          <>
            {messages.map(m => <MessageBubble key={m.id} message={m} toolColor={col} />)}
            {sending && <TypingIndicator />}
          </>
        )}
        {error && (
          <div className="mx-auto max-w-md p-3 bg-red-500/10 border border-red-500/30 rounded-xl text-red-300 text-xs text-center">{error}</div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div className="px-4 py-4 border-t border-white/5 bg-black/20 backdrop-blur-sm flex-shrink-0">
        <div className="max-w-3xl mx-auto">
          <div className="flex items-end gap-3 bg-white/4 border border-white/10 rounded-2xl px-4 py-3 focus-within:border-blue-500/40 focus-within:ring-1 focus-within:ring-blue-500/15 transition-all">
            <textarea
              ref={textareaRef} rows={1} value={input}
              onChange={e => { setInput(e.target.value); autoResize(e); }}
              onKeyDown={handleKey} placeholder={tool.placeholder} disabled={sending}
              className="flex-1 bg-transparent border-none outline-none resize-none text-sm text-ink-100 placeholder:text-ink-600 leading-relaxed min-h-[24px] max-h-[160px] disabled:opacity-60"
            />
            <button onClick={handleSend} disabled={!input.trim() || sending}
              className={cn(
                'flex-shrink-0 w-9 h-9 rounded-xl flex items-center justify-center transition-all duration-150 font-bold text-sm',
                input.trim() && !sending
                  ? 'bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-500 hover:to-blue-400 text-white shadow-lg shadow-blue-500/25 active:scale-95'
                  : 'bg-white/5 text-ink-600 cursor-not-allowed'
              )}>
              {sending
                ? <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                : '↑'}
            </button>
          </div>
          <p className="text-[10px] text-ink-700 text-center mt-2">Enter to send · Shift+Enter for new line</p>
        </div>
      </div>
    </div>
  );
}

function MessageBubble({ message, toolColor }) {
  const isUser = message.role === 'user';
  return (
    <div className={cn('flex gap-3 max-w-3xl mx-auto py-1 animate-fade-up', isUser && 'flex-row-reverse')}>
      <div className={cn(
        'w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0 mt-0.5',
        isUser
          ? 'bg-gradient-to-br from-blue-500 to-purple-600 text-white'
          : 'bg-white/8 border border-white/10 text-ink-300'
      )}>
        {isUser ? 'U' : '🎓'}
      </div>
      <div className={cn(
        'flex-1 max-w-[85%] rounded-2xl px-4 py-3 text-sm leading-relaxed',
        isUser
          ? 'bg-blue-600/15 border border-blue-500/20 text-ink-100 rounded-tr-sm'
          : 'bg-white/4 border border-white/8 text-ink-200 rounded-tl-sm'
      )}>
        {isUser
          ? <p className="whitespace-pre-wrap">{message.content}</p>
          : <div className="message-content" dangerouslySetInnerHTML={{ __html: formatMarkdown(message.content) }} />
        }
      </div>
    </div>
  );
}

function TypingIndicator() {
  return (
    <div className="flex gap-3 max-w-3xl mx-auto py-1 animate-fade-in">
      <div className="w-7 h-7 rounded-full bg-white/8 border border-white/10 flex items-center justify-center text-xs flex-shrink-0">🎓</div>
      <div className="bg-white/4 border border-white/8 rounded-2xl rounded-tl-sm px-4 py-3">
        <LoadingDots />
      </div>
    </div>
  );
}
