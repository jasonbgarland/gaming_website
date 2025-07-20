"use client";

import { GameImage } from "./GameImage";
import { useGameSearch, type Game } from "./useGameSearch";

export type { Game };

export interface GameSearchProps {
  className?: string;
  initialResults?: Game[];
}

export function GameSearch({
  className = "",
  initialResults,
}: GameSearchProps) {
  const { query, setQuery, results, isLoading, error, hasQuery, hasResults } =
    useGameSearch({ initialResults });

  return (
    <div className={`w-full max-w-4xl ${className}`}>
      {/* Search Form */}
      <form className="mb-8" onSubmit={(e) => e.preventDefault()}>
        <div className="flex gap-4">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search for games..."
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
            autoFocus
          />
        </div>
      </form>

      {/* Error State */}
      {error && (
        <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
          {typeof error === "string" ? error : error.message}
        </div>
      )}

      {/* Loading State */}
      {isLoading && (
        <div className="text-center py-8">
          <div className="text-gray-600">Searching for games...</div>
        </div>
      )}

      {/* Results */}
      {!isLoading && hasResults && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {results.map((game) => (
            <div
              key={game.id}
              className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
            >
              <GameImage
                coverImages={game.cover_images}
                fallbackUrl={game.cover_url}
                alt={`${game.name} cover`}
                className="w-full h-48 object-cover rounded mb-4"
              />
              <h3 className="font-semibold text-lg mb-2">
                {game.name || "Unknown Title"}
              </h3>
              {game.release_year && (
                <p className="text-gray-600 mb-1">
                  Released: {game.release_year}
                </p>
              )}
              {game.platforms && game.platforms.length > 0 && (
                <p className="text-gray-600 text-sm">
                  Platforms: {game.platforms.join(", ")}
                </p>
              )}
            </div>
          ))}
        </div>
      )}

      {/* No Results */}
      {!isLoading && hasQuery && !hasResults && !error && (
        <div className="text-center py-8 text-gray-600">
          No games found for &quot;{query}&quot;. Try a different search term.
        </div>
      )}
    </div>
  );
}
export default GameSearch;
