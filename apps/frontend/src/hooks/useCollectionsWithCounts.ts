"use client";

import useSWR from "swr";
import { useCollections } from "./useCollections";
import { collectionEntryApi } from "../services/collectionEntryApi";
import { Collection } from "../services/collectionsApi";

export interface CollectionWithCount extends Collection {
  gameCount: number;
}

/**
 * Enhanced hook that fetches collections along with their game counts.
 * This combines the basic collections data with entry counts for each collection.
 */
export function useCollectionsWithCounts() {
  const {
    collections,
    isLoading: collectionsLoading,
    error: collectionsError,
    ...collectionMethods
  } = useCollections();

  // Create a fetcher that gets game counts for all collections
  const countsFetcher = async (): Promise<{ [key: number]: number }> => {
    if (!collections || collections.length === 0) {
      return {};
    }

    // Fetch entry counts for all collections in parallel
    const countPromises = collections.map(async (collection) => {
      try {
        const entries = await collectionEntryApi.getCollectionEntries(
          collection.id
        );
        return { id: collection.id, count: entries.length };
      } catch (error) {
        console.warn(
          `Failed to fetch entries for collection ${collection.id}:`,
          error
        );
        return { id: collection.id, count: 0 };
      }
    });

    const countResults = await Promise.all(countPromises);

    // Convert to a lookup object
    const countsLookup: { [key: number]: number } = {};
    countResults.forEach(({ id, count }) => {
      countsLookup[id] = count;
    });

    return countsLookup;
  };

  const {
    data: gameCounts = {},
    error: countsError,
    isLoading: countsLoading,
    mutate: mutateCounts,
  } = useSWR(
    collections.length > 0
      ? `/collections-counts-${collections.map((c) => c.id).join("-")}`
      : null,
    countsFetcher,
    {
      // Don't refetch on focus since counts don't change frequently
      revalidateOnFocus: false,
      // Cache for 5 minutes
      dedupingInterval: 5 * 60 * 1000,
    }
  );

  // Combine collections with their game counts
  const collectionsWithCounts: CollectionWithCount[] = collections.map(
    (collection) => ({
      ...collection,
      gameCount: gameCounts[collection.id] || 0,
    })
  );

  // Combined loading state - loading if either collections or counts are loading
  const isLoading =
    collectionsLoading || (collections.length > 0 && countsLoading);

  // Combined error state
  const error = collectionsError || countsError;

  // Function to refresh both collections and counts
  const refreshCollectionsWithCounts = () => {
    collectionMethods.refreshCollections();
    mutateCounts();
  };

  // Function to update count for a specific collection (useful after adding/removing entries)
  const updateCollectionCount = async (collectionId: number) => {
    try {
      const entries = await collectionEntryApi.getCollectionEntries(
        collectionId
      );
      const newCounts = { ...gameCounts, [collectionId]: entries.length };
      mutateCounts(newCounts, false);
    } catch (error) {
      console.warn(
        `Failed to update count for collection ${collectionId}:`,
        error
      );
    }
  };

  return {
    collections: collectionsWithCounts,
    isLoading,
    error,
    refreshCollectionsWithCounts,
    updateCollectionCount,
    hasCollections: collectionsWithCounts.length > 0,
    // Spread the collection methods (createCollection, deleteCollection, updateCollection, refreshCollections)
    createCollection: collectionMethods.createCollection,
    deleteCollection: collectionMethods.deleteCollection,
    updateCollection: collectionMethods.updateCollection,
    refreshCollections: collectionMethods.refreshCollections,
  };
}
