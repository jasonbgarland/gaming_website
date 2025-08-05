"use client";

import useSWR from "swr";
import {
  collectionEntryApi,
  CollectionEntry,
  CreateCollectionEntryRequest,
  UpdateCollectionEntryRequest,
} from "../services/collectionEntryApi";

/**
 * Custom hook to manage collection entries for a specific collection.
 * Handles API calls, loading state, error handling, and cache management.
 */
export function useCollectionEntries(collectionId: number) {
  // SWR fetcher function
  const fetcher = () => collectionEntryApi.getCollectionEntries(collectionId);

  const {
    data: entries = [],
    error,
    isLoading,
    mutate,
  } = useSWR<CollectionEntry[]>(
    collectionId ? `/collections/${collectionId}/entries` : null,
    fetcher
  );

  // Add a game to the collection
  const addEntry = async (
    data: CreateCollectionEntryRequest
  ): Promise<CollectionEntry> => {
    // OPTIMISTIC UPDATE: Add entry immediately (with temp ID)
    const optimisticEntry: CollectionEntry = {
      id: Date.now(),
      collection_id: collectionId,
      game_id: data.game_id,
      notes: data.notes,
      status: data.status,
      rating: data.rating,
      custom_tags: data.custom_tags,
      added_at: new Date().toISOString(),
    };
    mutate([...entries, optimisticEntry], false);

    try {
      const newEntry = await collectionEntryApi.createCollectionEntry(
        collectionId,
        data
      );
      mutate(
        entries.filter((e) => e.id !== optimisticEntry.id).concat(newEntry),
        false
      );
      return newEntry;
    } catch (error) {
      mutate(
        entries.filter((e) => e.id !== optimisticEntry.id),
        false
      );
      throw error;
    }
  };

  // Remove a game from the collection
  const removeEntry = async (entryId: number): Promise<void> => {
    const originalEntries = entries;
    mutate(
      entries.filter((e) => e.id !== entryId),
      false
    );
    try {
      await collectionEntryApi.deleteCollectionEntry(collectionId, entryId);
    } catch (error) {
      mutate(originalEntries, false);
      throw error;
    }
  };

  // Update a collection entry
  const updateEntry = async (
    entryId: number,
    data: UpdateCollectionEntryRequest
  ): Promise<CollectionEntry> => {
    const originalEntries = entries;
    const optimisticUpdate = entries.map((e) =>
      e.id === entryId ? { ...e, ...data } : e
    );
    mutate(optimisticUpdate, false);
    try {
      const updatedEntry = await collectionEntryApi.updateCollectionEntry(
        collectionId,
        entryId,
        data
      );
      mutate(
        entries.map((e) => (e.id === entryId ? updatedEntry : e)),
        false
      );
      return updatedEntry;
    } catch (error) {
      mutate(originalEntries, false);
      throw error;
    }
  };

  const refreshEntries = () => {
    mutate();
  };

  return {
    entries,
    isLoading,
    error,
    addEntry,
    removeEntry,
    updateEntry,
    refreshEntries,
    hasEntries: entries.length > 0,
  };
}
