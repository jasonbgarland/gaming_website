/**
 * DEMO: Navigation Conditional Rendering Flow
 * This component shows exactly how the navigation updates
 */

"use client";

import React from "react";
import { useAuthStore } from "../store/auth";

const NavigationDemo: React.FC = () => {
  const isLoggedIn = useAuthStore((state) => state.isLoggedIn);
  const user = useAuthStore((state) => state.user);
  const token = useAuthStore((state) => state.token);
  const login = useAuthStore((state) => state.login);
  const logout = useAuthStore((state) => state.logout);

  // Debug logging to show re-renders
  console.log("🔄 Navigation re-rendered with:", { isLoggedIn, user, token });

  return (
    <div style={{ padding: "1rem", border: "2px solid #ccc", margin: "1rem" }}>
      <h3>Navigation Demo - Conditional Rendering</h3>

      {/* State Display */}
      <div
        style={{ background: "#f5f5f5", padding: "1rem", marginBottom: "1rem" }}
      >
        <strong>Current State:</strong>
        <ul>
          <li>isLoggedIn: {String(isLoggedIn)}</li>
          <li>user: {user ? user.email : "null"}</li>
          <li>token: {token ? "***" + token.slice(-4) : "null"}</li>
        </ul>
      </div>

      {/* Conditional Navigation */}
      <div
        style={{ background: "#e3f2fd", padding: "1rem", marginBottom: "1rem" }}
      >
        <strong>Navigation Renders:</strong>
        <div style={{ marginTop: "0.5rem" }}>
          {!isLoggedIn ? (
            // 🚪 LOGGED OUT STATE
            <div style={{ color: "red" }}>
              ❌ Logged Out Navigation:
              <div style={{ marginLeft: "1rem" }}>
                • [Login Button] • [Signup Button]
              </div>
            </div>
          ) : (
            // ✅ LOGGED IN STATE
            <div style={{ color: "green" }}>
              ✅ Logged In Navigation:
              <div style={{ marginLeft: "1rem" }}>
                • Welcome: {user?.email}• [My Library Link] • [Logout Button]
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Demo Controls */}
      <div>
        <strong>Demo Controls:</strong>
        <div style={{ marginTop: "0.5rem", display: "flex", gap: "1rem" }}>
          <button
            onClick={() =>
              login("demo-jwt-token", {
                email: "demo@example.com",
                username: "demouser",
              })
            }
            disabled={isLoggedIn}
            style={{
              padding: "0.5rem 1rem",
              backgroundColor: isLoggedIn ? "#ccc" : "#4caf50",
              color: "white",
              border: "none",
              borderRadius: "4px",
            }}
          >
            Simulate Login
          </button>

          <button
            onClick={() => logout()}
            disabled={!isLoggedIn}
            style={{
              padding: "0.5rem 1rem",
              backgroundColor: !isLoggedIn ? "#ccc" : "#f44336",
              color: "white",
              border: "none",
              borderRadius: "4px",
            }}
          >
            Simulate Logout
          </button>
        </div>
      </div>

      {/* Nested Conditional Example */}
      <div
        style={{ marginTop: "1rem", padding: "1rem", background: "#fff3e0" }}
      >
        <strong>Nested Conditional Example:</strong>
        <div style={{ marginTop: "0.5rem" }}>
          {isLoggedIn && (
            <div>
              🔐 User is authenticated
              {user?.email && (
                <div style={{ marginLeft: "1rem" }}>
                  📧 Email verified: {user.email}
                  {user.email.includes("admin") && (
                    <div style={{ marginLeft: "1rem", color: "purple" }}>
                      👑 Admin privileges detected
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default NavigationDemo;
