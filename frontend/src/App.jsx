import React, { useEffect, useState } from "react";
import MemoryForm from "./components/MemoryForm.jsx";
import MemoryList from "./components/MemoryList.jsx";
import MemoryDetail from "./components/MemoryDetail.jsx";
import {
  fetchMemories,
  parseMemory,
  generateShotJson,
  renderMemoryShot
} from "./api/client.js";

export default function App() {
  const [memories, setMemories] = useState([]);
  const [selectedId, setSelectedId] = useState(null);
  const [loadingCreate, setLoadingCreate] = useState(false);
  const [loadingJson, setLoadingJson] = useState(false);
  const [loadingRender, setLoadingRender] = useState(false);

  const selectedMemory = memories.find((m) => m.id === selectedId) || null;

  const loadMemories = async () => {
    const data = await fetchMemories();
    setMemories(data);
    if (!selectedId && data.length > 0) {
      setSelectedId(data[0].id);
    }
  };

  useEffect(() => {
    loadMemories();
  }, []);

  const handleCreate = async (text) => {
    setLoadingCreate(true);
    try {
      const newMemory = await parseMemory(text);
      setMemories((prev) => [newMemory, ...prev]);
      setSelectedId(newMemory.id);
    } finally {
      setLoadingCreate(false);
    }
  };

  const handleGenerateJson = async (id) => {
    setLoadingJson(true);
    try {
      const { fiboJson } = await generateShotJson(id);
      setMemories((prev) =>
        prev.map((m) => (m.id === id ? { ...m, fiboJson } : m))
      );
    } finally {
      setLoadingJson(false);
    }
  };

  const handleRender = async (id) => {
    setLoadingRender(true);
    try {
      const { imageUrl } = await renderMemoryShot(id);
      setMemories((prev) =>
        prev.map((m) => (m.id === id ? { ...m, imageUrl } : m))
      );
    } finally {
      setLoadingRender(false);
    }
  };

  return (
    <div style={{ maxWidth: "1080px", margin: "0 auto", padding: "1rem" }}>
      <h1>LifeLens</h1>
      <p>
        Turn emotional memories into structured JSON and controllable FIBO images.
      </p>

      <MemoryForm onSubmit={handleCreate} loading={loadingCreate} />

      <div style={{ display: "flex", marginTop: "1rem" }}>
        <div style={{ flex: 1 }}>
          <MemoryList
            memories={memories}
            onSelect={setSelectedId}
            selectedId={selectedId}
          />
        </div>
        <div style={{ flex: 2 }}>
          <MemoryDetail
            memory={selectedMemory}
            onGenerateJson={handleGenerateJson}
            onRender={handleRender}
            loadingJson={loadingJson}
            loadingRender={loadingRender}
          />
        </div>
      </div>
    </div>
  );
}
