import React from "react";
import Image from "next/image";
import { CollectionEntry } from "services/collectionEntryApi";

interface GameEntryCardProps {
  entry: CollectionEntry;
  onRemove?: (entryId: number) => void;
}

const GameEntryCard: React.FC<GameEntryCardProps> = ({ entry, onRemove }) => {
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
      className="game-entry-card relative"
      style={{
        border: "1px solid #ccc",
        borderRadius: "8px",
        padding: "1rem",
        margin: "0.5rem",
        backgroundColor: "#f9f9f9",
      }}
    >
      {/* Remove button */}
      {onRemove && (
        <button
          onClick={() => onRemove(entry.id)}
          className="absolute top-2 right-2 bg-red-500 hover:bg-red-600 text-white w-6 h-6 rounded-full text-xs"
          title="Remove from collection"
        >
          ×
        </button>
      )}

      {/* Game image and title */}
      <div className="flex flex-col items-center mb-4">
        {entry.game.cover_url && (
          <Image
            src={entry.game.cover_url}
            alt={entry.game.name}
            width={120}
            height={160}
            className="object-cover rounded mb-3"
          />
        )}
        <h3 className="font-semibold text-lg text-center">{entry.game.name}</h3>
        {entry.game.platform && (
          <p className="text-sm text-gray-600">{entry.game.platform}</p>
        )}
      </div>

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
