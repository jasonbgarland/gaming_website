"use client";

import Link from "next/link";
import LogoutButton from "@/components/auth/LogoutButton";
import { User } from "@/store/auth";

export default function Navigation({ user }: { user: User | null }) {
  return (
    <nav className="bg-gamer-surface border-b border-gamer-border text-gamer-text">
      <div className="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
        <div className="flex items-center space-x-8">
          <Link
            href="/"
            className="text-xl font-bold text-gamer-primary hover:text-gamer-primary-hover"
          >
            GameHub
          </Link>
          <Link
            href="/library"
            className="text-gamer-text hover:text-gamer-primary"
          >
            Collections
          </Link>
        </div>
        <div className="flex items-center space-x-4">
          {user ? (
            <>
              <span className="text-gamer-muted">
                Welcome, {user?.username}!
              </span>
              <LogoutButton className="text-red-400 hover:text-red-300">
                Logout
              </LogoutButton>
            </>
          ) : (
            <>
              <Link
                href="/login"
                className="text-gamer-text hover:text-gamer-primary"
              >
                Login
              </Link>
              <Link
                href="/signup"
                className="text-gamer-text hover:text-gamer-primary"
              >
                Sign Up
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}
