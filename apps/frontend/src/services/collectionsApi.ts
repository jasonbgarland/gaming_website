// API service for collections
import { useAuthStore } from "../store/auth";

export interface Collection {
  id: number;
  user_id: number;
  name: string;
  description: string;
}

export interface CreateCollectionRequest {
  name: string;
  description?: string;
}

export interface UpdateCollectionRequest {
  name?: string;
  description?: string;
}

class CollectionsApi {
  private baseUrl =
    process.env.NEXT_PUBLIC_GAME_SERVICE_URL || "http://localhost:8002";

  private async fetchWithAuth(url: string, options: RequestInit = {}) {
    // Get token from Zustand auth store
    const token = useAuthStore.getState().token;

    return fetch(url, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options.headers,
      },
    });
  }

  async getCollections(): Promise<Collection[]> {
    const response = await this.fetchWithAuth(`${this.baseUrl}/collections/`);

    if (!response.ok) {
      throw new Error(`Failed to fetch collections: ${response.status}`);
    }

    return response.json();
  }

  async getCollection(id: number): Promise<Collection> {
    const response = await this.fetchWithAuth(
      `${this.baseUrl}/collections/${id}`
    );

    if (!response.ok) {
      throw new Error(`Failed to fetch collection: ${response.status}`);
    }

    return response.json();
  }

  async createCollection(data: CreateCollectionRequest): Promise<Collection> {
    const response = await this.fetchWithAuth(`${this.baseUrl}/collections/`, {
      method: "POST",
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      if (response.status === 422) {
        // Try to get detailed validation error from response
        try {
          const errorData = await response.json();
          if (errorData.detail) {
            throw new Error(`Validation error: ${errorData.detail}`);
          }
        } catch {
          // If we can't parse the error, fall back to generic message
        }
        throw new Error("Invalid collection data. Name can only contain letters, numbers, and spaces.");
      }
      throw new Error(`Failed to create collection: ${response.status}`);
    }

    return response.json();
  }

  async updateCollection(
    id: number,
    data: UpdateCollectionRequest
  ): Promise<Collection> {
    const response = await this.fetchWithAuth(
      `${this.baseUrl}/collections/${id}`,
      {
        method: "PUT",
        body: JSON.stringify(data),
      }
    );

    if (!response.ok) {
      throw new Error(`Failed to update collection: ${response.status}`);
    }

    return response.json();
  }

  async deleteCollection(id: number): Promise<void> {
    const response = await this.fetchWithAuth(
      `${this.baseUrl}/collections/${id}`,
      {
        method: "DELETE",
      }
    );

    if (!response.ok) {
      throw new Error(`Failed to delete collection: ${response.status}`);
    }
  }
}

export const collectionsApi = new CollectionsApi();
