import { clsx } from 'clsx';
export const cn = (...a) => clsx(a);
export function formatDate(date) {
  if (!date) return '';
  const d = new Date(date), now = new Date(), diff = now - d;
  if (diff < 60000) return 'just now';
  if (diff < 3600000) return `${Math.floor(diff/60000)}m ago`;
  if (diff < 86400000) return `${Math.floor(diff/3600000)}h ago`;
  if (diff < 604800000) return `${Math.floor(diff/86400000)}d ago`;
  return d.toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric'});
}
export function formatMarkdown(text) {
  if (!text) return '';
  return text
    .replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>')
    .replace(/\*(.+?)\*/g,'<em>$1</em>')
    .replace(/`([^`]+)`/g,'<code>$1</code>')
    .replace(/^### (.+)$/gm,'<h3>$1</h3>')
    .replace(/^## (.+)$/gm,'<h2>$1</h2>')
    .replace(/^# (.+)$/gm,'<h1>$1</h1>')
    .replace(/^[-•] (.+)$/gm,'<li>$1</li>')
    .replace(/^---$/gm,'<hr/>')
    .replace(/\n\n/g,'</p><p>')
    .replace(/\n/g,'<br/>');
}
export const TOOLS = {
  study_assistant: { id:'study_assistant', label:'Study Assistant',     icon:'🎓', color:'gold',  placeholder:'Ask me anything about your studies…',         description:'Get explanations, summaries, and study help' },
  plagiarism:      { id:'plagiarism',      label:'Plagiarism Checker',  icon:'🔍', color:'coral', placeholder:'Paste your text to check for plagiarism…',     description:'Check your work for originality' },
  cv_generator:    { id:'cv_generator',    label:'CV Generator',        icon:'📄', color:'jade',  placeholder:'Describe your experience and skills…',         description:'Create professional CVs and resumes' },
  assignment:      { id:'assignment',      label:'Assignment Helper',   icon:'✏️', color:'gold',  placeholder:'Paste your assignment for formatting help…',   description:'Format and improve your assignments' },
  research:        { id:'research',        label:'Research Summarizer', icon:'🔬', color:'jade',  placeholder:'Paste research text to summarize…',            description:'Summarize papers and research' },
};
