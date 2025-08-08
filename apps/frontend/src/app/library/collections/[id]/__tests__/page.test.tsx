import React from "react";
import { render, screen } from "@testing-library/react";
import CollectionDetailPage from "../page";

import * as nextNavigation from "next/navigation";
import { useCollection } from "hooks/useCollection";
import { useCollectionEntries } from "hooks/useCollectionEntries";

jest.mock("next/navigation");
jest.mock("hooks/useCollection");
jest.mock("hooks/useCollectionEntries");

const mockUseParams = nextNavigation.useParams as jest.Mock;
const mockUseCollection = useCollection as jest.Mock;
const mockUseCollectionEntries = useCollectionEntries as jest.Mock;

describe("CollectionDetailPage", () => {
  beforeEach(() => {
    jest.clearAllMocks();
    mockUseCollectionEntries.mockReturnValue({
      entries: [],
      isLoading: false,
      error: null,
    });
  });

  it("renders loading state", () => {
    mockUseParams.mockReturnValue({ id: "1" });
    mockUseCollection.mockReturnValue({
      collection: null,
      isLoading: true,
      error: null,
    });

    render(<CollectionDetailPage />);

    expect(screen.getByText("Loading collection...")).toBeInTheDocument();
  });

  it("renders error state", () => {
    mockUseParams.mockReturnValue({ id: "1" });
    mockUseCollection.mockReturnValue({
      collection: null,
      isLoading: false,
      error: { message: "Failed to load collection" },
    });

    render(<CollectionDetailPage />);

    expect(screen.getByText("Collection Not Found")).toBeInTheDocument();
    expect(
      screen.getByText("Error: Failed to load collection")
    ).toBeInTheDocument();
  });
});
