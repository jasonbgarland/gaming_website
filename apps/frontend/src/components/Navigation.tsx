"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuthStore } from "../store/auth";
import LogoutButton from "./auth/LogoutButton";

/**
 * Navigation component that shows different content based on auth state.
 * - When logged out: shows Login/Signup links
 * - When logged in: shows user info and Logout button
 */
const Navigation: React.FC = () => {
  const isLoggedIn = useAuthStore((state) => state.isLoggedIn);
  const user = useAuthStore((state) => state.user);

  return (
    <nav style={{ padding: "1rem", borderBottom: "1px solid #ccc" }}>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <div>
          <Link
            href="/"
            style={{
              fontSize: "1.2rem",
              fontWeight: "bold",
              textDecoration: "none",
            }}
          >
            Gaming Website
          </Link>
        </div>

        <div style={{ display: "flex", gap: "1rem", alignItems: "center" }}>
          {!isLoggedIn ? (
            <>
              <Link href="/login" style={{ textDecoration: "none" }}>
                Login
              </Link>
              <Link href="/signup" style={{ textDecoration: "none" }}>
                Signup
              </Link>
            </>
          ) : (
            <>
              {user?.email && (
                <span style={{ marginRight: "1rem" }}>{user.email}</span>
              )}
              <Link href="/library" style={{ textDecoration: "none" }}>
                My Library
              </Link>
              <LogoutButton />
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navigation;
