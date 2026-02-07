"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000";

export default function DashboardPage() {
  const [user, setUser] = useState(null);
  const [mounted, setMounted] = useState(false);
  const [collections, setCollections] = useState([]);
  const [selectedCollectionId, setSelectedCollectionId] = useState("");
  const [collectionsLoading, setCollectionsLoading] = useState(false);
  const [collectionsError, setCollectionsError] = useState(null);
  const [newName, setNewName] = useState("");
  const [newDescription, setNewDescription] = useState("");
  const [createLoading, setCreateLoading] = useState(false);
  const [createError, setCreateError] = useState(null);

  const fetchCollections = useCallback(async () => {
    if (!user?.id) return;
    setCollectionsLoading(true);
    setCollectionsError(null);
    try {
      const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;
      const res = await fetch(`${API_BASE}/api/collections?user_id=${user.id}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        setCollectionsError(data.message || data.error || "Failed to load collections");
        setCollections([]);
        return;
      }
      setCollections(data.collections || []);
      if (data.collections?.length && !selectedCollectionId) {
        setSelectedCollectionId(String(data.collections[0].id));
      }
    } catch (err) {
      setCollectionsError(err.message || "Network error");
      setCollections([]);
    } finally {
      setCollectionsLoading(false);
    }
  }, [user?.id]);

  useEffect(() => {
    setMounted(true);
    if (typeof window !== "undefined") {
      const stored = localStorage.getItem("user");
      if (stored) setUser(JSON.parse(stored));
    }
  }, []);

  useEffect(() => {
    if (user?.id && mounted) fetchCollections();
  }, [user?.id, mounted, fetchCollections]);

  const handleCreateCollection = async (e) => {
    e.preventDefault();
    if (!user?.id || !newName.trim()) return;
    setCreateLoading(true);
    setCreateError(null);
    try {
      const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;
      const res = await fetch(`${API_BASE}/api/collections`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: JSON.stringify({
          name: newName.trim(),
          user_id: user.id,
          ...(newDescription.trim() ? { description: newDescription.trim() } : {}),
        }),
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        setCreateError(data.message || data.error || "Failed to create collection");
        setCreateLoading(false);
        return;
      }
      setNewName("");
      setNewDescription("");
      await fetchCollections();
      if (data.id) setSelectedCollectionId(String(data.id));
    } catch (err) {
      setCreateError(err.message || "Network error");
    } finally {
      setCreateLoading(false);
    }
  };

  if (!mounted) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-primary">
        <p className="text-muted-foreground">Loading…</p>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center gap-4 bg-primary px-4">
        <p className="text-center text-muted-foreground">You need to log in to view this page.</p>
        <Link
          href="/login"
          className="rounded-lg bg-foreground px-6 py-3 font-medium text-background transition hover:opacity-90"
        >
          Go to login
        </Link>
      </div>
    );
  }

  const selectedCollection = collections.find((c) => String(c.id) === selectedCollectionId);

  return (
    <div className="min-h-screen bg-primary px-4 py-8">
        <h1 className="text-2xl font-semibold">Dashboard</h1>
        <p className="text-muted-foreground">
          Welcome, {user.username}. Manage your collections below.
        </p>

        <section className="rounded-xl border border-foreground/15 bg-background/50 p-6 shadow-sm">
          <h2 className="text-lg font-medium">Add a collection</h2>
          <form onSubmit={handleCreateCollection} className="mt-4 flex flex-wrap items-end gap-4">
            <label className="flex min-w-[180px] flex-1 flex-col gap-1">
              <span className="text-sm font-medium text-muted-foreground">Name</span>
              <input
                type="text"
                value={newName}
                onChange={(e) => setNewName(e.target.value)}
                placeholder="My collection"
                className="rounded-lg border border-foreground/20 bg-background px-3 py-2 placeholder-muted-foreground focus:border-foreground/50 focus:outline-none focus:ring-1 focus:ring-foreground/30"
              />
            </label>
            <label className="flex min-w-[180px] flex-1 flex-col gap-1">
              <span className="text-sm font-medium text-muted-foreground">
                Description (optional)
              </span>
              <input
                type="text"
                value={newDescription}
                onChange={(e) => setNewDescription(e.target.value)}
                placeholder="Brief description"
                className="rounded-lg border border-foreground/20 bg-background px-3 py-2 placeholder-muted-foreground focus:border-foreground/50 focus:outline-none focus:ring-1 focus:ring-foreground/30"
              />
            </label>
            <button
              type="submit"
              disabled={createLoading || !newName.trim()}
              className="rounded-lg bg-foreground px-5 py-2.5 font-medium text-background transition hover:opacity-90 disabled:opacity-50"
            >
              {createLoading ? "Adding…" : "Add collection"}
            </button>
          </form>
          {createError && <p className="mt-3 text-sm text-red-600">{createError}</p>}
        </section>

        <section className="rounded-xl border border-foreground/15 bg-background/50 p-6 shadow-sm">
          <h2 className="text-lg font-medium">Select collection</h2>
          {collectionsLoading ? (
            <p className="mt-3 text-sm text-muted-foreground">Loading collections…</p>
          ) : collectionsError ? (
            <p className="mt-3 text-sm text-red-600">{collectionsError}</p>
          ) : (
            <div className="mt-4">
              <label className="mb-2 block text-sm font-medium text-muted-foreground">
                Collection
              </label>
              <select
                value={selectedCollectionId}
                onChange={(e) => setSelectedCollectionId(e.target.value)}
                className="w-full max-w-md rounded-lg border border-foreground/20 bg-background px-3 py-2.5 focus:border-foreground/50 focus:outline-none focus:ring-1 focus:ring-foreground/30"
              >
                <option value="">Select a collection…</option>
                {collections.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.name}
                  </option>
                ))}
              </select>
              {selectedCollection && (
                <p className="mt-2 text-sm text-muted-foreground">
                  {selectedCollection.description || "No description."}
                </p>
              )}
            </div>
          )}
        </section>
    </div>
  );
}
