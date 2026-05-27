"use client";

import { useState } from "react";
import useSWR from "swr";
import { useDebounce } from "./useDebounce";
import { type Game } from "./useGameSearch";

export interface SearchFilters {
  platforms: number[];
  genres: number[];
  years: number[];
  yearStart?: number;
  yearEnd?: number;
  minRating?: number;
  maxRating?: number;
  themes: number[];
  playerPerspectives: number[];
}

export const DEFAULT_FILTERS: SearchFilters = {
  platforms: [],
  genres: [],
  years: [],
  yearStart: undefined,
  yearEnd: undefined,
  minRating: undefined,
  maxRating: undefined,
  themes: [],
  playerPerspectives: [],
};

export interface UseGameSearchOptions {
  debounceMs?: number;
  initialResults?: Game[];
}

/**
 * Build URL query params from search filters.
 * Omits empty arrays and undefined values — backend ignores absent params.
 * Exported as a standalone utility so tests can call it directly
 * without going through the hook.
 */
export function buildFilterParams(f: SearchFilters): string {
  const params: string[] = [];

  if (f.platforms.length > 0) params.push(`platforms=${f.platforms.join(",")}`);
  if (f.genres.length > 0) params.push(`genres=${f.genres.join(",")}`);
  if (f.years.length > 0) params.push(`years=${f.years.join(",")}`);
  if (f.yearStart !== undefined) params.push(`year_start=${f.yearStart}`);
  if (f.yearEnd !== undefined) params.push(`year_end=${f.yearEnd}`);
  if (f.minRating !== undefined) params.push(`min_rating=${f.minRating}`);
  if (f.maxRating !== undefined) params.push(`max_rating=${f.maxRating}`);
  if (f.themes.length > 0) params.push(`themes=${f.themes.join(",")}`);
  if (f.playerPerspectives.length > 0) params.push(`player_perspectives=${f.playerPerspectives.join(",")}`);

  return params.join("&");
}

/**
 * Custom hook for enhanced game search with filtering support.
 * Manages query text, filter state, API calls, debouncing, and error handling.
 * Hits the /search-enhanced backend endpoint which supports platform, genre,
 * year, rating, theme, and player perspective filters.
 */
export function useGameSearch(
  options: UseGameSearchOptions = {}
) {
  const { debounceMs = 350, initialResults } = options;

  const [query, setQuery] = useState("");
  const [filters, setFilters] = useState<SearchFilters>(DEFAULT_FILTERS);

  // Debounce the query to avoid firing on every keystroke
  const debouncedQuery = useDebounce(query, debounceMs);

  /**
   * Compute the full request URL from debounced query + filters.
   * This URL serves as the SWR key — when it changes, SWR re-fetches.
   */
  const filterParams = buildFilterParams(filters);
  const requestUrl =
    debouncedQuery.trim() && process.env.NEXT_PUBLIC_GAME_API_URL
      ? `${process.env.NEXT_PUBLIC_GAME_API_URL}/igdb/search-enhanced?q=${encodeURIComponent(debouncedQuery)}${filterParams ? `&${filterParams}` : ""}`
      : null;

  // Simple fetcher — just fetch the URL that's already built
  const fetcher = async (url: string) => {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error("Failed to search games. Please try again.");
    }
    return response.json();
  };

  const {
    data: results = initialResults ?? [],
    error,
    isLoading,
  } = useSWR<Game[]>(requestUrl, fetcher);

  /**
   * Update a single filter field without replacing the whole object.
   */
  function updateFilter<K extends keyof SearchFilters>(
    key: K,
    value: SearchFilters[K]
  ) {
    setFilters((prev) => ({ ...prev, [key]: value }));
  }

  /**
   * Reset all filters to defaults.
   */
  function clearFilters() {
    setFilters(DEFAULT_FILTERS);
  }

  /**
   * Count how many filter categories have non-default values.
   * Year range (start + end) counts as one logical filter.
   */
  const activeFilterCount = [
    filters.platforms.length > 0,
    filters.genres.length > 0,
    filters.years.length > 0,
    filters.yearStart !== undefined || filters.yearEnd !== undefined,
    filters.minRating !== undefined,
    filters.maxRating !== undefined,
    filters.themes.length > 0,
    filters.playerPerspectives.length > 0,
  ].filter(Boolean).length;

  return {
    query,
    setQuery,
    filters,
    setFilters,
    updateFilter,
    clearFilters,
    results,
    isLoading,
    error,
    hasQuery: !!query.trim(),
    hasResults: !!results && results.length > 0,
    activeFilterCount,
  };
}