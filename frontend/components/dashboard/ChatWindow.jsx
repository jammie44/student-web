'use client';
import{useState,useEffect,useRef,useCallback}from'react';
import{TOOLS,TOOL_COLORS,formatMarkdown,cn}from'../../lib/utils';
import{api}from'../../lib/api';
import{Spinner,LoadingDots}from'../ui/Spinner';

export function ChatWindow({chat,onTitleUpdate,onMessageSent}){
  const[messages,setMessages]=useState([]);
  const[loading,setLoading]=useState(true);
  const[sending,setSending]=useState(false);
  const[input,setInput]=useState('');
  const[error,setError]=useState(null);
  const bottomRef=useRef(null);
  const taRef=useRef(null);
  const tool=TOOLS[chat?.tool]||TOOLS.study_assistant;
  const col=TOOL_COLORS[tool.color];

  const load=useCallback(async()=>{
    if(!chat?.id)return;
    setLoading(true);setError(null);setMessages([]);
    try{const d=await api.getMessages(chat.id);setMessages(d.messages||[]);}
    catch{setError('Could not load messages.');}
    finally{setLoading(false);}
  },[chat?.id]);

  useEffect(()=>{load();},[load]);
  useEffect(()=>{bottomRef.current?.scrollIntoView({behavior:'smooth'});},[messages,sending]);
  useEffect(()=>{if(!loading)setTimeout(()=>taRef.current?.focus(),80);},[loading]);

  const send=async()=>{
    const content=input.trim();if(!content||sending)return;
    setInput('');setSending(true);setError(null);
    if(taRef.current)taRef.current.style.height='auto';
    const tid=`tmp-${Date.now()}`;
    setMessages(p=>[...p,{id:tid,role:'user',content,created_at:new Date().toISOString()}]);
    try{
      const d=await api.sendMessage(chat.id,content);
      setMessages(p=>p.filter(m=>m.id!==tid).concat([d.user_message,d.ai_message]));
      if(onTitleUpdate)onTitleUpdate(chat.id,content.slice(0,50)+(content.length>50?'…':''));
      if(onMessageSent)onMessageSent();
    }catch(err){
      setMessages(p=>p.filter(m=>m.id!==tid));
      setError(err.message||'Failed to send. Please try again.');
    }finally{setSending(false);taRef.current?.focus();}
  };

  const onKey=e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();send();}};
  const onResize=e=>{e.target.style.height='auto';e.target.style.height=Math.min(e.target.scrollHeight,160)+'px';};

  const TIPS={
    study_assistant:['What is the pH of a neutral solution?','Explain osmosis with an example','Solve: 3x + 7 = 22','Prove infinite primes (Euclid)','What is Fermat\'s Little Theorem?','Explain SN1 vs SN2 reactions'],
    plagiarism:['Paste your essay text here to check for plagiarism','Check this paragraph for originality'],
    cv_generator:['Create a CV for a cybersecurity professional','Write a CV for a software engineer','Generate a CV for a chemist'],
    assignment:['Write an essay on what is art','Format my biology assignment on cell division'],
    research:['Paste a research paper here to summarize','Extract key findings from this article'],
  };

  return(
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="flex items-center gap-3 px-5 py-3.5 border-b bg-black/20 backdrop-blur-sm flex-shrink-0" style={{borderColor:'rgba(255,255,255,0.05)'}}>
        <div className="w-9 h-9 rounded-xl flex items-center justify-center text-lg border flex-shrink-0" style={{background:col.bg,borderColor:col.border}}>{tool.icon}</div>
        <div className="flex-1 min-w-0">
          <h2 className="text-sm font-semibold text-white truncate">{chat.title}</h2>
          <p className="text-xs" style={{color:'#475569'}}>{tool.label} · AI-powered</p>
        </div>
        <button onClick={load} disabled={loading} title="Reload messages" className="p-1.5 rounded-lg transition-colors" style={{color:'#334155'}}>↺</button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-5 min-h-0">
        {loading?(
          <div className="flex flex-col items-center justify-center h-40 gap-3">
            <Spinner/><p className="text-xs" style={{color:'#334155'}}>Loading chat history…</p>
          </div>
        ):messages.length===0?(
          <EmptyState tool={tool} col={col} tips={TIPS[tool.id]||TIPS.study_assistant} onSend={t=>{setInput(t);taRef.current?.focus();}}/>
        ):(
          <>
            {messages.map(m=><Bubble key={m.id} m={m}/>)}
            {sending&&<Typing/>}
          </>
        )}
        {error&&(
          <div className="mx-auto max-w-md p-3 rounded-xl text-xs text-center mt-2" style={{background:'rgba(239,68,68,0.1)',border:'1px solid rgba(239,68,68,0.3)',color:'#fca5a5'}}>
            {error} <button onClick={load} className="ml-2 underline" style={{color:'#60a5fa'}}>Reload</button>
          </div>
        )}
        <div ref={bottomRef}/>
      </div>

      {/* Input */}
      <div className="px-4 py-4 border-t bg-black/20 backdrop-blur-sm flex-shrink-0" style={{borderColor:'rgba(255,255,255,0.05)'}}>
        <div className="max-w-3xl mx-auto">
          <div className="flex items-end gap-3 rounded-2xl px-4 py-3 transition-all" style={{background:'rgba(255,255,255,0.04)',border:'1px solid rgba(255,255,255,0.1)'}}>
            <textarea ref={taRef} rows={1} value={input}
              onChange={e=>{setInput(e.target.value);onResize(e);}} onKeyDown={onKey}
              placeholder={tool.placeholder} disabled={sending}
              className="flex-1 bg-transparent border-none outline-none resize-none text-sm leading-relaxed disabled:opacity-60"
              style={{color:'#e2e8f0',minHeight:'24px',maxHeight:'160px'}}/>
            <button onClick={send} disabled={!input.trim()||sending}
              className="flex-shrink-0 w-9 h-9 rounded-xl flex items-center justify-center transition-all font-bold text-sm active:scale-95 disabled:cursor-not-allowed"
              style={input.trim()&&!sending?{background:'linear-gradient(to right,#2563eb,#3b82f6)',color:'#fff',boxShadow:'0 4px 15px rgba(59,130,246,0.25)'}:{background:'rgba(255,255,255,0.05)',color:'#334155'}}>
              {sending?<div className="w-4 h-4 border-2 rounded-full animate-spin" style={{borderColor:'rgba(255,255,255,0.3)',borderTopColor:'#fff'}}/>:'↑'}
            </button>
          </div>
          <p className="text-center mt-2 text-[10px]" style={{color:'#1e293b'}}>Enter to send · Shift+Enter for new line</p>
        </div>
      </div>
    </div>
  );
}

function Bubble({m}){
  const isUser=m.role==='user';
  return(
    <div className={cn('flex gap-3 max-w-3xl mx-auto py-1 animate-fade-in',isUser&&'flex-row-reverse')}>
      <div className="w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0 mt-0.5"
        style={isUser?{background:'linear-gradient(135deg,#3b82f6,#7c3aed)',color:'#fff'}:{background:'rgba(255,255,255,0.08)',border:'1px solid rgba(255,255,255,0.1)',color:'#94a3b8'}}>
        {isUser?'U':'🎓'}
      </div>
      <div className="flex-1 max-w-[85%] rounded-2xl px-4 py-3 text-sm leading-relaxed"
        style={isUser?{background:'rgba(59,130,246,0.15)',border:'1px solid rgba(59,130,246,0.2)',color:'#e2e8f0',borderTopRightRadius:'4px'}:{background:'rgba(255,255,255,0.04)',border:'1px solid rgba(255,255,255,0.08)',color:'#cbd5e1',borderTopLeftRadius:'4px'}}>
        {isUser?<p className="whitespace-pre-wrap">{m.content}</p>:<div className="message-content" dangerouslySetInnerHTML={{__html:formatMarkdown(m.content)}}/>}
      </div>
    </div>
  );
}

function Typing(){
  return(
    <div className="flex gap-3 max-w-3xl mx-auto py-1 animate-fade-in">
      <div className="w-7 h-7 rounded-full flex items-center justify-center text-xs flex-shrink-0" style={{background:'rgba(255,255,255,0.08)',border:'1px solid rgba(255,255,255,0.1)'}}>🎓</div>
      <div className="rounded-2xl px-4 py-3" style={{background:'rgba(255,255,255,0.04)',border:'1px solid rgba(255,255,255,0.08)',borderTopLeftRadius:'4px'}}><LoadingDots/></div>
    </div>
  );
}

function EmptyState({tool,col,tips,onSend}){
  return(
    <div className="flex flex-col items-center justify-center h-full text-center px-4 py-12 animate-fade-up">
      <div className="w-16 h-16 rounded-2xl flex items-center justify-center text-3xl mb-4 border" style={{background:col.bg,borderColor:col.border}}>{tool.icon}</div>
      <h3 className="font-bold text-white text-lg mb-2" style={{fontFamily:'Syne,sans-serif'}}>{tool.label}</h3>
      <p className="text-sm mb-8 max-w-sm" style={{color:'#64748b'}}>{tool.description}</p>
      <div className="space-y-2 w-full max-w-sm">
        <p className="text-[10px] font-bold uppercase tracking-widest mb-3" style={{color:'#334155'}}>Try asking</p>
        {tips.map((t,i)=>(
          <button key={i} onClick={()=>onSend(t)}
            className="w-full text-left px-4 py-3 rounded-xl text-xs transition-all"
            style={{background:'rgba(255,255,255,0.03)',border:'1px solid rgba(255,255,255,0.08)',color:'#64748b'}}>
            "{t}"
          </button>
        ))}
      </div>
    </div>
  );
}
