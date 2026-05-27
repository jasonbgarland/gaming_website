import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { EnhancedGameSearch } from "../EnhancedGameSearch";
import { type FilterOption } from "@/components/filters/FilterDropdown";
import { DEFAULT_FILTERS } from "@/hooks/useEnhancedGameSearch";

// ─── Mock next/image ───────────────────────────────────────────────────────────
jest.mock("next/image", () => {
  const MockedImage = (props: React.ComponentProps<"img">) => (
    // eslint-disable-next-line @next/next/no-img-element
    <img {...props} alt={props.alt || "mocked image"} />
  );
  MockedImage.displayName = "MockedImage";
  return MockedImage;
});

// ─── Mock useEnhancedGameSearch ────────────────────────────────────────────────
// We control all state from outside so tests stay simple and deterministic.
const mockSetQuery = jest.fn();
const mockUpdateFilter = jest.fn();
const mockClearFilters = jest.fn();

const defaultHookReturn = {
  query: "",
  setQuery: mockSetQuery,
  filters: DEFAULT_FILTERS,
  updateFilter: mockUpdateFilter,
  clearFilters: mockClearFilters,
  results: [],
  isLoading: false,
  error: undefined,
  hasQuery: false,
  hasResults: false,
  activeFilterCount: 0,
};

jest.mock("@/hooks/useEnhancedGameSearch", () => ({
  ...jest.requireActual("@/hooks/useEnhancedGameSearch"),
  useEnhancedGameSearch: jest.fn(),
}));

import { useEnhancedGameSearch } from "@/hooks/useEnhancedGameSearch";

const mockUseEnhancedGameSearch = useEnhancedGameSearch as jest.Mock;

// ─── Shared props ──────────────────────────────────────────────────────────────
const platformOptions: FilterOption[] = [
  { id: 6, label: "PC (Windows)" },
  { id: 167, label: "PlayStation 5" },
];

const genreOptions: FilterOption[] = [
  { id: 4, label: "Action" },
  { id: 31, label: "RPG" },
];

function renderComponent(overrides = {}) {
  mockUseEnhancedGameSearch.mockReturnValue({
    ...defaultHookReturn,
    ...overrides,
  });
  return render(
    <EnhancedGameSearch
      platformOptions={platformOptions}
      genreOptions={genreOptions}
    />
  );
}

describe("EnhancedGameSearch", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  // ─── Search input ──────────────────────────────────────

  it("renders the search input", () => {
    renderComponent();
    expect(screen.getByPlaceholderText(/search for games/i)).toBeInTheDocument();
  });

  it("calls setQuery when user types in the search input", async () => {
    const user = userEvent.setup();
    renderComponent();
    await user.type(screen.getByPlaceholderText(/search for games/i), "z");
    expect(mockSetQuery).toHaveBeenCalled();
  });

  it("displays the current query value in the input", () => {
    renderComponent({ query: "halo" });
    expect(screen.getByDisplayValue("halo")).toBeInTheDocument();
  });

  // ─── Filter dropdowns ──────────────────────────────────

  it("renders the Platform filter dropdown", () => {
    renderComponent();
    expect(screen.getByRole("button", { name: /platform/i })).toBeInTheDocument();
  });

  it("renders the Genre filter dropdown", () => {
    renderComponent();
    expect(screen.getByRole("button", { name: /genre/i })).toBeInTheDocument();
  });

  it("renders the Year filter dropdown", () => {
    renderComponent();
    expect(screen.getByRole("button", { name: /^year/i })).toBeInTheDocument();
  });

  it("passes platformOptions to the Platform dropdown", async () => {
    const user = userEvent.setup();
    renderComponent();
    await user.click(screen.getByRole("button", { name: /platform/i }));
    expect(screen.getByText("PC (Windows)")).toBeInTheDocument();
    expect(screen.getByText("PlayStation 5")).toBeInTheDocument();
  });

  it("passes genreOptions to the Genre dropdown", async () => {
    const user = userEvent.setup();
    renderComponent();
    await user.click(screen.getByRole("button", { name: /genre/i }));
    expect(screen.getByText("Action")).toBeInTheDocument();
    expect(screen.getByText("RPG")).toBeInTheDocument();
  });

  // ─── Filter wiring ─────────────────────────────────────

  it("calls updateFilter('platforms', ...) when a platform is selected", async () => {
    const user = userEvent.setup();
    renderComponent();
    await user.click(screen.getByRole("button", { name: /platform/i }));
    await user.click(screen.getByText("PC (Windows)"));
    expect(mockUpdateFilter).toHaveBeenCalledWith("platforms", expect.arrayContaining([6]));
  });

  it("calls updateFilter('genres', ...) when a genre is selected", async () => {
    const user = userEvent.setup();
    renderComponent();
    await user.click(screen.getByRole("button", { name: /genre/i }));
    await user.click(screen.getByText("Action"));
    expect(mockUpdateFilter).toHaveBeenCalledWith("genres", expect.arrayContaining([4]));
  });

  it("calls updateFilter('yearStart', ...) when year From input changes", async () => {
    const user = userEvent.setup();
    renderComponent();
    await user.click(screen.getByRole("button", { name: /^year/i }));
    // Use fireEvent.change for number inputs — userEvent.type fires per-keystroke
    // which causes jsdom to emit each digit individually rather than the full value.
    fireEvent.change(screen.getByLabelText(/from/i), { target: { value: "2020" } });
    expect(mockUpdateFilter).toHaveBeenCalledWith("yearStart", 2020);
  });

  it("calls updateFilter('yearEnd', ...) when year To input changes", async () => {
    const user = userEvent.setup();
    renderComponent();
    await user.click(screen.getByRole("button", { name: /^year/i }));
    fireEvent.change(screen.getByLabelText(/to/i), { target: { value: "2023" } });
    expect(mockUpdateFilter).toHaveBeenCalledWith("yearEnd", 2023);
  });

  // ─── Filter chips ──────────────────────────────────────

  it("does not render FilterChips when no filters are active", () => {
    renderComponent({ activeFilterCount: 0 });
    // no chips visible — the "Clear All" button is a reliable sentinel
    expect(screen.queryByText(/clear all/i)).not.toBeInTheDocument();
  });

  it("renders FilterChips when filters are active", () => {
    renderComponent({
      filters: { ...DEFAULT_FILTERS, platforms: [6] },
      activeFilterCount: 1,
    });
    // FilterChips renders "Clear All" whenever chips are present
    expect(screen.getByText(/clear all/i)).toBeInTheDocument();
  });

  it("chip label uses platform option name", () => {
    renderComponent({
      filters: { ...DEFAULT_FILTERS, platforms: [6] },
      activeFilterCount: 1,
    });
    expect(screen.getByText("PC (Windows)")).toBeInTheDocument();
  });

  it("calls updateFilter to remove a chip when close button clicked", async () => {
    const user = userEvent.setup();
    renderComponent({
      filters: { ...DEFAULT_FILTERS, platforms: [6] },
      activeFilterCount: 1,
    });
    const chip = screen.getByText("PC (Windows)").closest("[data-chip]")!;
    const closeBtn = chip.querySelector("[data-close]")!;
    await user.click(closeBtn);
    expect(mockUpdateFilter).toHaveBeenCalledWith("platforms", []);
  });

  it("calls clearFilters when Clear All is clicked", async () => {
    const user = userEvent.setup();
    renderComponent({
      filters: { ...DEFAULT_FILTERS, platforms: [6], genres: [4] },
      activeFilterCount: 2,
    });
    await user.click(screen.getByText(/clear all/i));
    expect(mockClearFilters).toHaveBeenCalledTimes(1);
  });

  // ─── Status states ─────────────────────────────────────

  it("shows loading state while searching", () => {
    renderComponent({ isLoading: true, hasQuery: true });
    expect(screen.getByText(/searching for games/i)).toBeInTheDocument();
  });

  it("shows error message when search fails", () => {
    renderComponent({ error: new Error("Network error!"), hasQuery: true });
    expect(screen.getByText(/network error/i)).toBeInTheDocument();
  });

  it("shows no-results message when query has no matches", () => {
    renderComponent({ query: "xyzzy", hasQuery: true, hasResults: false });
    expect(screen.getByText(/no games found/i)).toBeInTheDocument();
    expect(screen.getByText(/xyzzy/i)).toBeInTheDocument();
  });

  it("shows prompt message when no query is entered", () => {
    renderComponent({ hasQuery: false, hasResults: false });
    expect(screen.getByText(/search or filter/i)).toBeInTheDocument();
  });

  // ─── Results grid ──────────────────────────────────────

  it("renders result cards when results are present", () => {
    renderComponent({
      hasQuery: true,
      hasResults: true,
      results: [
        { id: 1, name: "Halo", release_year: 2001, platforms: ["Xbox"], cover_url: "" },
        { id: 2, name: "Zelda", release_year: 2023, platforms: ["Switch"], cover_url: "" },
      ],
    });
    expect(screen.getByText("Halo")).toBeInTheDocument();
    expect(screen.getByText("Zelda")).toBeInTheDocument();
  });

  it("renders release year and platforms in result card", () => {
    renderComponent({
      hasQuery: true,
      hasResults: true,
      results: [
        { id: 1, name: "Halo", release_year: 2001, platforms: ["Xbox"], cover_url: "" },
      ],
    });
    expect(screen.getByText(/2001/)).toBeInTheDocument();
    expect(screen.getByText(/xbox/i)).toBeInTheDocument();
  });

  it("renders 'Unknown Title' for a game with no name", () => {
    renderComponent({
      hasQuery: true,
      hasResults: true,
      results: [{ id: 99, name: "", platforms: [] }],
    });
    expect(screen.getByText("Unknown Title")).toBeInTheDocument();
  });

  it("does not render results while loading", () => {
    renderComponent({
      isLoading: true,
      hasQuery: true,
      hasResults: true,
      results: [{ id: 1, name: "Should Not Appear", platforms: [] }],
    });
    expect(screen.queryByText("Should Not Appear")).not.toBeInTheDocument();
  });

  // ─── Active filter count badge ─────────────────────────

  it("shows active filter count badge when filters are active", () => {
    renderComponent({ activeFilterCount: 2 });
    expect(screen.getByText("2 active filter(s)")).toBeInTheDocument();
  });

  it("does not show active filter count badge when no filters active", () => {
    renderComponent({ activeFilterCount: 0 });
    expect(screen.queryByText(/active filter/i)).not.toBeInTheDocument();
  });
});
