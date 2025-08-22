import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import GameSearchModal from "../GameSearchModal";
import { useGameSearch } from "../../../hooks/useGameSearch";

// Mock the useGameSearch hook
jest.mock("../../../hooks/useGameSearch");
const mockUseGameSearch = useGameSearch as jest.Mock;

describe("GameSearchModal", () => {
  const mockOnClose = jest.fn();
  const mockOnAddGame = jest.fn();

  const defaultProps = {
    isOpen: true,
    onClose: mockOnClose,
    onAddGame: mockOnAddGame,
    collectionName: "Test Collection",
  };

  beforeEach(() => {
    jest.clearAllMocks();
    mockUseGameSearch.mockReturnValue({
      query: "",
      setQuery: jest.fn(),
      results: [],
      isLoading: false,
      error: null,
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
      results: [],
      isLoading: false,
      error: "Network error",
    });

    render(<GameSearchModal {...defaultProps} />);

    expect(screen.getByText("Error: Network error")).toBeInTheDocument();
  });
});
