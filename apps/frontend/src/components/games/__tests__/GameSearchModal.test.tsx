import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import GameSearchModal from "../GameSearchModal";
import { useGameSearch } from "../../../hooks/useGameSearch";
import useSWR from "swr";

// Mock the hooks
jest.mock("../../../hooks/useGameSearch");
jest.mock("swr");

const mockUseGameSearch = useGameSearch as jest.Mock;
const mockUseSWR = useSWR as jest.Mock;

// Mock next/image
jest.mock("next/image", () => ({
  __esModule: true,
  default: (props: React.ImgHTMLAttributes<HTMLImageElement>) => {
    // eslint-disable-next-line @next/next/no-img-element, jsx-a11y/alt-text
    return <img {...props} />;
  },
}));

describe("GameSearchModal", () => {
  const mockOnClose = jest.fn();
  const mockOnAddGame = jest.fn();
  const mockUpdateFilter = jest.fn();

  const defaultProps = {
    isOpen: true,
    onClose: mockOnClose,
    onAddGame: mockOnAddGame,
    collectionName: "Test Collection",
  };

  const mockPlatforms = [
    { id: 6, name: "PC" },
    { id: 48, name: "PlayStation" },
  ];

  const mockGenres = [
    { id: 4, name: "Action" },
    { id: 5, name: "RPG" },
  ];

  const defaultFilters = {
    platforms: [],
    genres: [],
    themes: [],
    playerPerspectives: [],
    yearStart: undefined,
    yearEnd: undefined,
    minRating: undefined,
    maxRating: undefined,
  };

  beforeEach(() => {
    jest.clearAllMocks();

    mockUseGameSearch.mockReturnValue({
      query: "",
      setQuery: jest.fn(),
      filters: defaultFilters,
      updateFilter: mockUpdateFilter,
      results: [],
      isLoading: false,
      error: null,
    });

    // Mock useSWR to return platforms and genres
    mockUseSWR.mockImplementation((url: string) => {
      if (url.includes("/platforms")) {
        return { data: mockPlatforms };
      }
      if (url.includes("/genres")) {
        return { data: mockGenres };
      }
      return { data: undefined };
    });
  });

  it("renders modal when open", () => {
    render(<GameSearchModal {...defaultProps} />);

    expect(
      screen.getByRole("heading", { name: /Add Game to.*Test Collection/i })
    ).toBeInTheDocument();
    expect(
      screen.getByPlaceholderText("Search for games...")
    ).toBeInTheDocument();
  });

  it("does not render when closed", () => {
    render(<GameSearchModal {...defaultProps} isOpen={false} />);

    expect(
      screen.queryByText('Add Game to "Test Collection"')
    ).not.toBeInTheDocument();
  });

  it("calls onClose when close button is clicked", () => {
    render(<GameSearchModal {...defaultProps} />);

    fireEvent.click(screen.getByText("✕"));
    expect(mockOnClose).toHaveBeenCalledTimes(1);
  });

  it("renders filter dropdowns", () => {
    render(<GameSearchModal {...defaultProps} />);

    expect(screen.getByText("Platform")).toBeInTheDocument();
    expect(screen.getByText("Genre")).toBeInTheDocument();
    expect(screen.getByText("Year")).toBeInTheDocument();
  });

  it("fetches platform and genre options from API", () => {
    render(<GameSearchModal {...defaultProps} />);

    expect(mockUseSWR).toHaveBeenCalledWith(
      expect.stringContaining("/igdb/platforms"),
      expect.any(Function),
      expect.any(Object)
    );
    expect(mockUseSWR).toHaveBeenCalledWith(
      expect.stringContaining("/igdb/genres"),
      expect.any(Function),
      expect.any(Object)
    );
  });

  it("displays search results", () => {
    const mockGame = {
      id: 1,
      name: "Test Game",
      platforms: ["PC", "PlayStation"],
      release_year: 2023,
      cover_images: {
        small: "https://example.com/cover.jpg",
      },
    };

    mockUseGameSearch.mockReturnValue({
      query: "test",
      setQuery: jest.fn(),
      filters: defaultFilters,
      updateFilter: mockUpdateFilter,
      results: [mockGame],
      isLoading: false,
      error: null,
    });

    render(<GameSearchModal {...defaultProps} />);

    expect(screen.getByText("Test Game")).toBeInTheDocument();
    expect(screen.getByText("PC, PlayStation")).toBeInTheDocument();
    expect(screen.getByText("2023")).toBeInTheDocument();
  });

  it("calls onAddGame when Add button is clicked", async () => {
    const mockGame = {
      id: 1,
      name: "Test Game",
      platforms: ["PC"],
      release_year: 2023,
    };

    mockUseGameSearch.mockReturnValue({
      query: "test",
      setQuery: jest.fn(),
      filters: defaultFilters,
      updateFilter: mockUpdateFilter,
      results: [mockGame],
      isLoading: false,
      error: null,
    });

    render(<GameSearchModal {...defaultProps} />);

    fireEvent.click(screen.getByText("Add"));

    await waitFor(() => {
      expect(mockOnAddGame).toHaveBeenCalledWith(mockGame);
      expect(mockOnClose).toHaveBeenCalledTimes(1);
    });
  });

  it("displays loading state", () => {
    mockUseGameSearch.mockReturnValue({
      query: "test",
      setQuery: jest.fn(),
      filters: defaultFilters,
      updateFilter: mockUpdateFilter,
      results: [],
      isLoading: true,
      error: null,
    });

    render(<GameSearchModal {...defaultProps} />);

    expect(screen.getByText("Searching...")).toBeInTheDocument();
  });

  it("displays error state", () => {
    mockUseGameSearch.mockReturnValue({
      query: "test",
      setQuery: jest.fn(),
      filters: defaultFilters,
      updateFilter: mockUpdateFilter,
      results: [],
      isLoading: false,
      error: "Network error",
    });

    render(<GameSearchModal {...defaultProps} />);

    expect(screen.getByText("Error: Network error")).toBeInTheDocument();
  });

  it("displays active filter chips when filters are applied", () => {
    mockUseGameSearch.mockReturnValue({
      query: "",
      setQuery: jest.fn(),
      filters: {
        ...defaultFilters,
        platforms: [6],
        genres: [4],
        yearStart: 2020,
        yearEnd: 2023,
      },
      updateFilter: mockUpdateFilter,
      results: [],
      isLoading: false,
      error: null,
    });

    render(<GameSearchModal {...defaultProps} />);

    // FilterChips component should be rendered with active filters
    expect(screen.getByText("PC")).toBeInTheDocument();
    expect(screen.getByText("Action")).toBeInTheDocument();
    expect(screen.getByText("2020–2023")).toBeInTheDocument();
  });

  it("does not display filter chips when no filters are active", () => {
    mockUseGameSearch.mockReturnValue({
      query: "",
      setQuery: jest.fn(),
      filters: defaultFilters,
      updateFilter: mockUpdateFilter,
      results: [],
      isLoading: false,
      error: null,
    });

    render(<GameSearchModal {...defaultProps} />);

    // FilterChips component should not be rendered
    expect(screen.queryByText("Clear All")).not.toBeInTheDocument();
  });
});

