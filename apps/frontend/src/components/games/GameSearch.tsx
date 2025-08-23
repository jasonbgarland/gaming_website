"use client";

import { GameImage } from "./GameImage";
import { useGameSearch, type Game } from "@/hooks/useGameSearch";

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
            className="flex-1 px-4 py-2 border border-gamer-input-border rounded-lg bg-gamer-input text-gamer-text focus:outline-none focus:ring-2 focus:ring-gamer-primary transition-all"
            disabled={isLoading}
            autoFocus
          />
        </div>
      </form>

      {/* Error State */}
      {error && (
        <div className="mb-4 p-4 border border-danger rounded-lg bg-danger text-danger-foreground">
          {typeof error === "string" ? error : error.message}
        </div>
      )}

      {/* Loading State */}
      {isLoading && (
        <div className="text-center py-8">
          <div className="text-gamer-muted">Searching for games...</div>
        </div>
      )}

      {/* Results */}
      {!isLoading && hasResults && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {results.map((game) => (
            <div
              key={game.id}
              className="border border-gamer-border rounded-lg p-4 bg-gamer-surface transition-all duration-200 hover:scale-[1.02] hover:shadow-lg"
            >
              <GameImage
                coverImages={game.cover_images}
                fallbackUrl={game.cover_url}
                alt={`${game.name} cover`}
                className="w-full h-48 object-cover rounded mb-4"
              />
              <h3 className="font-semibold text-lg mb-2 text-gamer-text">
                {game.name || "Unknown Title"}
              </h3>
              {game.release_year && (
                <p className="mb-1 text-gamer-muted">
                  Released: {game.release_year}
                </p>
              )}
              {game.platforms && game.platforms.length > 0 && (
                <p className="text-sm text-gamer-muted">
                  Platforms: {game.platforms.join(", ")}
                </p>
              )}
            </div>
          ))}
        </div>
      )}

      {/* No Results */}
      {!isLoading && hasQuery && !hasResults && !error && (
        <div className="text-center py-8 text-gamer-muted">
          No games found for &quot;{query}&quot;. Try a different search term.
        </div>
      )}
    </div>
  );
}
export default GameSearch;
