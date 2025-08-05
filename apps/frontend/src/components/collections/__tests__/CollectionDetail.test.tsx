import { render } from "@testing-library/react";
import CollectionDetail from "../CollectionDetail";

describe("CollectionDetail", () => {
  const mockCollection = {
    id: 1,
    user_id: 1,
    name: "Summer releases",
    description: "Games I want to play this summer",
  };

  it("shows collection name and description", () => {
    const { getByText } = render(
      <CollectionDetail collection={mockCollection} />
    );
    expect(getByText("Summer releases")).toBeInTheDocument();
    expect(getByText("Games I want to play this summer")).toBeInTheDocument();
  });

  it("shows a loading indicator when loading", () => {
    const { getByText, queryByText } = render(
      <CollectionDetail
        collection={mockCollection}
        isLoading={true}
        error={undefined}
      />
    );
    expect(getByText("Summer releases")).toBeInTheDocument();
    expect(getByText("Games I want to play this summer")).toBeInTheDocument();
    expect(getByText(/loading.../i)).toBeInTheDocument();
    // Should not show error while loading
    expect(queryByText(/error loading entries/i)).not.toBeInTheDocument();
  });
  it("shows an empty state if there are no games", () => {
    const { getByText, queryByText } = render(
      <CollectionDetail
        collection={[]}
        isLoading={false}
        error={undefined}
      />
    );
    expect(getByText(/no games in this collection/i)).toBeInTheDocument();
    // Should not show loading or error
    expect(queryByText(/loading entries/i)).not.toBeInTheDocument();
    expect(queryByText(/error loading entries/i)).not.toBeInTheDocument();
  });
});
