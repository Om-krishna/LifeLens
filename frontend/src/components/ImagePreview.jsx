import React from "react";

export default function ImagePreview({ imageUrl }) {
  if (!imageUrl) return <p>No image rendered yet.</p>;

  return (
    <div>
      <img
        src={imageUrl}
        alt="Rendered memory"
        style={{ maxWidth: "100%", borderRadius: "4px" }}
      />
    </div>
  );
}
