import React from "react";
import {
  render,
  screen,
  waitFor,
  fireEvent,
  act,
} from "@testing-library/react";
import { SWRConfig } from "swr";
import LibraryPage from "../page";
import { useAuthStore } from "../../../store/auth";

// Mock the CollectionGrid component to focus on API integration
jest.mock("../../../components/collections/CollectionGrid", () => {
  return function MockCollectionGrid({
    collections,
  }: {
    collections: Array<{ id: number; name: string; description: string }>;
    onEdit: (id: number) => void;
    onDelete: (id: number) => void;
    onViewCollection: (id: number) => void;
  }) {
    return (
      <div data-testid="collection-grid">
        <div data-testid="collections-count">
          Collections: {collections.length}
        </div>
        {collections.map((collection) => (
          <div key={collection.id} data-testid={`collection-${collection.id}`}>
            {collection.name} - {collection.description}
          </div>
        ))}
      </div>
    );
  };
});

// Mock Next.js router
jest.mock("next/navigation", () => ({
  useRouter: () => ({
    push: jest.fn(),
    back: jest.fn(),
    forward: jest.fn(),
    refresh: jest.fn(),
    replace: jest.fn(),
    prefetch: jest.fn(),
  }),
}));

// Mock Zustand store
jest.mock("../../../store/auth", () => ({
  useAuthStore: {
    getState: jest.fn(),
  },
}));

const mockUseAuthStore = useAuthStore as jest.Mocked<typeof useAuthStore>;

describe("LibraryPage - API Integration", () => {
  let fetchMock: jest.MockedFunction<typeof fetch>;

  // Helper function to render with fresh SWR cache
  const renderWithFreshCache = (component: React.ReactElement) => {
    return render(
      <SWRConfig value={{ provider: () => new Map() }}>{component}</SWRConfig>
    );
  };

  beforeEach(() => {
    jest.clearAllMocks();

    // Mock fetch
    fetchMock = jest.fn();
    global.fetch = fetchMock;

    // Mock Zustand store to return a token
    mockUseAuthStore.getState.mockReturnValue({
      token: "mock-jwt-token",
      isLoggedIn: true,
      user: { email: "test@example.com", username: "testuser" },
      login: jest.fn(),
      logout: jest.fn(),
    });
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  it("should successfully fetch and display collections from API", async () => {
    // Mock successful API response
    const mockCollections = [
      {
        id: 1,
        name: "My Favorites",
        description: "Best games ever",
        user_id: 1,
        created_at: "2023-01-01T00:00:00Z",
      },
      {
        id: 2,
        name: "RPGs",
        description: "Role playing games",
        user_id: 1,
        created_at: "2023-01-02T00:00:00Z",
      },
    ];

    fetchMock.mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: async () => mockCollections,
    } as Response);

    renderWithFreshCache(<LibraryPage />);

    // Initially should show loading
    expect(screen.getByText("Loading collections...")).toBeInTheDocument();

    // Wait for API call to complete
    await waitFor(() => {
      expect(screen.queryByText("Loading collections...")).not.toBeInTheDocument();
    });

    // Verify API was called with correct parameters
    expect(fetchMock).toHaveBeenCalledWith(
      "http://localhost:8002/collections/",
      {
        headers: {
          Authorization: "Bearer mock-jwt-token",
          "Content-Type": "application/json",
        },
      }
    );

    // Verify collections are displayed
    expect(screen.getByTestId("collections-count")).toHaveTextContent(
      "Collections: 2"
    );
    expect(screen.getByTestId("collection-1")).toHaveTextContent(
      "My Favorites - Best games ever"
    );
    expect(screen.getByTestId("collection-2")).toHaveTextContent(
      "RPGs - Role playing games"
    );
  });

  it("should handle API error gracefully", async () => {
    // Mock API error response
    fetchMock.mockRejectedValueOnce(new Error("Network error"));

    renderWithFreshCache(<LibraryPage />);

    // Wait for error to be handled
    await waitFor(() => {
      expect(screen.queryByText("Loading...")).not.toBeInTheDocument();
    });

    // Verify error state is shown
    expect(
      screen.getByText(/Error loading collections: Network error/i)
    ).toBeInTheDocument();
  });

  it("should handle 401 unauthorized response", async () => {
    // Mock 401 response
    fetchMock.mockResolvedValueOnce({
      ok: false,
      status: 401,
      statusText: "Unauthorized",
      json: async () => ({ detail: "Invalid token" }),
    } as Response);

    renderWithFreshCache(<LibraryPage />);

    // Wait for error to be handled
    await waitFor(() => {
      expect(screen.queryByText("Loading...")).not.toBeInTheDocument();
    });

    // Verify error state is shown
    expect(screen.getByText(/Error loading collections/i)).toBeInTheDocument();
  });

  it("should handle empty collections response", async () => {
    // Mock empty response
    fetchMock.mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: async () => [],
    } as Response);

    renderWithFreshCache(<LibraryPage />);

    // Wait for API call to complete
    await waitFor(() => {
      expect(screen.queryByText("Loading...")).not.toBeInTheDocument();
    });

    // Verify empty state
    expect(screen.getByTestId("collections-count")).toHaveTextContent(
      "Collections: 0"
    );
  });

  it("should use correct API endpoint URL", async () => {
    // Mock successful response
    fetchMock.mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: async () => [],
    } as Response);

    renderWithFreshCache(<LibraryPage />);

    // Wait for API call
    await waitFor(() => {
      expect(fetchMock).toHaveBeenCalled();
    });

    // Verify the correct endpoint was called
    expect(fetchMock).toHaveBeenCalledWith(
      "http://localhost:8002/collections/",
      {
        headers: {
          Authorization: "Bearer mock-jwt-token",
          "Content-Type": "application/json",
        },
      }
    );
  });

  it("should create a new collection successfully", async () => {
    const initialCollections = [
      {
        id: 1,
        name: "Existing Collection",
        description: "Already here",
        user_id: 1,
        created_at: "2023-01-01T00:00:00Z",
      },
    ];

    const newCollection = {
      id: 2,
      name: "New Test Collection",
      description: "Created via modal",
      user_id: 1,
      created_at: "2023-01-02T00:00:00Z",
    };

    // Mock initial fetch for collections
    fetchMock.mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: async () => initialCollections,
    } as Response);

    renderWithFreshCache(<LibraryPage />);

    // Wait for initial load
    await waitFor(() => {
      expect(screen.queryByText("Loading...")).not.toBeInTheDocument();
    });

    // Verify initial state
    expect(screen.getByTestId("collections-count")).toHaveTextContent(
      "Collections: 1"
    );

    // Click "Create Collection" button
    const createButton = screen.getByRole("button", {
      name: /create collection/i,
    });
    fireEvent.click(createButton);

    // Wait for modal to appear
    await waitFor(() => {
      expect(screen.getByRole("dialog")).toBeInTheDocument();
    });

    // Fill out the form
    const nameInput = screen.getByLabelText(/collection name/i);
    const descriptionInput = screen.getByLabelText(/description/i);

    fireEvent.change(nameInput, { target: { value: "New Test Collection" } });
    fireEvent.change(descriptionInput, {
      target: { value: "Created via modal" },
    });

    // Mock the create collection API call
    fetchMock.mockResolvedValueOnce({
      ok: true,
      status: 201,
      json: async () => newCollection,
    } as Response);

    // Mock the refetch after creation (SWR will refetch)
    fetchMock.mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: async () => [...initialCollections, newCollection],
    } as Response);

    // Submit the form
    const saveButton = screen.getByRole("button", { name: /save/i });

    await act(async () => {
      fireEvent.click(saveButton);
    });

    // Wait for modal to close and API calls to complete
    await waitFor(() => {
      expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
    });

    // Verify the create API was called correctly
    expect(fetchMock).toHaveBeenCalledWith(
      "http://localhost:8002/collections/",
      {
        method: "POST",
        headers: {
          Authorization: "Bearer mock-jwt-token",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: "New Test Collection",
          description: "Created via modal",
        }),
      }
    );

    // Wait for optimistic update or refetch to show new collection
    await waitFor(() => {
      expect(screen.getByTestId("collections-count")).toHaveTextContent(
        "Collections: 2"
      );
    });

    // Verify new collection appears in the list
    expect(screen.getByTestId("collection-2")).toHaveTextContent(
      "New Test Collection - Created via modal"
    );
  });

  it("should handle create collection API error gracefully", async () => {
    // Mock initial fetch for collections
    fetchMock.mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: async () => [],
    } as Response);

    // Mock console.error to check error logging
    const consoleSpy = jest
      .spyOn(console, "error")
      .mockImplementation(() => {});

    renderWithFreshCache(<LibraryPage />);

    // Wait for initial load
    await waitFor(() => {
      expect(screen.queryByText("Loading...")).not.toBeInTheDocument();
    });

    // Click "Create Collection" button
    const createButton = screen.getByRole("button", {
      name: /create collection/i,
    });
    fireEvent.click(createButton);

    // Wait for modal to appear
    await waitFor(() => {
      expect(screen.getByRole("dialog")).toBeInTheDocument();
    });

    // Fill out the form
    const nameInput = screen.getByLabelText(/collection name/i);
    fireEvent.change(nameInput, { target: { value: "Test Collection" } });

    // Mock API error for create collection
    fetchMock.mockRejectedValueOnce(
      new Error("Failed to create collection: 500")
    );

    // Submit the form
    const saveButton = screen.getByRole("button", { name: /save/i });

    await act(async () => {
      fireEvent.click(saveButton);
    });

    // Wait for error handling
    await waitFor(() => {
      expect(consoleSpy).toHaveBeenCalledWith(
        "Failed to create collection:",
        expect.any(Error)
      );
    });

    // Modal should still close even on error (as per current implementation)
    await waitFor(() => {
      expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
    });

    consoleSpy.mockRestore();
  });
});
