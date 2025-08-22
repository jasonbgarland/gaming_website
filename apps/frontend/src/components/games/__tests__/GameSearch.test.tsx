import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import GameSearch from "../GameSearch";
import useSWR from "swr";

// Mock the Next.js Image component
jest.mock("next/image", () => {
  const MockedImage = (props: React.ComponentProps<"img">) => {
    // eslint-disable-next-line @next/next/no-img-element
    return <img {...props} alt={props.alt || "mocked image"} />;
  };
  MockedImage.displayName = "MockedImage";
  return MockedImage;
});

// Mock SWR for loading and error state tests
jest.mock("swr");
describe("GameSearch component (states)", () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

  it("shows loading state when isLoading is true", () => {
    (useSWR as jest.Mock).mockReturnValue({
      data: [],
      error: undefined,
      isLoading: true,
    });
    render(<GameSearch initialResults={[]} />);
    expect(screen.getByText("Searching for games...")).toBeInTheDocument();
  });

  it("shows error state when error is present", () => {
    (useSWR as jest.Mock).mockReturnValue({
      data: [],
      error: { message: "Network error!" },
      isLoading: false,
    });
    render(<GameSearch initialResults={[]} />);
    expect(screen.getByText("Network error!")).toBeInTheDocument();
  });
});
describe("GameSearch component (live search and edge cases)", () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

  it("updates results as user types (live search)", async () => {
    // Simulate SWR returning different results for different queries
    const swrMock = useSWR as jest.Mock;
    swrMock.mockImplementation((key: string | [string, string]) => {
      if (!key || !Array.isArray(key) || !key[1])
        return { data: [], error: undefined, isLoading: false };
      if (key[1] === "halo") {
        return {
          data: [
            {
              id: 1,
              name: "Halo",
              cover_url: "",
              platforms: ["Xbox"],
              release_year: 2001,
            },
          ],
          error: undefined,
          isLoading: false,
        };
      }
      return { data: [], error: undefined, isLoading: false };
    });
    render(<GameSearch initialResults={[]} />);
    const input = screen.getByPlaceholderText("Search for games...");
    fireEvent.change(input, { target: { value: "halo" } });
    // Wait for the result to appear
    await waitFor(() => {
      expect(screen.getByText("Halo")).toBeInTheDocument();
    });
  });

  it("handles missing platforms and release_year gracefully", () => {
    (useSWR as jest.Mock).mockReturnValue({
      data: [
        { id: 4, name: "Mystery Game" },
        { id: 5, name: "Partial", platforms: ["PC"] },
      ],
      error: undefined,
      isLoading: false,
    });
    render(<GameSearch initialResults={[]} />);
    expect(screen.getByText("Mystery Game")).toBeInTheDocument();
    expect(screen.getByText("Partial")).toBeInTheDocument();
    // Should not throw or render undefined for missing fields
  });
});

describe("GameSearch component", () => {
  beforeEach(() => {
    // Reset SWR mock to return no data for these tests (relies on initialResults)
    (useSWR as jest.Mock).mockReturnValue({
      data: undefined,
      error: undefined,
      isLoading: false,
    });
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it("renders a game with all fields present", () => {
    const games = [
      {
        id: 1,
        name: "Test Game",
        cover_url: "//images.igdb.com/igdb/image/upload/t_thumb/test.jpg",
        platforms: ["PC"],
        release_year: 2023,
      },
    ];
    render(<GameSearch initialResults={games} />);
    expect(screen.getByText("Test Game")).toBeInTheDocument();
    expect(screen.getByAltText("Test Game cover")).toBeInTheDocument();
    expect(screen.getByText("Released: 2023")).toBeInTheDocument();
    expect(screen.getByText("Platforms: PC")).toBeInTheDocument();
  });

  it("renders a game without cover image", () => {
    const games = [
      {
        id: 2,
        name: "No Cover Game",
        platforms: ["Switch"],
      },
    ];
    render(<GameSearch initialResults={games} />);
    expect(screen.getByText("No Cover Game")).toBeInTheDocument();
    expect(screen.getByText("Platforms: Switch")).toBeInTheDocument();
    // Should not have an image since cover_url is not provided
    expect(
      screen.queryByAltText("No Cover Game cover")
    ).not.toBeInTheDocument();
  });

  it('renders "Unknown Title" if name is missing', () => {
    const games = [
      {
        id: 3,
        name: "",
        platforms: [],
      },
    ];
    render(<GameSearch initialResults={games} />);
    expect(screen.getByText("Unknown Title")).toBeInTheDocument();
  });

  it("renders empty state for no results", () => {
    render(<GameSearch initialResults={[]} />);
    // With empty initial results and no search query,
    // the component just shows the search form with empty results
    expect(
      screen.getByPlaceholderText("Search for games...")
    ).toBeInTheDocument();
    // No search button in fetch-as-you-type UI
    // (No assertion needed)
  });
});
