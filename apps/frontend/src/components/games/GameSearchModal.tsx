"use client";

import React from "react";
import { useGameSearch } from "@/hooks/useGameSearch";
import { FilterDropdown, type FilterOption } from "@/components/filters/FilterDropdown";
import { YearRangeDropdown } from "@/components/filters/YearRangeDropdown";
import { FilterChips } from "@/components/filters/FilterChips";
import Image from "next/image";
import useSWR from "swr";

interface Game {
  id: number;
  name: string;
  cover_images?: {
    thumb?: string;
    small?: string;
    medium?: string;
    large?: string;
  };
  platforms?: string[];
  release_year?: number;
}

interface GameSearchModalProps {
  isOpen: boolean;
  onClose: () => void;
  onAddGame: (game: Game) => void;
  collectionName: string;
}

interface GenreOut {
  id: number;
  name: string;
}

interface PlatformOut {
  id: number;
  name: string;
}

const fetcher = (url: string) => fetch(url).then((r) => r.json());

const GameSearchModal: React.FC<GameSearchModalProps> = ({
  isOpen,
  onClose,
  onAddGame,
  collectionName,
}) => {
  const gameServiceUrl =
    process.env.NEXT_PUBLIC_GAME_SERVICE_URL || "http://localhost:8002";

  // Fetch filter options using SWR
  const { data: platformsData } = useSWR<PlatformOut[]>(
    `${gameServiceUrl}/igdb/platforms`,
    fetcher,
    {
      revalidateOnFocus: false,
      dedupingInterval: 604800000, // 7 days in ms
    }
  );

  const { data: genresData } = useSWR<GenreOut[]>(
    `${gameServiceUrl}/igdb/genres`,
    fetcher,
    {
      revalidateOnFocus: false,
      dedupingInterval: 604800000, // 7 days in ms
    }
  );

  const platformOptions: FilterOption[] =
    platformsData?.map((p) => ({ id: p.id, label: p.name })) || [];
  const genreOptions: FilterOption[] =
    genresData?.map((g) => ({ id: g.id, label: g.name })) || [];

  const {
    query,
    setQuery,
    filters,
    updateFilter,
    clearFilters,
    results,
    isLoading,
    error,
  } = useGameSearch();

  const handleAddGame = (game: Game) => {
    onAddGame(game);
    onClose();
    setQuery("");
  };

  const activeFilterCount =
    filters.platforms.length +
    filters.genres.length +
    (filters.yearStart ? 1 : 0);

  const handleRemoveFilter = (
    filterType: "platforms" | "genres" | "yearStart" | "yearEnd",
    value?: number
  ) => {
    if (filterType === "platforms" || filterType === "genres") {
      const currentValues = filters[filterType];
      const newValues = value
        ? currentValues.filter((v) => v !== value)
        : [];
      updateFilter(filterType, newValues);
    } else if (filterType === "yearStart") {
      updateFilter("yearStart", undefined);
      updateFilter("yearEnd", undefined);
    }
  };

  const handleYearRangeChange = (range: { yearStart?: number; yearEnd?: number }) => {
    updateFilter("yearStart", range.yearStart);
    updateFilter("yearEnd", range.yearEnd);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-gamer-surface rounded-lg p-6 w-full max-w-3xl max-h-[85vh] overflow-hidden border border-gamer-border">
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

        {/* Filters - compact layout for modal */}
        <div className="mb-4 flex flex-wrap gap-2">
          <FilterDropdown
            label="Platform"
            options={platformOptions}
            selected={filters.platforms}
            onChange={(selected) => updateFilter("platforms", selected)}
            className="flex-shrink-0"
          />
          <FilterDropdown
            label="Genre"
            options={genreOptions}
            selected={filters.genres}
            onChange={(selected) => updateFilter("genres", selected)}
            className="flex-shrink-0"
          />
          <YearRangeDropdown
            yearStart={filters.yearStart}
            yearEnd={filters.yearEnd}
            onChange={handleYearRangeChange}
            className="flex-shrink-0"
          />
        </div>

        {/* Active filter chips */}
        {activeFilterCount > 0 && (
          <div className="mb-4">
            <FilterChips
              filters={filters}
              labelMap={{
                platforms: Object.fromEntries(
                  platformOptions.map((p) => [p.id, p.label])
                ),
                genres: Object.fromEntries(
                  genreOptions.map((g) => [g.id, g.label])
                ),
              }}
              onRemoveFilter={handleRemoveFilter}
              onClearAll={clearFilters}
            />
          </div>
        )}

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
