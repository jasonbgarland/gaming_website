import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { FilterChips } from "../FilterChips";
import { DEFAULT_FILTERS, type SearchFilters } from "@/hooks/useGameSearch";

// We need label lookups to show "Platform: PS5" etc.
// The component receives a labelMap prop that maps filter types + IDs to display names
const mockLabelMap = {
  platforms: { 6: "PC (Windows)", 48: "PlayStation 4", 130: "Nintendo Switch", 167: "PlayStation 5" },
  genres: { 4: "Action", 12: "Shooter", 31: "RPG" },
  themes: { 18: "Sci-fi", 19: "Horror" },
  playerPerspectives: { 1: "First Person", 3: "Third Person" },
};

describe("FilterChips", () => {
  const mockOnRemoveFilter = jest.fn();
  const mockOnClearAll = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  // ─── Hidden when no filters ────────────────────────────
  it("renders nothing when no filters are active", () => {
    const { container } = render(
      <FilterChips
        filters={DEFAULT_FILTERS}
        labelMap={mockLabelMap}
        onRemoveFilter={mockOnRemoveFilter}
        onClearAll={mockOnClearAll}
      />
    );
    expect(container.innerHTML).toBe("");
  });

  // ─── Chip rendering ────────────────────────────────────
  it("renders chips for selected platforms", () => {
    const filters: SearchFilters = {
      ...DEFAULT_FILTERS,
      platforms: [6, 130],
    };
    render(
      <FilterChips
        filters={filters}
        labelMap={mockLabelMap}
        onRemoveFilter={mockOnRemoveFilter}
        onClearAll={mockOnClearAll}
      />
    );
    expect(screen.getByText("PC (Windows)")).toBeInTheDocument();
    expect(screen.getByText("Nintendo Switch")).toBeInTheDocument();
  });

  it("renders chips for selected genres", () => {
    const filters: SearchFilters = {
      ...DEFAULT_FILTERS,
      genres: [4, 31],
    };
    render(
      <FilterChips
        filters={filters}
        labelMap={mockLabelMap}
        onRemoveFilter={mockOnRemoveFilter}
        onClearAll={mockOnClearAll}
      />
    );
    expect(screen.getByText("Action")).toBeInTheDocument();
    expect(screen.getByText("RPG")).toBeInTheDocument();
  });

  it("renders chips for min/max rating", () => {
    const filters: SearchFilters = {
      ...DEFAULT_FILTERS,
      minRating: 70,
      maxRating: 90,
    };
    render(
      <FilterChips
        filters={filters}
        labelMap={mockLabelMap}
        onRemoveFilter={mockOnRemoveFilter}
        onClearAll={mockOnClearAll}
      />
    );
    expect(screen.getByText(/min.*70/i)).toBeInTheDocument();
    expect(screen.getByText(/max.*90/i)).toBeInTheDocument();
  });

  it("renders chips for year range", () => {
    const filters: SearchFilters = {
      ...DEFAULT_FILTERS,
      yearStart: 2020,
      yearEnd: 2023,
    };
    render(
      <FilterChips
        filters={filters}
        labelMap={mockLabelMap}
        onRemoveFilter={mockOnRemoveFilter}
        onClearAll={mockOnClearAll}
      />
    );
    expect(screen.getByText(/2020.*2023/i)).toBeInTheDocument();
  });

  it("renders chips for themes and perspectives", () => {
    const filters: SearchFilters = {
      ...DEFAULT_FILTERS,
      themes: [18],
      playerPerspectives: [1],
    };
    render(
      <FilterChips
        filters={filters}
        labelMap={mockLabelMap}
        onRemoveFilter={mockOnRemoveFilter}
        onClearAll={mockOnClearAll}
      />
    );
    expect(screen.getByText("Sci-fi")).toBeInTheDocument();
    expect(screen.getByText("First Person")).toBeInTheDocument();
  });

  // ─── Chip removal ──────────────────────────────────────
  it("calls onRemoveFilter when chip close button is clicked", async () => {
    const user = userEvent.setup();
    const filters: SearchFilters = {
      ...DEFAULT_FILTERS,
      platforms: [6, 130],
    };
    render(
      <FilterChips
        filters={filters}
        labelMap={mockLabelMap}
        onRemoveFilter={mockOnRemoveFilter}
        onClearAll={mockOnClearAll}
      />
    );
    // Find the close button on the "PC (Windows)" chip
    const pcChip = screen.getByText("PC (Windows)").closest("[data-chip]")!;
    const closeButton = pcChip.querySelector("[data-close]")!;
    await user.click(closeButton);
    expect(mockOnRemoveFilter).toHaveBeenCalledWith("platforms", 6);
  });

  // ─── Clear All button ──────────────────────────────────
  it("shows Clear All button when filters are active", () => {
    const filters: SearchFilters = {
      ...DEFAULT_FILTERS,
      platforms: [6],
    };
    render(
      <FilterChips
        filters={filters}
        labelMap={mockLabelMap}
        onRemoveFilter={mockOnRemoveFilter}
        onClearAll={mockOnClearAll}
      />
    );
    expect(screen.getByText(/clear all/i)).toBeInTheDocument();
  });

  it("does not show Clear All when no filters active", () => {
    render(
      <FilterChips
        filters={DEFAULT_FILTERS}
        labelMap={mockLabelMap}
        onRemoveFilter={mockOnRemoveFilter}
        onClearAll={mockOnClearAll}
      />
    );
    expect(screen.queryByText(/clear all/i)).not.toBeInTheDocument();
  });

  it("calls onClearAll when Clear All button is clicked", async () => {
    const user = userEvent.setup();
    const filters: SearchFilters = {
      ...DEFAULT_FILTERS,
      platforms: [6],
      genres: [4],
    };
    render(
      <FilterChips
        filters={filters}
        labelMap={mockLabelMap}
        onRemoveFilter={mockOnRemoveFilter}
        onClearAll={mockOnClearAll}
      />
    );
    await user.click(screen.getByText(/clear all/i));
    expect(mockOnClearAll).toHaveBeenCalledTimes(1);
  });
});