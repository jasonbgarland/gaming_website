// API service for collection entries
import { useAuthStore } from "../store/auth";

export interface CollectionEntry {
  id: number;
  collection_id: number;
  game_id: number;
  notes?: string;
  status?: string;
  rating?: number;
  custom_tags?: Record<string, string>;
  added_at?: string; // ISO date string, as returned by backend
}

export interface CreateCollectionEntryRequest {
  game_id: number;
  notes?: string;
  status?: string;
  rating?: number;
  custom_tags?: Record<string, string>;
}

export interface UpdateCollectionEntryRequest {
  notes?: string;
  status?: string;
  rating?: number;
  custom_tags?: Record<string, string>;
}

class CollectionEntryApi {
  private baseUrl =
    process.env.NEXT_PUBLIC_GAME_SERVICE_URL || "http://localhost:8002";

  private async fetchWithAuth(url: string, options: RequestInit = {}) {
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

  async getCollectionEntries(collectionId: number): Promise<CollectionEntry[]> {
    const response = await this.fetchWithAuth(
      `${this.baseUrl}/collections/${collectionId}/entries/`
    );
    if (!response.ok) {
      throw new Error(`Failed to fetch collection entries: ${response.status}`);
    }
    return response.json();
  }

  async getCollectionEntry(
    collectionId: number,
    entryId: number
  ): Promise<CollectionEntry> {
    const response = await this.fetchWithAuth(
      `${this.baseUrl}/collections/${collectionId}/entries/${entryId}`
    );
    if (!response.ok) {
      throw new Error(`Failed to fetch collection entry: ${response.status}`);
    }
    return response.json();
  }

  async createCollectionEntry(
    collectionId: number,
    data: CreateCollectionEntryRequest
  ): Promise<CollectionEntry> {
    const response = await this.fetchWithAuth(
      `${this.baseUrl}/collections/${collectionId}/entries/`,
      {
        method: "POST",
        body: JSON.stringify(data),
      }
    );
    if (!response.ok) {
      throw new Error(`Failed to create collection entry: ${response.status}`);
    }
    return response.json();
  }

  async updateCollectionEntry(
    collectionId: number,
    entryId: number,
    data: UpdateCollectionEntryRequest
  ): Promise<CollectionEntry> {
    const response = await this.fetchWithAuth(
      `${this.baseUrl}/collections/${collectionId}/entries/${entryId}`,
      {
        method: "PUT",
        body: JSON.stringify(data),
      }
    );
    if (!response.ok) {
      throw new Error(`Failed to update collection entry: ${response.status}`);
    }
    return response.json();
  }

  async deleteCollectionEntry(
    collectionId: number,
    entryId: number
  ): Promise<void> {
    const response = await this.fetchWithAuth(
      `${this.baseUrl}/collections/${collectionId}/entries/${entryId}`,
      {
        method: "DELETE",
      }
    );
    if (!response.ok) {
      throw new Error(`Failed to delete collection entry: ${response.status}`);
    }
  }
}

export const collectionEntryApi = new CollectionEntryApi();
