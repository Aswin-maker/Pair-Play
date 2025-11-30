const envBase = (import.meta.env.VITE_BACKEND_URL || '').trim();
const BASE_URL = envBase || (typeof window !== 'undefined' && window.location && window.location.port === '5173'
  ? ''
  : 'http://127.0.0.1:8000');

async function request(path, options = {}) {
  const url = `${BASE_URL}${path}`;
  const res = await fetch(url, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options
  });

  const contentType = res.headers.get('content-type') || '';

  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`HTTP ${res.status} ${res.statusText} at ${url}: ${text}`);
  }

  if (contentType.includes('application/json')) {
    return res.json();
  }
  const text = await res.text().catch(() => '');
  throw new Error(`Expected JSON but received ${contentType || 'unknown'} from ${url}: ${text.slice(0, 200)}`);
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
