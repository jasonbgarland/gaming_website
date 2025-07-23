"use client";

import useSWR from "swr";
import {
  collectionsApi,
  Collection,
  CreateCollectionRequest,
  UpdateCollectionRequest,
} from "../services/collectionsApi";

/**
 * Custom hook to manage collections data and operations.
 * Handles API calls, loading state, error handling, and cache management.
 */
export function useCollections() {
  // SWR fetcher function
  const fetcher = () => collectionsApi.getCollections();

  const {
    data: collections = [],
    error,
    isLoading,
    mutate,
  } = useSWR<Collection[]>("/collections", fetcher);

  // Helper functions for collection operations
  const createCollection = async (
    data: CreateCollectionRequest
  ): Promise<Collection> => {
    // Create optimistic collection with temporary ID
    const optimisticCollection: Collection = {
      id: Date.now(), // Temporary ID until server responds
      user_id: 0, // Will be filled by server
      name: data.name,
      description: data.description || "",
    };

    // OPTIMISTIC UPDATE: Update UI immediately
    mutate([...collections, optimisticCollection], false);

    try {
      // Make the actual API call
      const newCollection = await collectionsApi.createCollection(data);

      // Replace the optimistic version with the real one
      mutate(
        collections
          .filter((c) => c.id !== optimisticCollection.id) // Remove optimistic
          .concat(newCollection), // Add real one
        false
      );

      return newCollection;
    } catch (error) {
      // ROLLBACK: Remove the optimistic update on failure
      mutate(
        collections.filter((c) => c.id !== optimisticCollection.id),
        false
      );
      throw error; // Re-throw so UI can handle the error
    }
  };

  const deleteCollection = async (id: number): Promise<void> => {
    // OPTIMISTIC UPDATE: Remove from UI immediately
    const originalCollections = collections;
    mutate(
      collections.filter((c) => c.id !== id),
      false
    );

    try {
      // Make the actual API call
      await collectionsApi.deleteCollection(id);
      // Success! The optimistic update was correct
    } catch (error) {
      // ROLLBACK: Restore the original list on failure
      mutate(originalCollections, false);
      throw error;
    }
  };

  const updateCollection = async (
    id: number,
    data: UpdateCollectionRequest
  ): Promise<Collection> => {
    // OPTIMISTIC UPDATE: Update UI immediately
    const originalCollections = collections;
    const optimisticUpdate = collections.map((c) =>
      c.id === id ? { ...c, ...data } : c
    );
    mutate(optimisticUpdate, false);

    try {
      // Make the actual API call
      const updatedCollection = await collectionsApi.updateCollection(id, data);

      // Replace optimistic version with server response
      mutate(
        collections.map((c) => (c.id === id ? updatedCollection : c)),
        false
      );

      return updatedCollection;
    } catch (error) {
      // ROLLBACK: Restore original data on failure
      mutate(originalCollections, false);
      throw error;
    }
  };

  const refreshCollections = () => {
    mutate();
  };

  return {
    collections,
    isLoading,
    error,
    createCollection,
    deleteCollection,
    updateCollection,
    refreshCollections,
    hasCollections: collections.length > 0,
  };
}
