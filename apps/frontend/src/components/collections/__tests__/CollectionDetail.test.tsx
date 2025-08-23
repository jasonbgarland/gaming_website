import { jest } from "@jest/globals";
import { render } from "@testing-library/react";
import CollectionDetail from "../CollectionDetail";

// Mock the hooks
jest.mock("@/hooks/useCollectionEntries", () => ({
  useCollectionEntries: jest.fn(),
}));

import { useCollectionEntries } from "@/hooks/useCollectionEntries";
const mockUseCollectionEntries = useCollectionEntries as jest.Mock;

describe("CollectionDetail", () => {
  const mockCollection = {
    id: 1,
    user_id: 1,
    name: "Summer releases",
    description: "Games I want to play this summer",
  };

  beforeEach(() => {
    // Default mock implementation
    mockUseCollectionEntries.mockReturnValue({
      entries: [],
      isLoading: false,
      error: null,
      addEntry: jest.fn(),
      removeEntry: jest.fn(),
    });
  });

  it("shows collection name and description", () => {
    const { getByText } = render(
      <CollectionDetail collection={mockCollection} />
    );
    expect(getByText("Summer releases")).toBeInTheDocument();
    expect(getByText("Games I want to play this summer")).toBeInTheDocument();
  });

  it("shows a loading indicator when loading", () => {
    mockUseCollectionEntries.mockReturnValue({
      entries: [],
      isLoading: true,
      error: null,
      addEntry: jest.fn(),
      removeEntry: jest.fn(),
    });
    
    const { getByText, queryByText } = render(
      <CollectionDetail collection={mockCollection} />
    );
    expect(getByText("Summer releases")).toBeInTheDocument();
    expect(getByText("Games I want to play this summer")).toBeInTheDocument();
    expect(getByText(/loading games.../i)).toBeInTheDocument();
    // Should not show error while loading
    expect(queryByText(/error loading games/i)).not.toBeInTheDocument();
  });
  
  it("shows an empty state if there are no games", () => {
    mockUseCollectionEntries.mockReturnValue({
      entries: [],
      isLoading: false,
      error: null,
      addEntry: jest.fn(),
      removeEntry: jest.fn(),
    });
    
    const { getByText, queryByText } = render(
      <CollectionDetail collection={mockCollection} />
    );
    expect(getByText(/no games yet!/i)).toBeInTheDocument();
    // Should not show loading or error
    expect(queryByText(/loading games/i)).not.toBeInTheDocument();
    expect(queryByText(/error loading games/i)).not.toBeInTheDocument();
  });
});
