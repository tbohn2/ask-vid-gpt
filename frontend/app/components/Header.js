'use client';

import { useEffect, useState } from "react";
import Link from "next/link";
import Image from "next/image";
import logo from "../../public/logo.png";
import playButton from "../../public/play-button.png";

export default function Header() {
  const [user, setUser] = useState(null);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    if (typeof window !== "undefined") {
      const stored = localStorage.getItem("user");
      if (stored) setUser(JSON.parse(stored));
    }
  }, []);

  const handleLogout = () => {
    if (typeof window !== "undefined") {
      localStorage.removeItem("access_token");
      localStorage.removeItem("user");
      setUser(null);
      window.location.href = "/";
    }
  };

  return (
    <header className="flex items-center justify-between w-full p-4">
      <Link href="/" className="flex items-center gap-2 w-1/2">
        <Image src={playButton} alt="play button" className="w-1/8" />
        <Image src={logo} alt="logo" className="w-3/8" />
      </Link>
      <nav className="flex flex-grow items-center justify-end gap-4 text-2xl">
        <Link href="/dashboard">Dashboard</Link>
        {mounted && user ? (
          <button type="button" onClick={handleLogout}>
            Logout
          </button>
        ) : (
          <Link href="/login">Login</Link>
        )}
      </nav>
    </header>
  );
}