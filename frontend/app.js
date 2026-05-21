const API = 'http://127.0.0.1:8000/api/v1';

// ─── Helpers ──────────────────────────────────────────────────

function getToken()  { return localStorage.getItem('access_token'); }
function getRefresh(){ return localStorage.getItem('refresh_token'); }

function setMessage(id, text, isSuccess = false) {
  const el = document.getElementById(id);
  if (!el) return;
  el.textContent = text;
  el.className = 'message' + (isSuccess ? ' success' : '');
}

async function apiFetch(path, options = {}) {
  const headers = { 'Content-Type': 'application/json', ...options.headers };
  const token = getToken();
  if (token) headers['Authorization'] = `Bearer ${token}`;

  let res = await fetch(`${API}${path}`, { ...options, headers });

  // Auto-refresh token if expired
  if (res.status === 401 && getRefresh()) {
    const ref = await fetch(`${API}/auth/refresh/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh: getRefresh() }),
    });
    if (ref.ok) {
      const data = await ref.json();
      localStorage.setItem('access_token', data.access);
      headers['Authorization'] = `Bearer ${data.access}`;
      res = await fetch(`${API}${path}`, { ...options, headers });
    } else {
      logout(); return null;
    }
  }
  return res;
}

// ─── Auth ─────────────────────────────────────────────────────

function showTab(tab) {
  document.getElementById('login-tab').style.display    = tab === 'login'    ? 'block' : 'none';
  document.getElementById('register-tab').style.display = tab === 'register' ? 'block' : 'none';
  document.querySelectorAll('.tab').forEach((t, i) => {
    t.classList.toggle('active', (i === 0 && tab === 'login') || (i === 1 && tab === 'register'));
  });
}

async function login() {
  const email    = document.getElementById('login-email').value;
  const password = document.getElementById('login-password').value;

  const res  = await fetch(`${API}/auth/login/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });
  const data = await res.json();

  if (res.ok) {
    localStorage.setItem('access_token',  data.access);
    localStorage.setItem('refresh_token', data.refresh);
    localStorage.setItem('user', JSON.stringify(data.user));
    window.location.href = 'dashboard.html';
  } else {
    setMessage('auth-message', data.error || 'Login failed.');
  }
}

async function register() {
  const body = {
    username:  document.getElementById('reg-username').value,
    email:     document.getElementById('reg-email').value,
    password:  document.getElementById('reg-password').value,
    password2: document.getElementById('reg-password2').value,
  };
  const res  = await fetch(`${API}/auth/register/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  const data = await res.json();

  if (res.ok) {
    setMessage('auth-message', 'Registered! Please login.', true);
    showTab('login');
  } else {
    const errs = Object.values(data).flat().join(' ');
    setMessage('auth-message', errs);
  }
}

function logout() {
  localStorage.clear();
  window.location.href = 'index.html';
}

// ─── Dashboard Guard ──────────────────────────────────────────

async function initDashboard() {
  if (!getToken()) { window.location.href = 'index.html'; return; }

  const res = await apiFetch('/auth/me/');
  if (!res || !res.ok) { logout(); return; }

  const user = await res.json();
  document.getElementById('user-info').textContent = `${user.email} (${user.role})`;
  loadTasks();
}

// ─── Tasks CRUD ───────────────────────────────────────────────

async function loadTasks() {
  const res  = await apiFetch('/tasks/');
  const data = await res.json();
  renderTasks(data.results ?? data);
}

function renderTasks(tasks) {
  const list = document.getElementById('tasks-list');
  if (!tasks.length) { list.innerHTML = '<p style="color:#888">No tasks yet.</p>'; return; }

  list.innerHTML = tasks.map(t => `
    <div class="task-item">
      <div>
        <span class="status-badge s-${t.status}">${t.status.replace('_',' ')}</span>
        <h4>${t.title}</h4>
        <p>${t.description || '—'}</p>
      </div>
      <div class="task-actions">
        ${t.status !== 'done' ? `<button class="btn-done" onclick="markDone(${t.id})">Done</button>` : ''}
        <button class="btn-delete" onclick="deleteTask(${t.id})">Delete</button>
      </div>
    </div>
  `).join('');
}

async function createTask() {
  const title = document.getElementById('task-title').value.trim();
  const desc  = document.getElementById('task-desc').value.trim();
  if (!title) { setMessage('dash-message', 'Title is required.'); return; }

  const res = await apiFetch('/tasks/', {
    method: 'POST',
    body: JSON.stringify({ title, description: desc }),
  });
  if (res.ok) {
    document.getElementById('task-title').value = '';
    document.getElementById('task-desc').value  = '';
    setMessage('dash-message', 'Task created!', true);
    loadTasks();
  } else {
    const data = await res.json();
    setMessage('dash-message', JSON.stringify(data.errors || data));
  }
}

async function deleteTask(id) {
  if (!confirm('Delete this task?')) return;
  await apiFetch(`/tasks/${id}/`, { method: 'DELETE' });
  loadTasks();
}

async function markDone(id) {
  await apiFetch(`/tasks/${id}/`, {
    method: 'PATCH',
    body: JSON.stringify({ status: 'done' }),
  });
  loadTasks();
}

// ─── Page Router ─────────────────────────────────────────────

if (window.location.pathname.includes('dashboard')) {
  initDashboard();
}