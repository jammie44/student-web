import { clsx } from 'clsx';
export const cn = (...a) => clsx(a);

export function formatDate(d) {
  if (!d) return '';
  const dt = new Date(d), now = new Date(), diff = now - dt;
  if (diff < 60000) return 'just now';
  if (diff < 3600000) return `${Math.floor(diff/60000)}m ago`;
  if (diff < 86400000) return `${Math.floor(diff/3600000)}h ago`;
  if (diff < 604800000) return `${Math.floor(diff/86400000)}d ago`;
  return dt.toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric'});
}

export function formatMarkdown(t) {
  if (!t) return '';
  return t
    .replace(/```([\s\S]*?)```/g,'<pre><code>$1</code></pre>')
    .replace(/`([^`]+)`/g,'<code>$1</code>')
    .replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>')
    .replace(/\*(.+?)\*/g,'<em>$1</em>')
    .replace(/^### (.+)$/gm,'<h3>$1</h3>')
    .replace(/^## (.+)$/gm,'<h2>$1</h2>')
    .replace(/^# (.+)$/gm,'<h1>$1</h1>')
    .replace(/^> (.+)$/gm,'<blockquote>$1</blockquote>')
    .replace(/^[-•*] (.+)$/gm,'<li>$1</li>')
    .replace(/^(\d+)\. (.+)$/gm,'<li>$2</li>')
    .replace(/(<li>[\s\S]+?<\/li>)/g,'<ul>$1</ul>')
    .replace(/^---$/gm,'<hr/>')
    .replace(/\n\n/g,'</p><p>')
    .replace(/\n/g,'<br/>');
}

export const TOOLS = {
  study_assistant:{id:'study_assistant',label:'Study Assistant',icon:'🎓',color:'blue',placeholder:'Ask any academic question — maths, science, history, philosophy…',description:'Detailed answers on any subject, any level',},
  plagiarism:{id:'plagiarism',label:'Plagiarism Checker',icon:'🔍',color:'purple',placeholder:'Paste your essay text here to check originality…',description:'Real originality analysis with specific feedback',},
  cv_generator:{id:'cv_generator',label:'CV Generator',icon:'📄',color:'green',placeholder:'e.g. "Create a CV for a cybersecurity professional with 3 years experience"',description:'Complete, filled-in professional CVs for any field',},
  assignment:{id:'assignment',label:'Assignment Helper',icon:'✏️',color:'gold',placeholder:'Paste your assignment text to format, or type a topic to get a full essay…',description:'Format and elevate your work to academic standard',},
  research:{id:'research',label:'Research Summarizer',icon:'🔬',color:'teal',placeholder:'Paste a research paper, article, or essay (min 50 words) to summarize…',description:'Extract key findings, themes, and conclusions',},
};

export const TOOL_COLORS = {
  blue:  {bg:'rgba(59,130,246,0.08)',border:'rgba(59,130,246,0.2)',text:'#60a5fa',glow:'rgba(59,130,246,0.15)'},
  purple:{bg:'rgba(139,92,246,0.08)',border:'rgba(139,92,246,0.2)',text:'#a78bfa',glow:'rgba(139,92,246,0.15)'},
  green: {bg:'rgba(16,185,129,0.08)',border:'rgba(16,185,129,0.2)',text:'#34d399',glow:'rgba(16,185,129,0.15)'},
  gold:  {bg:'rgba(245,158,11,0.08)',border:'rgba(245,158,11,0.2)',text:'#fbbf24',glow:'rgba(245,158,11,0.15)'},
  teal:  {bg:'rgba(20,184,166,0.08)',border:'rgba(20,184,166,0.2)',text:'#2dd4bf',glow:'rgba(20,184,166,0.15)'},
};
