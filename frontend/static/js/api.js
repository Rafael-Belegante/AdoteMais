const API_BASE = "http://localhost:8000";

function getToken() {
    return localStorage.getItem("token");
}

function getUserId() {
    const raw = localStorage.getItem("user");
    if (!raw) return null;
    try {
        const data = JSON.parse(raw);
        return data.id_usuario;
    } catch {
        return null;
    }
}

async function apiRequest(path, options = {}) {
    const headers = options.headers || {};
    headers["Content-Type"] = headers["Content-Type"] || "application/json";
    const token = getToken();
    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }
    const res = await fetch(`${API_BASE}${path}`, {
        ...options,
        headers
    });
    if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || "Erro na requisição");
    }
    return res.json();
}
