"use client";

import { useEffect, useState } from "react";

type VisitStatus = "not_visited" | "passed_by" | "visited" | "thorough";

type Place = {
  id: number;
  name: string;
  category: string;
  lat: number;
  lon: number;
  status: VisitStatus;
};

const API_BASE = "http://localhost:8000";

export default function Home() {
  const [places, setPlaces] = useState<Place[]>([]);
  const [loading, setLoading] = useState(false);

  async function loadPlaces() {
    const res = await fetch(`${API_BASE}/places`);
    const data = await res.json();
    setPlaces(data);
  }

  useEffect(() => {
    loadPlaces().catch(console.error);
  }, []);

  async function setStatus(placeId: number, status: VisitStatus) {
    try {
      setLoading(true);
      const res = await fetch(`${API_BASE}/visits`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ place_id: placeId, status }),
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(text);
      }

      // simplest: re-fetch after save
      await loadPlaces();
    } catch (e) {
      console.error(e);
      alert("Failed to save status. Check console + backend logs.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main style={{ padding: 20, fontFamily: "system-ui" }}>
      <h1 style={{ fontSize: 24, fontWeight: 700 }}>Places</h1>
      <p style={{ color: "#555" }}>
        Click a button → POST to backend → backend saves → UI refreshes.
      </p>

      {loading && <p>Saving…</p>}

      <ul style={{ padding: 0, listStyle: "none", marginTop: 16 }}>
        {places.map((p) => (
          <li
            key={p.id}
            style={{
              padding: 12,
              border: "1px solid #ddd",
              borderRadius: 12,
              marginBottom: 12,
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              gap: 12,
            }}
          >
            <div>
              <div style={{ fontWeight: 600 }}>{p.name}</div>
              <div style={{ fontSize: 13, color: "#666" }}>
                {p.category} • status: <b>{p.status}</b>
              </div>
            </div>

            <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
              <button onClick={() => setStatus(p.id, "not_visited")}>Not</button>
              <button onClick={() => setStatus(p.id, "visited")}>Visited</button>
              <button onClick={() => setStatus(p.id, "explored")}>Explored</button>
            </div>
          </li>
        ))}
      </ul>
    </main>
  );
}
