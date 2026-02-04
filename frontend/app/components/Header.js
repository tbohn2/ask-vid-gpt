'use client';
import Link from "next/link";
import logo from "../../public/logo.png";
import playButton from "../../public/play-button.png";
import Image from "next/image";

export default function Header() {
    return (
        <header className="flex items-center justify-between w-full p-4">
            <Link href="/" className="flex items-center gap-2 w-1/2">
                <Image src={playButton} alt="play button" className="w-1/8" />
                <Image src={logo} alt="logo" className="w-3/8" />
            </Link>
            <nav className="flex flex-grow items-center justify-end gap-4 text-2xl">
                <Link href="/dashboard">Dashboard</Link>
                <Link href="/login">Login</Link>
            </nav>
        </header>
    );
}