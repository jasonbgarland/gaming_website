"use client";

import { useState } from "react";
import useSWR from "swr";
import { useDebounce } from "./useDebounce";

export interface Game {
  id: number;
  name: string;
  cover_url?: string;
  cover_images?: {
    thumb?: string;
    small?: string;
    medium?: string;
    large?: string;
  };
  platforms?: string[];
  release_year?: number;
}

export interface UseGameSearchOptions {
  debounceMs?: number;
  initialResults?: Game[];
}

/**
 * Custom hook to encapsulate game search logic.
 * Handles API calls, debouncing, loading state, and error handling.
 */
export function useGameSearch(options: UseGameSearchOptions = {}) {
  const { debounceMs = 350, initialResults } = options;

  const [query, setQuery] = useState("");

  // Debounce the query to avoid firing on every keystroke
  const debouncedQuery = useDebounce(query, debounceMs);

  // SWR fetcher function
  const fetcher = async () => {
    const API_URL = process.env.NEXT_PUBLIC_GAME_API_URL;
    if (!API_URL) {
      throw new Error("Game API URL is not configured.");
    }

    const response = await fetch(
      `${API_URL}/igdb/search?q=${encodeURIComponent(debouncedQuery)}`
    );

    if (!response.ok) {
      throw new Error("Failed to search games. Please try again.");
    }

    return response.json();
  };

  // Only fetch if debouncedQuery is non-empty
  const shouldFetch = !!(debouncedQuery && debouncedQuery.trim());

  const {
    data: results = initialResults ?? [],
    error,
    isLoading,
  } = useSWR<Game[]>(shouldFetch ? ["games", debouncedQuery] : null, fetcher);

  return {
    query,
    setQuery,
    results,
    isLoading,
    error,
    hasQuery: !!query.trim(),
    hasResults: !!(results && results.length > 0),
  };
}
