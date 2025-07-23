"use client";

import useSWR from "swr";
import { collectionsApi, Collection } from "../services/collectionsApi";

/**
 * Custom hook to manage a single collection by ID.
 * Handles fetching, loading state, and error handling for individual collections.
 * Use this for collection detail pages, edit forms, etc.
 */
export function useCollection(id: number | null) {
  // SWR fetcher function
  const fetcher = (id: number) => collectionsApi.getCollection(id);

  const {
    data: collection,
    error,
    isLoading,
    mutate,
  } = useSWR<Collection>(
    id ? `/collections/${id}` : null, // Only fetch if id is provided
    () => fetcher(id!)
  );

  const refreshCollection = () => {
    mutate();
  };

  return {
    collection,
    isLoading,
    error,
    refreshCollection,
    hasCollection: !!collection,
  };
}
