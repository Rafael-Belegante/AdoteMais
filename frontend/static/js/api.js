const API_BASE = "http://localhost:8000";

function getToken() {
  return localStorage.getItem("token");
}

function getUser() {
  const raw = localStorage.getItem("user");
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

function getUserId() {
  const u = getUser();
  return u ? u.id_usuario : null;
}

function buildQuery(params = {}) {
  const entries = Object.entries(params).filter(
    ([, v]) => v !== undefined && v !== null && String(v).trim() !== ""
  );
  if (!entries.length) return "";
  const qs = new URLSearchParams();
  for (const [k, v] of entries) {
    qs.append(k, v);
  }
  return "?" + qs.toString();
}

async function apiRequest(path, options = {}) {
  const headers = options.headers ? { ...options.headers } : {};

  if (!headers["Content-Type"] && !(options.body instanceof FormData)) {
    headers["Content-Type"] = "application/json";
  }

  const token = getToken();
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    let detail = "Erro na requisição";
    try {
      const data = await response.json();
      if (data && data.detail) {
        detail = data.detail;
      }
    } catch {}
    throw new Error(detail);
  }

  if (response.status === 204) return null;

  return response.json();
}
