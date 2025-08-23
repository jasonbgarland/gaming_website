import React from "react";
import Image from "next/image";
import { CollectionEntry } from "@/services/collectionEntryApi";

interface GameEntryCardProps {
  entry: CollectionEntry;
  onRemove?: (entryId: number) => void;
}

const GameEntryCard: React.FC<GameEntryCardProps> = ({ entry, onRemove }) => {
  // Helper function to format tags
  const formatTags = (tags?: Record<string, string>) => {
    if (!tags) return null;
    return Object.entries(tags).map(([key, value]) => (
      <span
        key={key}
        className="inline-block bg-gamer-primary text-white text-xs px-2 py-1 rounded-full"
      >
        {value}
      </span>
    ));
  };

  return (
    <div className="relative border border-gamer-border rounded-lg p-4 m-2 bg-gamer-surface hover:bg-gamer-elevated transition-all duration-200 hover:scale-[1.02] hover:shadow-lg">
      {/* Remove button */}
      {onRemove && (
        <button
          onClick={() => onRemove(entry.id)}
          className="group absolute top-2 right-2 bg-gamer-surface hover:bg-gamer-danger text-gamer-danger hover:text-white w-8 h-8 rounded-full flex items-center justify-center transition-colors border border-gamer-danger hover:border-gamer-danger"
          aria-label="Remove from collection"
        >
          <svg
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            className="w-4 h-4"
          >
            <path
              d="M10 12V17"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <path
              d="M14 12V17"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <path
              d="M4 7H20"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <path
              d="M6 10V18C6 19.6569 7.34315 21 9 21H15C16.6569 21 18 19.6569 18 18V10"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <path
              d="M9 5C9 3.89543 9.89543 3 11 3H13C14.1046 3 15 3.89543 15 5V7H9V5Z"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          {/* Custom tooltip */}
          <span className="absolute bottom-full right-0 mb-2 px-2 py-1 text-xs bg-gamer-elevated text-gamer-text rounded border border-gamer-border opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap z-10">
            Remove from collection
          </span>
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
        <h3 className="font-semibold text-lg text-center text-gamer-text">
          {entry.game.name}
        </h3>
        {entry.game.platform && (
          <p className="text-sm text-gamer-muted">{entry.game.platform}</p>
        )}
      </div>

      {/* User's notes */}
      {entry.notes && <p className="text-gamer-text mb-2">{entry.notes}</p>}

      {/* Status */}
      {entry.status && (
        <div className="mb-2 text-gamer-text">
          <span className="font-medium text-gamer-primary">Status:</span>{" "}
          {entry.status}
        </div>
      )}

      {/* Rating */}
      {entry.rating && (
        <div className="mb-2 text-gamer-text">
          <span className="font-medium text-gamer-primary">Rating:</span>{" "}
          {entry.rating}/10
        </div>
      )}

      {/* Custom tags */}
      {entry.custom_tags && (
        <div className="mb-2">
          <span className="font-medium text-gamer-primary">Tags:</span>
          <div className="flex flex-wrap gap-1 mt-1">
            {formatTags(entry.custom_tags)}
          </div>
        </div>
      )}

      {/* Date added */}
      {entry.added_at && (
        <div className="text-xs text-gamer-muted">
          Added: {new Date(entry.added_at).toLocaleDateString()}
        </div>
      )}
    </div>
  );
};

export default GameEntryCard;
