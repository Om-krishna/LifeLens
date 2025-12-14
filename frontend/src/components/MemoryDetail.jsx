import React from "react";
import ShotJsonView from "./ShotJsonView.jsx";
import ImagePreview from "./ImagePreview.jsx";

export default function MemoryDetail({
  memory,
  onGenerateJson,
  onRender,
  loadingJson,
  loadingRender
}) {
  if (!memory) return <p>Select a memory to see details.</p>;

  return (
    <div style={{ paddingLeft: "1rem" }}>
      <h2>Selected Memory</h2>
      <p>{memory.text}</p>

      <h3>Parsed Metadata</h3>
      <pre
        style={{
          background: "#f1f1f1",
          padding: "0.5rem",
          borderRadius: "4px",
          fontSize: "0.8rem"
        }}
      >
        {JSON.stringify(memory.metadata, null, 2)}
      </pre>

      <h3>FIBO JSON</h3>
      <button onClick={() => onGenerateJson(memory.id)} disabled={loadingJson}>
        {loadingJson ? "Generating JSON..." : "Generate FIBO JSON"}
      </button>
      <ShotJsonView fiboJson={memory.fiboJson} />

      <h3>Rendered Image</h3>
      <button
        onClick={() => onRender(memory.id)}
        disabled={loadingRender || !memory.fiboJson}
        style={{ marginBottom: "1.5rem" }} 
      >
        {loadingRender ? "Rendering..." : "Render with FIBO"}
      </button>
      <ImagePreview imageUrl={memory.imageUrl} />
    </div>
  );
}
