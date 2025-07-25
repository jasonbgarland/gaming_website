"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";

export interface User {
  email?: string;
  [key: string]: unknown;
}

export interface AuthState {
  isLoggedIn: boolean;
  token: string | null;
  user: User | null;
  login: (token: string, user?: User) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      isLoggedIn: false,
      token: null,
      user: null,
      login: (token, user) => set({ isLoggedIn: true, token, user }),
      logout: () => set({ isLoggedIn: false, token: null, user: null }),
    }),
    {
      name: "auth-storage", // key in localStorage
      partialize: (state) => ({
        token: state.token,
        user: state.user,
        isLoggedIn: state.isLoggedIn,
      }),
    }
  )
);
