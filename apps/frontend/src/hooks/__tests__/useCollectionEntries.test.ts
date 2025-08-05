import { renderHook } from "@testing-library/react";
import { useCollectionEntries } from "../useCollectionEntries";
import useSWR from "swr";

jest.mock("swr");

const mockEntries = [
  {
    id: 1,
    collection_id: 42,
    game_id: 100,
    notes: "Great game!",
    status: "completed",
    rating: 9,
    custom_tags: { genre: "adventure" },
    added_at: "2025-07-30T12:00:00Z",
  },
];

describe("useCollectionEntries", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("returns entries, loading, and error state", () => {
    (useSWR as jest.Mock).mockReturnValue({
      data: mockEntries,
      error: undefined,
      isLoading: false,
      mutate: jest.fn(),
    });
    const { result } = renderHook(() => useCollectionEntries(42));
    expect(result.current.entries).toEqual(mockEntries);
    expect(result.current.isLoading).toBe(false);
    expect(result.current.error).toBeUndefined();
    expect(result.current.hasEntries).toBe(true);
  });

  it("returns empty array and hasEntries false if no entries", () => {
    (useSWR as jest.Mock).mockReturnValue({
      data: [],
      error: undefined,
      isLoading: false,
      mutate: jest.fn(),
    });
    const { result } = renderHook(() => useCollectionEntries(42));
    expect(result.current.entries).toEqual([]);
    expect(result.current.hasEntries).toBe(false);
  });

  it("returns loading state", () => {
    (useSWR as jest.Mock).mockReturnValue({
      data: undefined,
      error: undefined,
      isLoading: true,
      mutate: jest.fn(),
    });
    const { result } = renderHook(() => useCollectionEntries(42));
    expect(result.current.isLoading).toBe(true);
  });

  it("returns error state", () => {
    (useSWR as jest.Mock).mockReturnValue({
      data: undefined,
      error: new Error("Failed to fetch"),
      isLoading: false,
      mutate: jest.fn(),
    });
    const { result } = renderHook(() => useCollectionEntries(42));
    expect(result.current.error).toBeInstanceOf(Error);
  });
});
