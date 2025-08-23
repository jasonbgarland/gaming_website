"use client";

import React from "react";
import { useGameSearch, Game } from "@/hooks/useGameSearch";
import Image from "next/image";

interface GameSearchModalProps {
  isOpen: boolean;
  onClose: () => void;
  onAddGame: (game: Game) => void;
  collectionName: string;
}

const GameSearchModal: React.FC<GameSearchModalProps> = ({
  isOpen,
  onClose,
  onAddGame,
  collectionName,
}) => {
  const { query, setQuery, results, isLoading, error } = useGameSearch();

  const handleAddGame = (game: Game) => {
    onAddGame(game);
    onClose();
    setQuery("");
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-gamer-surface rounded-lg p-6 w-full max-w-2xl max-h-[80vh] overflow-hidden border border-gamer-border">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold text-gamer-text">
            Add Game to &ldquo;{collectionName}&rdquo;
          </h2>
          <button
            onClick={onClose}
            className="text-gamer-muted hover:text-gamer-text transition-colors"
          >
            ✕
          </button>
        </div>

        {/* Search form */}
        <div className="mb-4">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search for games..."
            className="w-full px-3 py-2 border border-gamer-input-border rounded bg-gamer-input text-gamer-text placeholder-gamer-muted focus:ring-gamer-primary focus:border-gamer-primary"
          />
        </div>

        {/* Search results */}
        <div className="overflow-y-auto max-h-96">
          {error && (
            <div className="text-gamer-danger text-center py-4">
              Error: {error}
            </div>
          )}

          {results.length === 0 && !isLoading && !error && query.trim() && (
            <div className="text-gamer-muted text-center py-8">
              No games found for &ldquo;{query}&rdquo;
            </div>
          )}

          {results.length === 0 && !isLoading && !error && !query.trim() && (
            <div className="text-gamer-muted text-center py-8">
              Search for games to add to your collection
            </div>
          )}

          {isLoading && (
            <div className="text-gamer-text text-center py-8">Searching...</div>
          )}

          <div className="space-y-2">
            {results.map((game: Game) => (
              <div
                key={game.id}
                className="flex items-center justify-between p-3 border border-gamer-border rounded bg-gamer-elevated hover:bg-gamer-subtle transition-colors"
              >
                <div className="flex items-center space-x-3">
                  {game.cover_images?.small && (
                    <Image
                      src={game.cover_images.small}
                      alt={game.name}
                      width={48}
                      height={64}
                      className="object-cover rounded"
                    />
                  )}
                  <div>
                    <h3 className="font-medium text-gamer-text">{game.name}</h3>
                    {game.platforms && (
                      <p className="text-sm text-gamer-muted">
                        {game.platforms.slice(0, 3).join(", ")}
                      </p>
                    )}
                    {game.release_year && (
                      <p className="text-sm text-gamer-muted">
                        {game.release_year}
                      </p>
                    )}
                  </div>
                </div>
                <button
                  onClick={() => handleAddGame(game)}
                  className="bg-gamer-success hover:bg-green-600 text-white px-3 py-1 rounded text-sm transition-colors"
                >
                  Add
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default GameSearchModal;
