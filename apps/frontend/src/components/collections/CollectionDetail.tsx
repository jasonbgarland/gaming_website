"use client";

import React from "react";
import { Collection } from "../../services/collectionsApi";
import { useCollectionEntries } from "hooks/useCollectionEntries";
import GameEntryGrid from "components/games/GameEntryGrid";

interface CollectionDetailProps {
  collection: Collection;
  // isLoading?: boolean;
  // error?: string;
  // onAddGame?: (gameData: { [key: string]: unknown }) => void; // Use a safer type or define GameInput
  // onRemoveGame?: (gameId: number) => void;
  // onDeleteCollection?: () => void;
}

const CollectionDetail: React.FC<CollectionDetailProps> = ({
  collection,
  // isLoading,
  // error,
  // onAddGame,
  // onRemoveGame,
  // onDeleteCollection,
}) => {
  // Load collection entries using the custom hook
  const {
    entries,
    isLoading: entriesIsLoading,
    error: entriesError,
  } = useCollectionEntries(collection.id);

  // Helper function for rendering entries block
  function renderEntries() {
    if (entriesIsLoading) return <p>Loading entries...</p>;
    if (entriesError) return <p>Error loading entries.</p>;
    // GameEntryGrid handles empty state internally
    return <GameEntryGrid entries={entries} />;
  }

  return (
    <div>
      <h1>{collection.name}</h1>
      <p>{collection.description}</p>
      {renderEntries()}
    </div>
  );
};

export default CollectionDetail;
