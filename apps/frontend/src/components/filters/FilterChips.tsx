"use client";

import React from "react";
import { type SearchFilters } from "@/hooks/useEnhancedGameSearch";

/**
 * Label map provides human-readable names for filter IDs.
 * Populated from the IGDB API (platforms, genres, themes, perspectives).
 * Ratings and year ranges are formatted directly.
 */
export interface FilterLabelMap {
  platforms?: Record<number, string>;
  genres?: Record<number, string>;
  themes?: Record<number, string>;
  playerPerspectives?: Record<number, string>;
}

export interface FilterChipsProps {
  filters: SearchFilters;
  labelMap: FilterLabelMap;
  onRemoveFilter: (filterType: keyof SearchFilters, value: number | undefined) => void;
  onClearAll: () => void;
}

/**
 * Displays active filter selections as removable chip/pill elements.
 * Each chip shows the filter category and value, with an × button to remove it.
 * Includes a "Clear All" button when multiple filters are active.
 */
export function FilterChips({
  filters,
  labelMap,
  onRemoveFilter,
  onClearAll,
}: FilterChipsProps) {
  // Build the list of chips to display
  const chips: { key: string; label: string; filterType: keyof SearchFilters; value: number | undefined }[] = [];

  // Platform chips
  filters.platforms.forEach((id) => {
    const name = labelMap.platforms?.[id] || `Platform #${id}`;
    chips.push({ key: `platform-${id}`, label: name, filterType: "platforms", value: id });
  });

  // Genre chips
  filters.genres.forEach((id) => {
    const name = labelMap.genres?.[id] || `Genre #${id}`;
    chips.push({ key: `genre-${id}`, label: name, filterType: "genres", value: id });
  });

  // Year range chip (treated as one logical filter)
  if (filters.yearStart !== undefined || filters.yearEnd !== undefined) {
    const start = filters.yearStart ?? "?";
    const end = filters.yearEnd ?? "?";
    chips.push({
      key: "year-range",
      label: `${start}–${end}`,
      filterType: "yearStart", // removing clears both yearStart and yearEnd
      value: undefined, // special: clears the whole range
    });
  }

  // Min rating chip
  if (filters.minRating !== undefined) {
    chips.push({
      key: "min-rating",
      label: `Min ★ ${filters.minRating}`,
      filterType: "minRating",
      value: undefined,
    });
  }

  // Max rating chip
  if (filters.maxRating !== undefined) {
    chips.push({
      key: "max-rating",
      label: `Max ★ ${filters.maxRating}`,
      filterType: "maxRating",
      value: undefined,
    });
  }

  // Theme chips
  filters.themes.forEach((id) => {
    const name = labelMap.themes?.[id] || `Theme #${id}`;
    chips.push({ key: `theme-${id}`, label: name, filterType: "themes", value: id });
  });

  // Player perspective chips
  filters.playerPerspectives.forEach((id) => {
    const name = labelMap.playerPerspectives?.[id] || `Perspective #${id}`;
    chips.push({ key: `perspective-${id}`, label: name, filterType: "playerPerspectives", value: id });
  });

  // Nothing to show
  if (chips.length === 0) {
    return null;
  }

  function handleRemove(chip: typeof chips[0]) {
    // Year range: clear both start and end
    if (chip.filterType === "yearStart") {
      onRemoveFilter("yearStart", undefined);
      onRemoveFilter("yearEnd", undefined);
    } else {
      onRemoveFilter(chip.filterType, chip.value);
    }
  }

  return (
    <div className="flex flex-wrap gap-2 items-center">
      {chips.map((chip) => (
        <div
          key={chip.key}
          data-chip
          className="flex items-center gap-2 px-3 py-1 bg-gamer-primary-light border border-gamer-primary/30 rounded-full text-sm text-gamer-text"
        >
          <span>{chip.label}</span>
          <button
            data-close
            onClick={() => handleRemove(chip)}
            className="w-4 h-4 flex items-center justify-center rounded-full hover:bg-gamer-primary/30 transition-colors text-gamer-muted hover:text-gamer-text"
            aria-label={`Remove ${chip.label} filter`}
          >
            ×
          </button>
        </div>
      ))}
      {chips.length > 0 && (
        <button
          onClick={onClearAll}
          className="px-3 py-1 text-sm text-gamer-muted hover:text-gamer-text transition-colors underline"
        >
          Clear All
        </button>
      )}
    </div>
  );
}