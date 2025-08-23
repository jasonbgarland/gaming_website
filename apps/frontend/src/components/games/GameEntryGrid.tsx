import React from "react";
import { CollectionEntry } from "@/services/collectionEntryApi";
import GameEntryCard from "./GameEntryCard";

interface GameEntryGridProps {
  entries: CollectionEntry[];
  onRemoveGame?: (entryId: number) => void;
}

const GameEntryGrid: React.FC<GameEntryGridProps> = ({
  entries,
  onRemoveGame,
}) => {
  // Handle empty state
  if (entries.length === 0) {
    return (
      <div className="text-center py-16 text-gamer-muted w-full flex flex-col items-center justify-center">
        <div className="mb-4">
          <svg
            className="mx-auto h-12 w-12 text-gamer-subtle-text"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M14 10l-2 1m0 0l-2-1m2 1v2.5M20 7l-2 1m2-1l-2-1m2 1v2.5M14 4l-2-1-2 1M4 7l2-1M4 7l2 1M4 7v2.5M12 21l-2-1m2 1l2-1m-2 1v-2.5M6 18l-2-1v-2.5M18 18l2-1v-2.5"
            />
          </svg>
        </div>
        <h3 className="text-lg font-medium text-gamer-text mb-2">
          No games yet!
        </h3>
        <p className="text-gamer-muted">
          Click &quot;Add Game&quot; to start building your collection.
        </p>
      </div>
    );
  }

  return (
    <div
      className="game-entry-grid"
      role="region"
      aria-label="Game entries grid"
    >
      {entries.map((entry) => (
        <GameEntryCard key={entry.id} entry={entry} onRemove={onRemoveGame} />
      ))}
    </div>
  );
};

export default GameEntryGrid;
