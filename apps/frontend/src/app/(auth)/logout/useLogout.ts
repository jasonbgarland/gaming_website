"use client";

import { useAuthStore } from "../../../store/auth";
import { useRouter } from "next/navigation";

/**
 * Custom hook to handle user logout.
 * Clears auth state, removes token from localStorage, and redirects to login.
 */
export function useLogout() {
  const logout = useAuthStore((state) => state.logout);
  const router = useRouter();

  /**
   * Handles the logout process
   */
  const handleLogout = () => {
    // Clear auth state in Zustand store
    logout();

    // Clear JWT token from localStorage
    localStorage.removeItem("token");

    // Redirect to login page
    router.push("/login");
  };

  return { handleLogout };
}
