const BASE_URL = import.meta.env.VITE_BACKEND_URL || 'http://127.0.0.1:8000';

async function request(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json', ...(options.headers||{}) },
    ...options
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Request failed ${res.status}: ${text}`);
  }
  return res.json();
}

export async function fetchPackages() {
  return request('/api/packages');
}

export async function aiRecommend(text) {
  return request('/api/ai-recommend', {
    method: 'POST',
    body: JSON.stringify({ text })
  });
}

export async function createLead(lead) {
  return request('/api/create-lead', {
    method: 'POST',
    body: JSON.stringify(lead)
  });
}

export async function searchPackages(filters) {
  return request('/api/search-packages', {
    method: 'POST',
    body: JSON.stringify(filters)
  });
}
