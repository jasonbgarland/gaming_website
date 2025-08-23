import { render, screen, fireEvent, within } from "@testing-library/react";
import CollectionGrid from "../../../components/collections/CollectionGrid";
import { CollectionWithCount } from "../../../hooks/useCollectionsWithCounts";

describe("CollectionGrid", () => {
  const mockCollections: CollectionWithCount[] = [
    {
      id: 1,
      name: "Library",
      user_id: 1,
      description: "This is my games library!",
      gameCount: 20,
    },
    {
      id: 2,
      name: "Backlog",
      user_id: 1,
      description: "Games I want to play soon.",
      gameCount: 17,
    },
    {
      id: 3,
      name: "Favorites",
      user_id: 1,
      description: "My top picks.",
      gameCount: 0, // Explicitly set gameCount
    },
  ];

  const mockHandlers = {
    onDelete: jest.fn(),
    onViewCollection: jest.fn(),
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("renders collection cards", () => {
    render(<CollectionGrid collections={mockCollections} {...mockHandlers} />);

    // There should be 3 collection cards (not counting delete buttons)
    const collectionCards = screen.getAllByRole("button", {
      name: /view .* collection/i,
    });
    expect(collectionCards).toHaveLength(3);

    expect(
      screen.getByRole("heading", { name: /library/i })
    ).toBeInTheDocument();
    expect(
      screen.getByRole("heading", { name: /backlog/i })
    ).toBeInTheDocument();
    expect(
      screen.getByRole("heading", { name: /favorites/i })
    ).toBeInTheDocument();
  });

  it("renders a message if no collections are provided", () => {
    render(<CollectionGrid collections={[]} {...mockHandlers} />);

    // no collections rendered
    const collectionCards = screen.queryAllByRole("button");
    expect(collectionCards).toHaveLength(0);

    expect(screen.getByText("No collections yet!")).toBeInTheDocument();
  });

  it("calls onDelete when the delete button is clicked", () => {
    render(<CollectionGrid collections={mockCollections} {...mockHandlers} />);

    const libraryButton = screen.getByLabelText("Delete Library collection");
    fireEvent.click(libraryButton);
    expect(mockHandlers.onDelete).toHaveBeenCalledWith(1);

    const backlogButton = screen.getByLabelText("Delete Backlog collection");
    fireEvent.click(backlogButton);
    expect(mockHandlers.onDelete).toHaveBeenCalledWith(2);

    const favoritesButton = screen.getByLabelText(
      "Delete Favorites collection"
    );
    fireEvent.click(favoritesButton);
    expect(mockHandlers.onDelete).toHaveBeenCalledWith(3);
  });

  it("calls onView when the view button is clicked", () => {
    render(<CollectionGrid collections={mockCollections} {...mockHandlers} />);

    const libraryButton = screen.getByRole("button", {
      name: "View Library collection",
    });
    fireEvent.click(libraryButton);
    expect(mockHandlers.onViewCollection).toHaveBeenCalledWith(1);

    const backlogButton = screen.getByRole("button", {
      name: "View Backlog collection",
    });
    fireEvent.click(backlogButton);
    expect(mockHandlers.onViewCollection).toHaveBeenCalledWith(2);

    const favoritesButton = screen.getByRole("button", {
      name: "View Favorites collection",
    });
    fireEvent.click(favoritesButton);
    expect(mockHandlers.onViewCollection).toHaveBeenCalledWith(3);
  });

  it("renders collection description and game count", () => {
    render(<CollectionGrid collections={mockCollections} {...mockHandlers} />);

    const cards = screen.getAllByRole("button", {
      name: /view .* collection/i,
    });
    const firstCard = cards[0];
    expect(within(firstCard).getByText("Library")).toBeInTheDocument();
    expect(within(firstCard).getByText("20 games")).toBeInTheDocument();

    const secondCard = cards[1];
    expect(within(secondCard).getByText("Backlog")).toBeInTheDocument();
    expect(within(secondCard).getByText("17 games")).toBeInTheDocument();

    const thirdCard = cards[2];
    expect(within(thirdCard).getByText("Favorites")).toBeInTheDocument();
    // no game count provided, so it will list "0 games"
    expect(within(thirdCard).getByText("0 games")).toBeInTheDocument();
  });

  it("grid container is accessible by region role and label", () => {
    render(<CollectionGrid collections={mockCollections} {...mockHandlers} />);
    const grid = screen.getByRole("region", { name: /collections grid/i });
    expect(grid).toBeInTheDocument();
    expect(grid).toHaveClass("collection-grid");
  });

  it("empty state message is in a live region", () => {
    render(<CollectionGrid collections={[]} {...mockHandlers} />);
    const emptyMsg = screen.getByText("No collections yet!");
    expect(emptyMsg).toHaveAttribute("aria-live", "polite");
  });
});
