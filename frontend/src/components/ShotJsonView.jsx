import React from "react";

export default function ShotJsonView({ fiboJson }) {
  if (!fiboJson) return <p>No FIBO JSON generated yet.</p>;

  return (
    <pre
      style={{
        background: "#111",
        color: "#0f0",
        padding: "0.5rem",
        fontSize: "0.75rem",
        borderRadius: "4px",
        maxHeight: "200px",
        overflow: "auto"
      }}
    >
      {JSON.stringify(fiboJson, null, 2)}
    </pre>
  );
}
