import React, { useState } from "react";

export default function MemoryForm({ onSubmit, loading }) {
  const [text, setText] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!text.trim()) return;
    onSubmit(text);
    setText("");
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: "1rem" }}>
      <textarea
        rows={4}
        style={{ width: "100%", padding: "0.5rem" }}
        placeholder="Write a memory that means a lot to you..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <button type="submit" disabled={loading} style={{ marginTop: "0.5rem" }}>
        {loading ? "Creating..." : "Create Memory"}
      </button>
    </form>
  );
}
