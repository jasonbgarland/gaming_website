import { render, screen, fireEvent } from "@testing-library/react";
import { useRouter } from "next/navigation";
import LibraryPage from "../page";
import { Collection } from "services/collectionsApi";

// Mock Next.js router
jest.mock("next/navigation", () => ({
  useRouter: jest.fn(),
}));

// Mock the CollectionGrid component
jest.mock("../components/CollectionGrid", () => {
  return function MockCollectionGrid({
    collections,
    onEdit,
    onDelete,
    onViewCollection,
  }: {
    collections: Array<{ id: number; name: string }>;
    onEdit: (id: number) => void;
    onDelete: (id: number) => void;
    onViewCollection: (id: number) => void;
  }) {
    return (
      <div data-testid="collection-grid">
        <div>Collections: {collections.length}</div>
        <button onClick={() => onEdit(1)}>Edit Mock</button>
        <button onClick={() => onDelete(1)}>Delete Mock</button>
        <button onClick={() => onViewCollection(1)}>View Mock</button>
      </div>
    );
  };
});

// Mock the useCollectionsWithCounts hook
jest.mock("../../../hooks/useCollectionsWithCounts", () => ({
  useCollectionsWithCounts: jest.fn(),
}));

const mockPush = jest.fn();
const mockUseRouter = useRouter as jest.MockedFunction<typeof useRouter>;

// Dynamic import to avoid require()
const mockUseCollectionsWithCounts = jest.fn();
jest.mock("../../../hooks/useCollectionsWithCounts", () => ({
  useCollectionsWithCounts: () => mockUseCollectionsWithCounts(),
}));

describe("LibraryPage", () => {
  beforeEach(() => {
    jest.clearAllMocks();
    mockUseRouter.mockReturnValue({
      push: mockPush,
      back: jest.fn(),
      forward: jest.fn(),
      refresh: jest.fn(),
      replace: jest.fn(),
      prefetch: jest.fn(),
    });
  });

  it("renders the My Library heading", () => {
    // Mock loading state
    mockUseCollectionsWithCounts.mockReturnValue({
      collections: [],
      isLoading: true,
      error: null,
      deleteCollection: jest.fn(),
      createCollection: jest.fn(),
      updateCollection: jest.fn(),
      refreshCollections: jest.fn(),
      refreshCollectionsWithCounts: jest.fn(),
      updateCollectionCount: jest.fn(),
      hasCollections: false,
    });

    render(<LibraryPage />);

    const heading = screen.getByRole("heading", { name: /my library/i });
    expect(heading).toBeInTheDocument();
  });

  it("shows loading state initially", () => {
    // Mock loading state
    mockUseCollectionsWithCounts.mockReturnValue({
      collections: [],
      isLoading: true,
      error: null,
      deleteCollection: jest.fn(),
      createCollection: jest.fn(),
      updateCollection: jest.fn(),
      refreshCollections: jest.fn(),
      refreshCollectionsWithCounts: jest.fn(),
      updateCollectionCount: jest.fn(),
      hasCollections: false,
    });

    render(<LibraryPage />);

    expect(screen.getByText("Loading...")).toBeInTheDocument();
  });

  it("shows error state when API fails", () => {
    // Mock error state
    mockUseCollectionsWithCounts.mockReturnValue({
      collections: [],
      isLoading: false,
      error: new Error("Failed to fetch collections"),
      deleteCollection: jest.fn(),
      createCollection: jest.fn(),
      updateCollection: jest.fn(),
      refreshCollections: jest.fn(),
      refreshCollectionsWithCounts: jest.fn(),
      updateCollectionCount: jest.fn(),
      hasCollections: false,
    });

    render(<LibraryPage />);

    expect(
      screen.getByText("Error loading collections: Failed to fetch collections")
    ).toBeInTheDocument();
  });

  it("renders CollectionGrid with collections after loading", async () => {
    const mockCollections = [
      { id: 1, name: "My Favorites", description: "Best games" },
      { id: 2, name: "RPGs", description: "Role playing games" },
      { id: 3, name: "Indie Games", description: "Independent games" },
    ];

    // Mock loaded state with collections
    mockUseCollectionsWithCounts.mockReturnValue({
      collections: mockCollections.map((c) => ({ ...c, gameCount: 0 })),
      isLoading: false,
      error: null,
      deleteCollection: jest.fn(),
      createCollection: jest.fn(),
      updateCollection: jest.fn(),
      refreshCollections: jest.fn(),
      refreshCollectionsWithCounts: jest.fn(),
      updateCollectionCount: jest.fn(),
      hasCollections: true,
    });

    render(<LibraryPage />);

    // Should render the mocked grid
    expect(screen.getByTestId("collection-grid")).toBeInTheDocument();
    expect(screen.getByText("Collections: 3")).toBeInTheDocument();
  });

  it("passes correct handlers to CollectionGrid", async () => {
    const mockCollections = [
      { id: 1, name: "My Favorites", description: "Best games" },
    ];

    const mockDeleteCollection = jest.fn();

    // Mock loaded state with collections
    mockUseCollectionsWithCounts.mockReturnValue({
      collections: mockCollections.map((c) => ({ ...c, gameCount: 0 })),
      isLoading: false,
      error: null,
      deleteCollection: mockDeleteCollection,
      createCollection: jest.fn(),
      updateCollection: jest.fn(),
      refreshCollections: jest.fn(),
      refreshCollectionsWithCounts: jest.fn(),
      updateCollectionCount: jest.fn(),
      hasCollections: true,
    });

    render(<LibraryPage />);

    // Test that clicking view calls router.push
    const viewButton = screen.getByText("View Mock");
    viewButton.click();

    expect(mockPush).toHaveBeenCalledWith("/library/collections/1");
  });

  it("shows the Create Collection form when button is clicked", () => {
    // Mock collections to be empty
    const mockCollections: Collection[] = [];

    // Mock loaded state with collections
    mockUseCollectionsWithCounts.mockReturnValue({
      collections: mockCollections.map((c) => ({ ...c, gameCount: 0 })),
      isLoading: false,
      error: null,
      deleteCollection: jest.fn(),
      createCollection: jest.fn(),
      updateCollection: jest.fn(),
      refreshCollections: jest.fn(),
      refreshCollectionsWithCounts: jest.fn(),
      updateCollectionCount: jest.fn(),
      hasCollections: false,
    });

    render(<LibraryPage />);

    // Initially, the modal should not be visible
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();

    // Find and click the "Create Collection" button
    const createCollectionButton = screen.getByRole("button", {
      name: "Create Collection",
    });
    fireEvent.click(createCollectionButton);

    // After clicking, the modal should appear with form fields
    expect(screen.getByLabelText(/collection name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/description/i)).toBeInTheDocument();
    expect(screen.getByRole("dialog")).toBeInTheDocument();

    // Check that the submit button ("Save") and cancel button exist in the modal
    const submitButton = screen.getByRole("button", { name: "Save" });
    const cancelButton = screen.getByRole("button", { name: "Cancel" });
    expect(submitButton).toBeInTheDocument();
    expect(cancelButton).toBeInTheDocument();
  });
});
