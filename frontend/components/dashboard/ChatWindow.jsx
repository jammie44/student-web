'use client';
import { useState, useEffect, useRef, useCallback } from 'react';
import { api } from '../../lib/api';
import { TOOLS, formatMarkdown, cn } from '../../lib/utils';
import { Spinner, LoadingDots } from '../ui/Spinner';

export function ChatWindow({ chat, onTitleUpdate }) {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const [input, setInput] = useState('');
  const [error, setError] = useState(null);
  const bottomRef = useRef(null);
  const textareaRef = useRef(null);
  const tool = TOOLS[chat?.tool] || TOOLS.study_assistant;

  const loadMessages = useCallback(async () => {
    if (!chat?.id) return;
    setLoading(true); setError(null);
    try {
      const data = await api.getMessages(chat.id);
      setMessages(data.messages || []);
    } catch { setError('Failed to load messages.'); }
    finally { setLoading(false); }
  }, [chat?.id]);

  useEffect(() => { loadMessages(); }, [loadMessages]);
  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior:'smooth' }); }, [messages, sending]);

  const handleSend = async () => {
    const content = input.trim();
    if (!content || sending) return;
    setInput(''); setSending(true); setError(null);
    const tempId = `temp-${Date.now()}`;
    setMessages(prev => [...prev, { id:tempId, role:'user', content, created_at:new Date().toISOString() }]);
    try {
      const data = await api.sendMessage(chat.id, content);
      setMessages(prev => prev.filter(m=>m.id!==tempId).concat([data.user_message, data.ai_message]));
      if (onTitleUpdate) onTitleUpdate(chat.id, content.slice(0,50)+(content.length>50?'…':''));
    } catch (err) {
      setMessages(prev => prev.filter(m=>m.id!==tempId));
      setError(err.message || 'Failed to send message.');
    } finally {
      setSending(false); textareaRef.current?.focus();
    }
  };

  const handleKey = (e) => { if (e.key==='Enter' && !e.shiftKey) { e.preventDefault(); handleSend(); } };
  const autoResize = (e) => { e.target.style.height='auto'; e.target.style.height=Math.min(e.target.scrollHeight,160)+'px'; };

  const colorCls = tool.color==='gold'?'bg-gold-500/10 border-gold-500/20':tool.color==='jade'?'bg-jade-500/10 border-jade-500/20':'bg-coral-500/10 border-coral-500/20';

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="flex items-center gap-3 px-6 py-4 border-b border-ink-800/60 bg-ink-950/80 backdrop-blur-sm flex-shrink-0">
        <div className={cn('w-9 h-9 rounded-xl flex items-center justify-center text-lg border', colorCls)}>{tool.icon}</div>
        <div>
          <h2 className="text-sm font-semibold text-ink-100">{chat.title}</h2>
          <p className="text-xs text-ink-500">{tool.label}</p>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-6 space-y-1 min-h-0">
        {loading ? (
          <div className="flex items-center justify-center h-40"><Spinner/></div>
        ) : messages.length===0 ? (
          <EmptyState tool={tool} onSend={msg=>{ setInput(msg); textareaRef.current?.focus(); }}/>
        ) : (
          <>
            {messages.map(m=><MessageBubble key={m.id} message={m}/>)}
            {sending && <TypingIndicator/>}
          </>
        )}
        {error && <div className="mx-auto max-w-md p-3 bg-coral-500/10 border border-coral-500/30 rounded-xl text-coral-300 text-xs text-center">{error}</div>}
        <div ref={bottomRef}/>
      </div>

      {/* Input */}
      <div className="px-4 py-4 border-t border-ink-800/60 bg-ink-950/80 backdrop-blur-sm flex-shrink-0">
        <div className="max-w-3xl mx-auto">
          <div className="flex items-end gap-3 bg-ink-900/80 border border-ink-700 rounded-2xl px-4 py-3 focus-within:border-gold-500/50 focus-within:ring-1 focus-within:ring-gold-500/20 transition-all">
            <textarea ref={textareaRef} rows={1} value={input}
              onChange={e=>{ setInput(e.target.value); autoResize(e); }}
              onKeyDown={handleKey} placeholder={tool.placeholder} disabled={sending}
              className="flex-1 bg-transparent border-none outline-none resize-none text-sm text-ink-100 placeholder:text-ink-600 leading-relaxed min-h-[24px] max-h-[160px] disabled:opacity-60"/>
            <button onClick={handleSend} disabled={!input.trim()||sending}
              className={cn('flex-shrink-0 w-9 h-9 rounded-xl flex items-center justify-center transition-all duration-150',
                input.trim()&&!sending?'bg-gold-500 hover:bg-gold-400 text-ink-950 shadow-lg shadow-gold-500/20 active:scale-95':'bg-ink-800 text-ink-600 cursor-not-allowed')}>
              {sending?<div className="w-4 h-4 border-2 border-ink-600 border-t-ink-300 rounded-full animate-spin"/>:'↑'}
            </button>
          </div>
          <p className="text-[10px] text-ink-700 text-center mt-2">Enter to send · Shift+Enter for new line</p>
        </div>
      </div>
    </div>
  );
}

function MessageBubble({ message }) {
  const isUser = message.role==='user';
  return (
    <div className={cn('flex gap-3 max-w-3xl mx-auto py-1 animate-fade-up', isUser&&'flex-row-reverse')}>
      <div className={cn('w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0 mt-0.5',
        isUser?'bg-gold-500/20 border border-gold-500/30 text-gold-400':'bg-ink-800 border border-ink-700 text-ink-400')}>
        {isUser?'U':'🎓'}
      </div>
      <div className={cn('flex-1 max-w-[80%] rounded-2xl px-4 py-3 text-sm leading-relaxed',
        isUser?'bg-gold-500/10 border border-gold-500/20 text-ink-100 rounded-tr-sm':'bg-ink-800/80 border border-ink-700/60 text-ink-200 rounded-tl-sm')}>
        {isUser
          ? <p className="whitespace-pre-wrap">{message.content}</p>
          : <div className="message-content" dangerouslySetInnerHTML={{__html:formatMarkdown(message.content)}}/>}
      </div>
    </div>
  );
}

function TypingIndicator() {
  return (
    <div className="flex gap-3 max-w-3xl mx-auto py-1 animate-fade-in">
      <div className="w-7 h-7 rounded-full bg-ink-800 border border-ink-700 flex items-center justify-center text-xs flex-shrink-0">🎓</div>
      <div className="bg-ink-800/80 border border-ink-700/60 rounded-2xl rounded-tl-sm px-4 py-3"><LoadingDots/></div>
    </div>
  );
}

function EmptyState({ tool, onSend }) {
  const suggestions = {
    study_assistant:['Explain photosynthesis simply','Help me study for exams','What is Newton\'s second law?'],
    plagiarism:['Check my essay for plagiarism','Analyse this paragraph for originality'],
    cv_generator:['Create a CV for a CS graduate','Write a professional summary'],
    assignment:['Format my biology assignment','Improve my essay structure'],
    research:['Summarise this research paper','Extract key findings from my text'],
  };
  const tips = suggestions[tool.id]||suggestions.study_assistant;
  const colorCls = tool.color==='gold'?'bg-gold-500/10 border-gold-500/20':tool.color==='jade'?'bg-jade-500/10 border-jade-500/20':'bg-coral-500/10 border-coral-500/20';
  return (
    <div className="flex flex-col items-center justify-center h-full text-center px-4 py-16 animate-fade-up">
      <div className={cn('w-16 h-16 rounded-2xl flex items-center justify-center text-3xl mb-4 border', colorCls)}>{tool.icon}</div>
      <h3 className="font-display font-bold text-ink-200 text-lg mb-2">{tool.label}</h3>
      <p className="text-ink-500 text-sm mb-8 max-w-sm">{tool.description}</p>
      <div className="space-y-2 w-full max-w-sm">
        <p className="text-[10px] text-ink-600 uppercase tracking-widest font-bold mb-3">Try asking</p>
        {tips.map((tip,i)=>(
          <button key={i} onClick={()=>onSend(tip)}
            className="w-full text-left px-4 py-3 rounded-xl bg-ink-900/60 border border-ink-800 text-xs text-ink-400 hover:text-ink-200 hover:border-gold-500/30 hover:bg-gold-500/5 transition-all">
            "{tip}"
          </button>
        ))}
      </div>
    </div>
  );
}
