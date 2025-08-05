import React from "react";
import { CollectionEntry } from "services/collectionEntryApi";
import GameEntryCard from "./GameEntryCard";

interface GameEntryGridProps {
  entries: CollectionEntry[];
}

const GameEntryGrid: React.FC<GameEntryGridProps> = ({ entries }) => {
  // Handle empty state
  if (entries.length === 0) {
    return (
      <div className="game-entry-grid">
        <p>No games in this collection.</p>
      </div>
    );
  }

  return (
    <div
      className="game-entry-grid"
      style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))",
        gap: "1rem",
        padding: "1rem 0",
      }}
    >
      {entries.map((entry) => (
        <GameEntryCard key={entry.id} entry={entry} />
      ))}
    </div>
  );
};

export default GameEntryGrid;
