import React from "react";

export default function MemoryList({ memories, onSelect, selectedId }) {
  return (
    <div style={{ borderRight: "1px solid #ccc", paddingRight: "1rem" }}>
      <h3>Memories</h3>
      {memories.length === 0 && <p>No memories yet. Create one above.</p>}
      <ul style={{ listStyle: "none", padding: 0 }}>
        {memories.map((m) => (
          <li
            key={m.id}
            onClick={() => onSelect(m.id)}
            style={{
              marginBottom: "0.5rem",
              padding: "0.5rem",
              cursor: "pointer",
              backgroundColor: m.id === selectedId ? "#eef" : "#f9f9f9",
              borderRadius: "4px"
            }}
          >
            <strong>{new Date(m.createdAt).toLocaleString()}</strong>
            <p style={{ margin: 0, fontSize: "0.85rem" }}>
              {m.text.length > 80 ? m.text.slice(0, 80) + "..." : m.text}
            </p>
          </li>
        ))}
      </ul>
    </div>
  );
}
