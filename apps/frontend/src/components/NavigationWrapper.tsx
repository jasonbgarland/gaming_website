"use client";

import React from "react";
import { useAuthStore } from "@/store/auth";
import Navigation from "./Navigation";

/**
 * Client-side wrapper for Navigation that handles auth state
 */
export default function NavigationWrapper() {
  const user = useAuthStore((state) => state.user);

  return <Navigation user={user} />;
}
