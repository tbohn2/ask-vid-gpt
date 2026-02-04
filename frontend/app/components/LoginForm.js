"use client";

import { useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000";

export default function LoginForm() {
  const [isSignUp, setIsSignUp] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState({ type: "", text: "" });
  const [loading, setLoading] = useState(false);

  const resetForm = () => {
    setUsername("");
    setPassword("");
    setMessage({ type: "", text: "" });
  };

  const handleToggleMode = () => {
    setIsSignUp((prev) => !prev);
    resetForm();
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage({ type: "", text: "" });
    setLoading(true);

    const url = isSignUp ? `${API_BASE}/api/users` : `${API_BASE}/api/login`;
    const body = { username, password };

    try {
      const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      const data = await res.json().catch(() => ({}));

      if (!res.ok) {
        setMessage({
          type: "error",
          text: data.message || data.error || "Something went wrong",
        });
        setLoading(false);
        return;
      }

      if (isSignUp) {
        setMessage({ type: "success", text: "Account created! You can log in now." });
        setIsSignUp(false);
        resetForm();
      } else {
        if (data.access_token) {
          if (typeof window !== "undefined") {
            localStorage.setItem("access_token", data.access_token);
            localStorage.setItem("user", JSON.stringify({ id: data.id, username: data.username }));
          }
          setMessage({ type: "success", text: "Logged in successfully." });
          resetForm();
          // Optional: redirect or refresh
          window.location.href = "/";
        } else {
          setMessage({ type: "error", text: "No token received." });
        }
      }
    } catch (err) {
      setMessage({
        type: "error",
        text: err.message || "Network error. Is the backend running?",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-sm rounded-2xl border border-zinc-200 bg-white p-8 shadow-lg dark:border-zinc-800 dark:bg-zinc-900">
      <h1 className="mb-2 text-2xl font-semibold text-zinc-900 dark:text-zinc-50">
        {isSignUp ? "Create account" : "Log in"}
      </h1>
      <p className="mb-6 text-sm text-zinc-500 dark:text-zinc-400">
        {isSignUp
          ? "Enter a username and password to sign up."
          : "Enter your credentials to sign in."}
      </p>

      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <label className="flex flex-col gap-1.5">
          <span className="text-sm font-medium text-zinc-700 dark:text-zinc-300">
            Username
          </span>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Your username"
            required
            autoComplete={isSignUp ? "username" : "username"}
            className="rounded-lg border border-zinc-300 bg-white px-3 py-2 text-zinc-900 placeholder-zinc-400 focus:border-zinc-500 focus:outline-none focus:ring-1 focus:ring-zinc-500 dark:border-zinc-600 dark:bg-zinc-800 dark:text-zinc-100 dark:placeholder-zinc-500"
          />
        </label>

        <label className="flex flex-col gap-1.5">
          <span className="text-sm font-medium text-zinc-700 dark:text-zinc-300">
            Password
          </span>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="••••••••"
            required
            autoComplete={isSignUp ? "new-password" : "current-password"}
            className="rounded-lg border border-zinc-300 bg-white px-3 py-2 text-zinc-900 placeholder-zinc-400 focus:border-zinc-500 focus:outline-none focus:ring-1 focus:ring-zinc-500 dark:border-zinc-600 dark:bg-zinc-800 dark:text-zinc-100 dark:placeholder-zinc-500"
          />
        </label>

        {message.text && (
          <p
            className={`rounded-lg px-3 py-2 text-sm ${
              message.type === "error"
                ? "bg-red-50 text-red-700 dark:bg-red-900/20 dark:text-red-400"
                : "bg-emerald-50 text-emerald-700 dark:bg-emerald-900/20 dark:text-emerald-400"
            }`}
          >
            {message.text}
          </p>
        )}

        <button
          type="submit"
          disabled={loading}
          className="mt-1 rounded-lg bg-zinc-900 px-4 py-2.5 font-medium text-white transition hover:bg-zinc-800 disabled:opacity-50 dark:bg-zinc-100 dark:text-zinc-900 dark:hover:bg-zinc-200"
        >
          {loading ? "Please wait…" : isSignUp ? "Create account" : "Log in"}
        </button>
      </form>

      <p className="mt-6 text-center text-sm text-zinc-500 dark:text-zinc-400">
        {isSignUp ? "Already have an account?" : "Don't have an account?"}{" "}
        <button
          type="button"
          onClick={handleToggleMode}
          className="font-medium text-zinc-900 underline underline-offset-2 hover:no-underline dark:text-zinc-100"
        >
          {isSignUp ? "Log in" : "Create account"}
        </button>
      </p>
    </div>
  );
}
