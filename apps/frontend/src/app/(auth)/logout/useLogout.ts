"use client";

import { useAuthStore } from "../../../store/auth";
import { useRouter } from "next/navigation";

/**
 * Custom hook to handle user logout.
 * Clears auth state (Zustand will handle localStorage persistence).
 */
export function useLogout() {
  const logout = useAuthStore((state) => state.logout);
  const router = useRouter();

  /**
   * Handles the logout process
   */
  const handleLogout = () => {
    // Clear auth state in Zustand store (this will also clear localStorage via persist middleware)
    logout();

    // Redirect to login page
    router.push("/login");
  };

  return { handleLogout };
}
