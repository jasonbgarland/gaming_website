"use client";

import React, { useState } from "react";
import { Collection } from "../../services/collectionsApi";
import { useCollectionEntries } from "hooks/useCollectionEntries";
import GameEntryGrid from "components/games/GameEntryGrid";
import GameSearchModal from "components/games/GameSearchModal";
import { Game } from "../../hooks/useGameSearch";

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
  const [showAddGameModal, setShowAddGameModal] = useState(false);

  // Load collection entries using the custom hook
  const {
    entries,
    isLoading: entriesIsLoading,
    error: entriesError,
    addEntry,
    removeEntry,
  } = useCollectionEntries(collection.id);

  const handleAddGame = async (game: Game) => {
    try {
      await addEntry({
        game_id: game.id,
        // Don't set default notes or status - let users add these later if desired
      });
    } catch (error) {
      console.error("Failed to add game to collection:", error);
      // TODO: Show error toast/notification
    }
  };

  const handleRemoveGame = async (entryId: number) => {
    try {
      await removeEntry(entryId);
    } catch (error) {
      console.error("Failed to remove game from collection:", error);
      // TODO: Show error toast/notification
    }
  };

  // Helper function for rendering entries block
  function renderEntries() {
    if (entriesIsLoading) return <p>Loading entries...</p>;
    if (entriesError) return <p>Error loading entries.</p>;
    // GameEntryGrid handles empty state internally
    return <GameEntryGrid entries={entries} onRemoveGame={handleRemoveGame} />;
  }

  return (
    <div className="space-y-6">
      {/* Header with collection info and actions */}
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold">{collection.name}</h1>
          <p className="text-gray-600 mt-2">{collection.description}</p>
        </div>
        <div className="space-x-2">
          <button
            onClick={() => setShowAddGameModal(true)}
            className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded"
          >
            Add Game
          </button>
        </div>
      </div>

      {/* Games in collection */}
      <div>
        <h2 className="text-xl font-semibold mb-4">
          Games ({entries?.length || 0})
        </h2>
        {renderEntries()}
      </div>

      {/* Add Game Modal */}
      <GameSearchModal
        isOpen={showAddGameModal}
        onClose={() => setShowAddGameModal(false)}
        onAddGame={handleAddGame}
        collectionName={collection.name}
      />
    </div>
  );
};

export default CollectionDetail;
