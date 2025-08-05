import React from "react";
import { CollectionEntry } from "services/collectionEntryApi";

interface GameEntryCardProps {
  entry: CollectionEntry;
}

const GameEntryCard: React.FC<GameEntryCardProps> = ({ entry }) => {
  // Helper function to format tags
  const formatTags = (tags?: Record<string, string>) => {
    if (!tags) return null;
    return Object.entries(tags).map(([key, value]) => (
      <span key={key} className="tag">
        {value}
      </span>
    ));
  };

  return (
    <div
      className="game-entry-card"
      style={{
        border: "1px solid #ccc",
        borderRadius: "8px",
        padding: "1rem",
        margin: "0.5rem",
        backgroundColor: "#f9f9f9",
      }}
    >
      {/* Game ID (temporary until we have game lookup) */}
      <h3>Game ID: {entry.game_id}</h3>

      {/* User's notes */}
      {entry.notes && <p>{entry.notes}</p>}

      {/* Status */}
      {entry.status && (
        <div>
          <strong>Status:</strong> {entry.status}
        </div>
      )}

      {/* Rating */}
      {entry.rating && (
        <div>
          <strong>Rating:</strong> {entry.rating}/10
        </div>
      )}

      {/* Custom tags */}
      {entry.custom_tags && (
        <div>
          <strong>Tags:</strong> {formatTags(entry.custom_tags)}
        </div>
      )}

      {/* Date added */}
      {entry.added_at && (
        <div>
          <small>Added: {new Date(entry.added_at).toLocaleDateString()}</small>
        </div>
      )}
    </div>
  );
};

export default GameEntryCard;
