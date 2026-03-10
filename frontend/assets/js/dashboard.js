// dashboard.js
const API_BASE = 'http://localhost:8000/api/v1';
const token = localStorage.getItem('token');

if (!token) {
    window.location.href = 'login.html';
}

const headers = {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
};

document.getElementById('logout').addEventListener('click', () => {
    localStorage.removeItem('token');
    window.location.href = 'login.html';
});

async function generateCV() {
    const data = document.getElementById('cvInput').value;
    const response = await fetch(`${API_BASE}/cv/generate`, {
        method: 'POST',
        headers,
        body: JSON.stringify({ data })
    });
    const result = await response.json();
    document.getElementById('cvOutput').innerText = result.content || result.detail;
}

async function formatAssignment() {
    const text = document.getElementById('assignmentInput').value;
    const response = await fetch(`${API_BASE}/assignments/format`, {
        method: 'POST',
        headers,
        body: JSON.stringify({ text })
    });
    const result = await response.json();
    document.getElementById('assignmentOutput').innerText = result.content || result.detail;
}

async function summarizeResearch() {
    const text = document.getElementById('researchInput').value;
    const response = await fetch(`${API_BASE}/research/summarize`, {
        method: 'POST',
        headers,
        body: JSON.stringify({ text })
    });
    const result = await response.json();
    document.getElementById('researchOutput').innerText = result.content || result.detail;
}

async function detectPlagiarism() {
    const text = document.getElementById('plagiarismInput').value;
    const response = await fetch(`${API_BASE}/plagiarism/detect`, {
        method: 'POST',
        headers,
        body: JSON.stringify({ text })
    });
    const result = await response.json();
    document.getElementById('plagiarismOutput').innerText = result.content || result.detail;
}

async function studyCopilot() {
    const question = document.getElementById('studyQuestion').value;
    const response = await fetch(`${API_BASE}/ai-chat/ask`, {
        method: 'POST',
        headers,
        body: JSON.stringify({ question })
    });
    const result = await response.json();
    document.getElementById('studyOutput').innerText = result.answer || result.detail;
}

async function uploadResearch() {
    const file = document.getElementById('researchFile').files[0];
    const formData = new FormData();
    formData.append('file', file);
    const response = await fetch(`${API_BASE}/research/upload`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` },
        body: formData
    });
    const result = await response.json();
    alert(result.message || result.detail);
}

async function askResearch() {
    const query = document.getElementById('researchQuery').value;
    const formData = new FormData();
    formData.append('query', query);
    const response = await fetch(`${API_BASE}/research/ask`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` },
        body: formData
    });
    const result = await response.json();
    document.getElementById('researchAskOutput').innerText = result.answer || result.detail;
}