"use client";

import { create } from "zustand";

export interface User {
  email?: string;
  [key: string]: unknown;
}

interface AuthState {
  isLoggedIn: boolean;
  token: string | null;
  user: User | null;
  login: (token: string, user?: User) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  isLoggedIn: false,
  token: null,
  user: null,
  login: (token, user) => set({ isLoggedIn: true, token, user }),
  logout: () => set({ isLoggedIn: false, token: null, user: null }),
}));
