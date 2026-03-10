// admin.js
const API_BASE = 'http://localhost:8000/api/v1';
const token = localStorage.getItem('token');

if (!token) {
    window.location.href = 'login.html';
}

const headers = {
    'Authorization': `Bearer ${token}`
};

document.getElementById('logout').addEventListener('click', () => {
    localStorage.removeItem('token');
    window.location.href = 'login.html';
});

async function loadAnalytics() {
    const response = await fetch(`${API_BASE}/admin/analytics`, { headers });
    const data = await response.json();
    const analyticsDiv = document.getElementById('analytics');
    analyticsDiv.innerHTML = `
        <div class="bg-white p-4 rounded shadow">
            <h3>Total Users</h3>
            <p class="text-2xl">${data.total_users}</p>
        </div>
        <div class="bg-white p-4 rounded shadow">
            <h3>Total Subscriptions</h3>
            <p class="text-2xl">${data.total_subscriptions}</p>
        </div>
        <div class="bg-white p-4 rounded shadow">
            <h3>Total AI Requests</h3>
            <p class="text-2xl">${data.total_ai_requests}</p>
        </div>
        <div class="bg-white p-4 rounded shadow">
            <h3>Total Credits</h3>
            <p class="text-2xl">${data.total_credits}</p>
        </div>
    `;
}

async function loadUsers() {
    const response = await fetch(`${API_BASE}/admin/users`, { headers });
    const users = await response.json();
    const tbody = document.querySelector('#usersTable tbody');
    tbody.innerHTML = users.map(user => `
        <tr>
            <td class="p-2">${user.id}</td>
            <td class="p-2">${user.email}</td>
            <td class="p-2">${user.is_active}</td>
            <td class="p-2">${user.is_admin}</td>
        </tr>
    `).join('');
}

async function loadSubscriptions() {
    const response = await fetch(`${API_BASE}/admin/subscriptions`, { headers });
    const subs = await response.json();
    const tbody = document.querySelector('#subsTable tbody');
    tbody.innerHTML = subs.map(sub => `
        <tr>
            <td class="p-2">${sub.id}</td>
            <td class="p-2">${sub.user_id}</td>
            <td class="p-2">${sub.stripe_subscription_id}</td>
            <td class="p-2">${sub.status}</td>
        </tr>
    `).join('');
}

document.addEventListener('DOMContentLoaded', () => {
    loadAnalytics();
    loadUsers();
    loadSubscriptions();
});