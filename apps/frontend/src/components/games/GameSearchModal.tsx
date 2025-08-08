"use client";

import React from "react";
import { useGameSearch, Game } from "components/useGameSearch";
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
      <div className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[80vh] overflow-hidden">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold">
            Add Game to &ldquo;{collectionName}&rdquo;
          </h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700"
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
            className="w-full px-3 py-2 border border-gray-300 rounded"
          />
        </div>

        {/* Search results */}
        <div className="overflow-y-auto max-h-96">
          {error && (
            <div className="text-red-500 text-center py-4">Error: {error}</div>
          )}

          {results.length === 0 && !isLoading && !error && query.trim() && (
            <div className="text-gray-500 text-center py-8">
              No games found for &ldquo;{query}&rdquo;
            </div>
          )}

          {results.length === 0 && !isLoading && !error && !query.trim() && (
            <div className="text-gray-500 text-center py-8">
              Search for games to add to your collection
            </div>
          )}

          {isLoading && <div className="text-center py-8">Searching...</div>}

          <div className="space-y-2">
            {results.map((game: Game) => (
              <div
                key={game.id}
                className="flex items-center justify-between p-3 border border-gray-200 rounded hover:bg-gray-50"
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
                    <h3 className="font-medium">{game.name}</h3>
                    {game.platforms && (
                      <p className="text-sm text-gray-500">
                        {game.platforms.slice(0, 3).join(", ")}
                      </p>
                    )}
                    {game.release_year && (
                      <p className="text-sm text-gray-500">
                        {game.release_year}
                      </p>
                    )}
                  </div>
                </div>
                <button
                  onClick={() => handleAddGame(game)}
                  className="bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded text-sm"
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
