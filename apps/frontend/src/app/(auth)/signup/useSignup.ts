"use client";

import { useState } from "react";
import { useAuthStore } from "../../../store/auth";
import { useRouter } from "next/navigation";

export type SignupCredentials = {
  username: string;
  email: string;
  password: string;
  confirmPassword: string;
};

/**
 * Custom hook to encapsulate signup logic for the SignupPage.
 * Handles API call, error state, loading state, and redirects.
 */
export function useSignup() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const login = useAuthStore((state) => state.login);
  const router = useRouter();

  /**
   * Handles signup form submission.
   * @param credentials - The user's username, email, password, and confirmPassword
   */
  const handleSignup = async ({
    username,
    email,
    password,
    confirmPassword,
  }: SignupCredentials) => {
    setIsLoading(true);
    setError("");

    // Client-side validation
    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      setIsLoading(false);
      return;
    }

    const API_URL = process.env.NEXT_PUBLIC_AUTH_API_URL;
    if (!API_URL) {
      setError(
        "Auth API URL is not configured. Please set NEXT_PUBLIC_AUTH_API_URL."
      );
      setIsLoading(false);
      return;
    }
    try {
      const response = await fetch(`${API_URL}/signup`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, password }),
      });
      if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        const errorMessage =
          errorData?.detail ||
          "Invalid signup. Please check your details and try again.";
        setError(errorMessage);
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

      // Update global auth state (Zustand will handle localStorage persistence)
      login(data.access_token);
      // Redirect user to home page after successful signup
      router.push("/");
    } catch {
      setError("Network error: Unable to sign up. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };
  return { handleSignup, isLoading, error };
}
