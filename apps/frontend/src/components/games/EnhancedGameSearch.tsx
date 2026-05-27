"use client";

import React from "react";
import { useEnhancedGameSearch, type SearchFilters } from "@/hooks/useEnhancedGameSearch";
import { FilterDropdown, type FilterOption } from "@/components/filters/FilterDropdown";
import { FilterChips, type FilterLabelMap } from "@/components/filters/FilterChips";
import { YearRangeDropdown } from "@/components/filters/YearRangeDropdown";
import { GameImage } from "./GameImage";
import { type Game } from "./GameSearch";

export interface EnhancedGameSearchProps {
  platformOptions: FilterOption[];
  genreOptions: FilterOption[];
  className?: string;
}

/**
 * Enhanced game search with Platform, Genre, and Year range filters.
 * Uses useEnhancedGameSearch for state management and SWR-backed API calls.
 * Filter options (platformOptions, genreOptions) are passed as props so
 * the parent can fetch them from the API independently (task 2).
 */
export function EnhancedGameSearch({
  platformOptions,
  genreOptions,
  className = "",
}: EnhancedGameSearchProps) {
  const {
    query,
    setQuery,
    filters,
    updateFilter,
    clearFilters,
    results,
    isLoading,
    error,
    hasQuery,
    hasResults,
    activeFilterCount,
  } = useEnhancedGameSearch();

  // Build label map for FilterChips from the options passed as props
  const labelMap: FilterLabelMap = {
    platforms: Object.fromEntries(platformOptions.map((o) => [o.id, o.label])),
    genres: Object.fromEntries(genreOptions.map((o) => [o.id, o.label])),
  };

  /**
   * Handle chip removal. For array-based filters (platforms, genres),
   * remove the specific ID. For scalar filters (yearStart, yearEnd, ratings),
   * clear the value entirely.
   * Note: FilterChips calls onRemoveFilter twice for year range (yearStart + yearEnd).
   */
  function handleRemoveFilter(
    filterType: keyof SearchFilters,
    value: number | undefined
  ) {
    const current = filters[filterType];
    if (Array.isArray(current) && value !== undefined) {
      updateFilter(filterType, (current as number[]).filter((id) => id !== value) as SearchFilters[typeof filterType]);
    } else {
      updateFilter(filterType, undefined as SearchFilters[typeof filterType]);
    }
  }

  return (
    <div className={`w-full max-w-4xl ${className}`}>
      {/* Search input */}
      <form className="mb-6" onSubmit={(e) => e.preventDefault()}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search for games..."
          className="w-full px-4 py-2 border border-gamer-input-border rounded-lg bg-gamer-input text-gamer-text focus:outline-none focus:ring-2 focus:ring-gamer-primary transition-all"
          disabled={isLoading}
          autoFocus
        />
      </form>

      {/* Filter row */}
      <div className="mb-4">
        <div className="flex flex-wrap gap-3 items-center">
          <FilterDropdown
            label="Platform"
            options={platformOptions}
            selected={filters.platforms}
            onChange={(selected) => updateFilter("platforms", selected)}
          />
          <FilterDropdown
            label="Genre"
            options={genreOptions}
            selected={filters.genres}
            onChange={(selected) => updateFilter("genres", selected)}
          />
          <YearRangeDropdown
            yearStart={filters.yearStart}
            yearEnd={filters.yearEnd}
            onChange={({ yearStart, yearEnd }) => {
              updateFilter("yearStart", yearStart);
              updateFilter("yearEnd", yearEnd);
            }}
          />
          {activeFilterCount > 0 && (
            <span className="text-sm text-gamer-muted">
              {activeFilterCount} active filter(s)
            </span>
          )}
        </div>
      </div>

      {/* Active filter chips */}
      {activeFilterCount > 0 && (
        <div className="mb-6">
          <FilterChips
            filters={filters}
            labelMap={labelMap}
            onRemoveFilter={handleRemoveFilter}
            onClearAll={clearFilters}
          />
        </div>
      )}

      {/* Error state */}
      {error && (
        <div className="mb-4 p-4 border border-danger rounded-lg bg-danger text-danger-foreground">
          {typeof error === "string" ? error : (error as Error).message}
        </div>
      )}

      {/* Loading state */}
      {isLoading && (
        <div className="text-center py-8 text-gamer-muted">
          Searching for games...
        </div>
      )}

      {/* Results grid */}
      {!isLoading && hasResults && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {results.map((game: Game) => (
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

      {/* No results state */}
      {!isLoading && hasQuery && !hasResults && !error && (
        <div className="text-center py-8 text-gamer-muted">
          No games found for &quot;{query}&quot;. Try a different search term.
        </div>
      )}

      {/* Empty/prompt state */}
      {!isLoading && !hasQuery && !hasResults && !error && (
        <div className="text-center py-8 text-gamer-muted">
          Search or filter to find games.
        </div>
      )}
    </div>
  );
}

export default EnhancedGameSearch;
