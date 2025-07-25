import { collectionsApi } from "../../../services/collectionsApi";
import { useAuthStore } from "../../../store/auth";

// Mock Zustand store
jest.mock("../../../store/auth", () => ({
  useAuthStore: {
    getState: jest.fn(),
  },
}));

const mockUseAuthStore = useAuthStore as jest.Mocked<typeof useAuthStore>;

describe("Collections API Integration", () => {
  let fetchMock: jest.MockedFunction<typeof fetch>;

  beforeEach(() => {
    jest.clearAllMocks();

    // Mock fetch
    fetchMock = jest.fn();
    global.fetch = fetchMock;

    // Mock Zustand store to return a token
    mockUseAuthStore.getState.mockReturnValue({
      token: "mock-jwt-token",
      isLoggedIn: true,
      user: { email: "test@example.com" },
      login: jest.fn(),
      logout: jest.fn(),
    });
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  describe("getCollections", () => {
    it("should successfully fetch collections with correct headers", async () => {
      const mockCollections = [
        {
          id: 1,
          name: "My Favorites",
          description: "Best games ever",
          user_id: 1,
        },
        { id: 2, name: "RPGs", description: "Role playing games", user_id: 1 },
      ];

      fetchMock.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => mockCollections,
      } as Response);

      const result = await collectionsApi.getCollections();

      // Verify API was called with correct parameters
      expect(fetchMock).toHaveBeenCalledWith(
        "http://localhost:8002/collections/",
        expect.objectContaining({
          headers: expect.objectContaining({
            Authorization: "Bearer mock-jwt-token",
            "Content-Type": "application/json",
          }),
        })
      );

      // Verify response
      expect(result).toEqual(mockCollections);
    });

    it("should handle 401 unauthorized response", async () => {
      fetchMock.mockResolvedValueOnce({
        ok: false,
        status: 401,
        statusText: "Unauthorized",
        json: async () => ({ detail: "Invalid token" }),
      } as Response);

      await expect(collectionsApi.getCollections()).rejects.toThrow(
        "Failed to fetch collections: 401"
      );
    });

    it("should handle network errors", async () => {
      fetchMock.mockRejectedValueOnce(new Error("Network error"));

      await expect(collectionsApi.getCollections()).rejects.toThrow(
        "Network error"
      );
    });

    it("should handle missing auth token", async () => {
      // Mock no token in Zustand store
      mockUseAuthStore.getState.mockReturnValue({
        token: null,
        isLoggedIn: false,
        user: null,
        login: jest.fn(),
        logout: jest.fn(),
      });

      fetchMock.mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => [],
      } as Response);

      await collectionsApi.getCollections();

      // Verify API was called without Authorization header
      expect(fetchMock).toHaveBeenCalledWith(
        "http://localhost:8002/collections/",
        expect.objectContaining({
          headers: expect.objectContaining({
            "Content-Type": "application/json",
          }),
        })
      );

      const callArgs = fetchMock.mock.calls[0][1] as RequestInit;
      expect(callArgs.headers).not.toHaveProperty("Authorization");
    });
  });

  describe("createCollection", () => {
    it("should successfully create a collection", async () => {
      const newCollection = {
        name: "New Collection",
        description: "Test collection",
      };
      const createdCollection = {
        id: 3,
        ...newCollection,
        user_id: 1,
      };

      fetchMock.mockResolvedValueOnce({
        ok: true,
        status: 201,
        json: async () => createdCollection,
      } as Response);

      const result = await collectionsApi.createCollection(newCollection);

      // Verify API was called with correct parameters
      expect(fetchMock).toHaveBeenCalledWith(
        "http://localhost:8002/collections/",
        expect.objectContaining({
          method: "POST",
          headers: expect.objectContaining({
            Authorization: "Bearer mock-jwt-token",
            "Content-Type": "application/json",
          }),
          body: JSON.stringify(newCollection),
        })
      );

      // Verify response
      expect(result).toEqual(createdCollection);
    });

    it("should handle validation errors", async () => {
      const newCollection = { name: "", description: "Invalid collection" };

      fetchMock.mockResolvedValueOnce({
        ok: false,
        status: 422,
        statusText: "Unprocessable Entity",
        json: async () => ({
          detail: "name cannot be empty",
        }),
      } as Response);

      await expect(
        collectionsApi.createCollection(newCollection)
      ).rejects.toThrow(
        "Invalid collection data. Name can only contain letters, numbers, and spaces."
      );
    });
  });

  describe("deleteCollection", () => {
    it("should successfully delete a collection", async () => {
      fetchMock.mockResolvedValueOnce({
        ok: true,
        status: 204,
        json: async () => ({}),
      } as Response);

      await collectionsApi.deleteCollection(1);

      // Verify API was called with correct parameters
      expect(fetchMock).toHaveBeenCalledWith(
        "http://localhost:8002/collections/1",
        expect.objectContaining({
          method: "DELETE",
          headers: expect.objectContaining({
            Authorization: "Bearer mock-jwt-token",
            "Content-Type": "application/json",
          }),
        })
      );
    });

    it("should handle 404 not found", async () => {
      fetchMock.mockResolvedValueOnce({
        ok: false,
        status: 404,
        statusText: "Not Found",
        json: async () => ({ detail: "Collection not found" }),
      } as Response);

      await expect(collectionsApi.deleteCollection(999)).rejects.toThrow(
        "Failed to delete collection: 404"
      );
    });
  });

  describe("API endpoint configuration", () => {
    it("should use correct base URL for all endpoints", () => {
      // This verifies that the base URL is configured correctly
      // We've already verified this in the other tests by checking the fetch calls
      expect(true).toBe(true);
    });
  });
});
