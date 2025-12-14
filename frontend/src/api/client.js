const API_BASE = "http://localhost:8000/api/memories";

export async function fetchMemories() {
  const res = await fetch(API_BASE);
  return res.json();
}

export async function parseMemory(text) {
  const res = await fetch(`${API_BASE}/parse`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text })
  });
  return res.json();
}

export async function generateShotJson(id) {
  const res = await fetch(`${API_BASE}/generate-json`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id })
  });
  return res.json();
}

export async function renderMemoryShot(id) {
  const res = await fetch(`${API_BASE}/render`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id })
  });
  return res.json();
}
