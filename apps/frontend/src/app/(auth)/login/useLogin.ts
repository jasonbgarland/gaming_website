"use client";

import { useState } from "react";
import { useAuthStore } from "../../../store/auth";
import { useRouter } from "next/navigation";

export type LoginCredentials = {
  email: string;
  password: string;
};

/**
 * Custom hook to encapsulate login logic for the LoginPage.
 * Handles API call, error state, loading state, and redirects.
 */
export function useLogin() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const login = useAuthStore((state) => state.login);
  const router = useRouter();

  /**
   * Handles login form submission.
   * @param credentials - The user's email and password
   */
  const handleLogin = async ({ email, password }: LoginCredentials) => {
    setIsLoading(true);
    setError("");
    const API_URL = process.env.NEXT_PUBLIC_AUTH_API_URL;
    if (!API_URL) {
      setError(
        "Auth API URL is not configured. Please set NEXT_PUBLIC_AUTH_API_URL."
      );
      setIsLoading(false);
      return;
    }
    try {
      const response = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      if (!response.ok) {
        setError("Invalid credentials. Please check your email and password.");
        return;
      }
      let data: { access_token?: string; token_type?: string };
      try {
        data = await response.json();
      } catch {
        setError("Unexpected error: Could not parse server response.");
        return;
      }
      if (!data || !data.access_token) {
        setError("Unexpected error: No token received from server.");
        return;
      }

      // Get user information using the token
      try {
        const meResponse = await fetch(`${API_URL}/me`, {
          headers: {
            Authorization: `Bearer ${data.access_token}`,
            "Content-Type": "application/json",
          },
        });

        if (!meResponse.ok) {
          setError("Unexpected error: Could not get user information.");
          return;
        }

        const userData = await meResponse.json();

        // Update global auth state (Zustand will handle localStorage persistence)
        login(data.access_token, userData);
      } catch {
        setError("Network error: Could not get user information.");
        return;
      }

      // Redirect user to dashboard or home
      router.push("/");
    } catch {
      setError("Network error: Unable to login. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return { handleLogin, isLoading, error };
}
