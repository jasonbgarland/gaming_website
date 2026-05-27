import { renderHook, act } from "@testing-library/react";
import useSWR from "swr";
import { useEnhancedGameSearch, buildFilterParams, type SearchFilters, DEFAULT_FILTERS } from "../useEnhancedGameSearch";

// Mock dependencies
jest.mock("swr");
jest.mock("../useDebounce", () => ({
  useDebounce: (value: string, _delay: number) => value, // skip debounce in tests
}));

const mockGames = [
  {
    id: 1,
    name: "Zelda",
    cover_url: "https://mock.url/cover1.jpg",
    platforms: ["Switch"],
    release_year: 2023,
  },
  {
    id: 2,
    name: "Halo",
    cover_url: "https://mock.url/cover2.jpg",
    platforms: ["Xbox"],
    release_year: 2021,
  },
];

// Helper to set up SWR mock with default return values
function mockSWRReturn(data = mockGames, error = undefined, isLoading = false) {
  (useSWR as jest.Mock).mockReturnValue({
    data,
    error,
    isLoading,
    mutate: jest.fn(),
  });
}

describe("useEnhancedGameSearch", () => {
  beforeEach(() => {
    jest.clearAllMocks();
    mockSWRReturn();
  });

  // ─── Hook existence ────────────────────────────────────
  it("should export useEnhancedGameSearch as a function", () => {
    expect(typeof useEnhancedGameSearch).toBe("function");
  });

  // ─── Initial state ─────────────────────────────────────
  it("returns empty query and default filters on init", () => {
    const { result } = renderHook(() => useEnhancedGameSearch());
    expect(result.current.query).toBe("");
    expect(result.current.filters).toEqual({
      platforms: [],
      genres: [],
      years: [],
      yearStart: undefined,
      yearEnd: undefined,
      minRating: undefined,
      maxRating: undefined,
      themes: [],
      playerPerspectives: [],
    });
  });

  it("returns default results, no loading, no error on init", () => {
    mockSWRReturn([], undefined, false);
    const { result } = renderHook(() => useEnhancedGameSearch());
    expect(result.current.results).toEqual([]);
    expect(result.current.isLoading).toBe(false);
    expect(result.current.error).toBeUndefined();
  });

  // ─── Query management ──────────────────────────────────
  it("allows setting the search query", () => {
    const { result } = renderHook(() => useEnhancedGameSearch());
    act(() => {
      result.current.setQuery("zelda");
    });
    expect(result.current.query).toBe("zelda");
  });

  // ─── Filter management ─────────────────────────────────
  it("allows updating a single filter via updateFilter", () => {
    const { result } = renderHook(() => useEnhancedGameSearch());
    act(() => {
      result.current.updateFilter("platforms", [6, 48]);
    });
    expect(result.current.filters.platforms).toEqual([6, 48]);
    // Other filters remain at defaults
    expect(result.current.filters.genres).toEqual([]);
  });

  it("allows updating multiple filters independently", () => {
    const { result } = renderHook(() => useEnhancedGameSearch());
    act(() => {
      result.current.updateFilter("platforms", [6]);
      result.current.updateFilter("genres", [4, 12]);
      result.current.updateFilter("minRating", 75);
    });
    expect(result.current.filters.platforms).toEqual([6]);
    expect(result.current.filters.genres).toEqual([4, 12]);
    expect(result.current.filters.minRating).toBe(75);
  });

  it("allows setting filters directly via setFilters", () => {
    const { result } = renderHook(() => useEnhancedGameSearch());
    const newFilters: SearchFilters = {
      ...result.current.filters,
      platforms: [130],
      genres: [31],
    };
    act(() => {
      result.current.setFilters(newFilters);
    });
    expect(result.current.filters.platforms).toEqual([130]);
    expect(result.current.filters.genres).toEqual([31]);
  });

  it("clears all filters via clearFilters", () => {
    const { result } = renderHook(() => useEnhancedGameSearch());
    act(() => {
      result.current.updateFilter("platforms", [6, 48]);
      result.current.updateFilter("genres", [4]);
      result.current.updateFilter("minRating", 80);
      result.current.updateFilter("yearStart", 2020);
      result.current.updateFilter("yearEnd", 2023);
    });
    act(() => {
      result.current.clearFilters();
    });
    expect(result.current.filters).toEqual({
      platforms: [],
      genres: [],
      years: [],
      yearStart: undefined,
      yearEnd: undefined,
      minRating: undefined,
      maxRating: undefined,
      themes: [],
      playerPerspectives: [],
    });
  });

  // ─── Active filter count ───────────────────────────────
  it("counts active filters correctly", () => {
    const { result } = renderHook(() => useEnhancedGameSearch());
    // Initially no filters active
    expect(result.current.activeFilterCount).toBe(0);

    act(() => {
      result.current.updateFilter("platforms", [6, 48]);  // 1 filter category
      result.current.updateFilter("genres", [4, 12]);     // 1 filter category
      result.current.updateFilter("minRating", 75);       // 1 filter category
    });
    // 3 categories have non-default values
    expect(result.current.activeFilterCount).toBe(3);
  });

  it("counts year range as one filter", () => {
    const { result } = renderHook(() => useEnhancedGameSearch());
    act(() => {
      result.current.updateFilter("yearStart", 2020);
      result.current.updateFilter("yearEnd", 2023);
    });
    // year range is one logical filter, not two
    expect(result.current.activeFilterCount).toBe(1);
  });

  // ─── SWR key / URL construction ────────────────────────
  // The SWR key is the full request URL. We verify:
  // 1. Null key when no query (no fetch happens)
  // 2. Correct URL with query + filters when query is set

  it("passes null SWR key when query is empty (no fetch)", () => {
    mockSWRReturn([], undefined, false);
    renderHook(() => useEnhancedGameSearch());
    // Empty query → shouldFetch = false → key = null
    expect(useSWR).toHaveBeenCalledWith(null, expect.any(Function));
  });

  it("passes request URL as SWR key when query is set", () => {
    mockSWRReturn();
    const { result } = renderHook(() => useEnhancedGameSearch());
    act(() => {
      result.current.setQuery("zelda");
    });

    // After re-render with query set, SWR should be called with a URL string
    const callsWithKey = (useSWR as jest.Mock).mock.calls.filter(
      (call: unknown[]) => call[0] !== null
    );
    expect(callsWithKey.length).toBeGreaterThan(0);
    const swrKey = callsWithKey[callsWithKey.length - 1][0] as string;
    expect(swrKey).toContain("/search-enhanced?q=zelda");
  });

  // ─── buildFilterParams (URL param construction) ────────
  // Instead of mocking fetch, we test _buildFilterParams directly.
  // This is the core logic that converts SearchFilters → URL params.

  it("returns empty string when all filters are default", () => {
    const params = buildFilterParams(DEFAULT_FILTERS);
    expect(params).toBe("");
  });

  it("builds comma-separated platform IDs", () => {
    const params = buildFilterParams({
      ...DEFAULT_FILTERS,
      platforms: [6, 48, 130],
    });
    expect(params).toContain("platforms=6,48,130");
  });

  it("builds comma-separated genre IDs", () => {
    const params = buildFilterParams({
      ...DEFAULT_FILTERS,
      genres: [4, 12],
    });
    expect(params).toContain("genres=4,12");
  });

  it("builds comma-separated year values", () => {
    const params = buildFilterParams({
      ...DEFAULT_FILTERS,
      years: [2020, 2021],
    });
    expect(params).toContain("years=2020,2021");
  });

  it("builds year range params", () => {
    const params = buildFilterParams({
      ...DEFAULT_FILTERS,
      yearStart: 2018,
      yearEnd: 2022,
    });
    expect(params).toContain("year_start=2018");
    expect(params).toContain("year_end=2022");
  });

  it("builds rating params", () => {
    const params = buildFilterParams({
      ...DEFAULT_FILTERS,
      minRating: 70,
      maxRating: 90,
    });
    expect(params).toContain("min_rating=70");
    expect(params).toContain("max_rating=90");
  });

  it("builds theme and perspective params", () => {
    const params = buildFilterParams({
      ...DEFAULT_FILTERS,
      themes: [18, 19],
      playerPerspectives: [1, 3],
    });
    expect(params).toContain("themes=18,19");
    expect(params).toContain("player_perspectives=1,3");
  });

  it("builds all filter params combined", () => {
    const params = buildFilterParams({
      ...DEFAULT_FILTERS,
      platforms: [6],
      genres: [4, 12],
      years: [],
      yearStart: 2020,
      yearEnd: 2023,
      minRating: 80,
      maxRating: undefined,
      themes: [18],
      playerPerspectives: [1],
    });
    expect(params).toContain("platforms=6");
    expect(params).toContain("genres=4,12");
    expect(params).toContain("year_start=2020");
    expect(params).toContain("year_end=2023");
    expect(params).toContain("min_rating=80");
    expect(params).toContain("themes=18");
    expect(params).toContain("player_perspectives=1");
    // Empty arrays should NOT appear
    expect(params).not.toContain("years=");
    // Undefined values should NOT appear
    expect(params).not.toContain("max_rating=");
  });

  // ─── Error handling ────────────────────────────────────
  it("returns error state when API fails", () => {
    mockSWRReturn(undefined, new Error("API error"), false);
    const { result } = renderHook(() => useEnhancedGameSearch());
    expect(result.current.error).toBeInstanceOf(Error);
  });

  // ─── Derived state ─────────────────────────────────────
  it("hasQuery is true when query is non-empty", () => {
    const { result } = renderHook(() => useEnhancedGameSearch());
    expect(result.current.hasQuery).toBe(false);
    act(() => {
      result.current.setQuery("zelda");
    });
    expect(result.current.hasQuery).toBe(true);
  });

  it("hasResults is true when results array is non-empty", () => {
    mockSWRReturn(mockGames);
    const { result } = renderHook(() => useEnhancedGameSearch());
    expect(result.current.hasResults).toBe(true);
  });

  it("hasResults is false when results array is empty", () => {
    mockSWRReturn([]);
    const { result } = renderHook(() => useEnhancedGameSearch());
    expect(result.current.hasResults).toBe(false);
  });
});