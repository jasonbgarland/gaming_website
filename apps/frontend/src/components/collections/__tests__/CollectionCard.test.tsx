import { render, screen, fireEvent } from "@testing-library/react";
import { Collection } from "../../../services/collectionsApi";
import CollectionCard from "../CollectionCard";

describe("CollectionCard", () => {
  const mockCollection: Collection = {
    id: 1,
    user_id: 1,
    name: "Favorite RPGs",
    description: "My collection of favorite role-playing games",
  };

  const mockHandlers = {
    onEdit: jest.fn(),
    onDelete: jest.fn(),
    onViewCollection: jest.fn(),
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("renders collection name and description", () => {
    render(<CollectionCard collection={mockCollection} {...mockHandlers} />);

    expect(screen.getByText("Favorite RPGs")).toBeInTheDocument();
    expect(
      screen.getByText("My collection of favorite role-playing games")
    ).toBeInTheDocument();
  });

  it("displays game count when provided", () => {
    const collectionWithGames = { ...mockCollection, gameCount: 5 };
    render(
      <CollectionCard collection={collectionWithGames} {...mockHandlers} />
    );

    expect(screen.getByText("5 games")).toBeInTheDocument();
  });

  it("displays '0 games' when no games in collection", () => {
    const collectionWithNoGames = { ...mockCollection, gameCount: 0 };
    render(
      <CollectionCard collection={collectionWithNoGames} {...mockHandlers} />
    );

    expect(screen.getByText("0 games")).toBeInTheDocument();
  });

  it("calls onViewCollection when card is clicked", () => {
    render(<CollectionCard collection={mockCollection} {...mockHandlers} />);

    const card = screen.getByRole("button", { name: /view favorite rpgs/i });
    fireEvent.click(card);

    expect(mockHandlers.onViewCollection).toHaveBeenCalledWith(1);
  });

  it("shows action buttons on hover", () => {
    render(<CollectionCard collection={mockCollection} {...mockHandlers} />);

    const card = screen.getByRole("button", { name: /view favorite rpgs/i });

    // Actions should be hidden initially
    expect(screen.queryByText("Edit")).not.toBeVisible();
    expect(screen.queryByText("Delete")).not.toBeVisible();

    // Hover to show actions
    fireEvent.mouseEnter(card);

    expect(screen.getByText("Edit")).toBeVisible();
    expect(screen.getByText("Delete")).toBeVisible();
  });

  it("calls onEdit when edit button is clicked", () => {
    render(<CollectionCard collection={mockCollection} {...mockHandlers} />);

    const card = screen.getByRole("button", { name: /view favorite rpgs/i });
    fireEvent.mouseEnter(card);

    const editButton = screen.getByText("Edit");
    fireEvent.click(editButton);

    expect(mockHandlers.onEdit).toHaveBeenCalledWith(1);
    expect(mockHandlers.onViewCollection).not.toHaveBeenCalled();
  });

  it("calls onDelete when delete button is clicked", () => {
    render(<CollectionCard collection={mockCollection} {...mockHandlers} />);

    const card = screen.getByRole("button", { name: /view favorite rpgs/i });
    fireEvent.mouseEnter(card);

    const deleteButton = screen.getByText("Delete");
    fireEvent.click(deleteButton);

    expect(mockHandlers.onDelete).toHaveBeenCalledWith(1);
    expect(mockHandlers.onViewCollection).not.toHaveBeenCalled();
  });

  it("hides action buttons when mouse leaves", () => {
    render(<CollectionCard collection={mockCollection} {...mockHandlers} />);

    const card = screen.getByRole("button", { name: /view favorite rpgs/i });

    // Show actions on hover
    fireEvent.mouseEnter(card);
    expect(screen.getByText("Edit")).toBeVisible();

    // Hide actions when mouse leaves
    fireEvent.mouseLeave(card);
    expect(screen.queryByText("Edit")).not.toBeVisible();
    expect(screen.queryByText("Delete")).not.toBeVisible();
  });

  it("has proper accessibility attributes", () => {
    render(<CollectionCard collection={mockCollection} {...mockHandlers} />);

    const card = screen.getByRole("button", {
      name: /view favorite rpgs collection/i,
    });
    expect(card).toBeInTheDocument();
    expect(card).toHaveAttribute("tabindex", "0");

    // Collection name should be a heading
    expect(
      screen.getByRole("heading", { name: "Favorite RPGs" })
    ).toBeInTheDocument();
  });

  // Keyboard Navigation Tests
  it("calls onViewCollection when Enter key is pressed", () => {
    render(<CollectionCard collection={mockCollection} {...mockHandlers} />);

    const card = screen.getByRole("button", {
      name: /view favorite rpgs collection/i,
    });
    fireEvent.keyDown(card, { key: "Enter" });

    expect(mockHandlers.onViewCollection).toHaveBeenCalledWith(1);
  });

  it("calls onViewCollection when Space key is pressed", () => {
    render(<CollectionCard collection={mockCollection} {...mockHandlers} />);

    const card = screen.getByRole("button", {
      name: /view favorite rpgs collection/i,
    });
    fireEvent.keyDown(card, { key: " " });

    expect(mockHandlers.onViewCollection).toHaveBeenCalledWith(1);
  });

  it("does not trigger onViewCollection for other keys", () => {
    render(<CollectionCard collection={mockCollection} {...mockHandlers} />);

    const card = screen.getByRole("button", {
      name: /view favorite rpgs collection/i,
    });
    fireEvent.keyDown(card, { key: "Tab" });

    expect(mockHandlers.onViewCollection).not.toHaveBeenCalled();
  });

  // Focus Management Tests
  it("shows action buttons when card receives focus", () => {
    render(<CollectionCard collection={mockCollection} {...mockHandlers} />);

    const card = screen.getByRole("button", {
      name: /view favorite rpgs collection/i,
    });

    // Actions should be hidden initially
    expect(screen.queryByText("Edit")).not.toBeVisible();
    expect(screen.queryByText("Delete")).not.toBeVisible();

    // Focus to show actions
    fireEvent.focus(card);

    expect(screen.getByText("Edit")).toBeVisible();
    expect(screen.getByText("Delete")).toBeVisible();
  });

  it("hides action buttons when card loses focus", () => {
    render(<CollectionCard collection={mockCollection} {...mockHandlers} />);

    const card = screen.getByRole("button", {
      name: /view favorite rpgs collection/i,
    });

    // Focus to show actions
    fireEvent.focus(card);
    expect(screen.getByText("Edit")).toBeVisible();

    // Blur to hide actions
    fireEvent.blur(card);
    expect(screen.queryByText("Edit")).not.toBeVisible();
    expect(screen.queryByText("Delete")).not.toBeVisible();
  });

  // Enhanced ARIA Label Tests
  it("has proper ARIA labels for action buttons", () => {
    render(<CollectionCard collection={mockCollection} {...mockHandlers} />);

    const card = screen.getByRole("button", {
      name: /view favorite rpgs collection/i,
    });
    fireEvent.mouseEnter(card); // Show the action buttons

    expect(
      screen.getByLabelText("Edit Favorite RPGs collection")
    ).toBeInTheDocument();
    expect(
      screen.getByLabelText("Delete Favorite RPGs collection")
    ).toBeInTheDocument();
  });

  it("handles keyboard interactions correctly", () => {
    render(<CollectionCard collection={mockCollection} {...mockHandlers} />);

    const card = screen.getByRole("button", {
      name: /view favorite rpgs collection/i,
    });

    // Test Enter key
    fireEvent.keyDown(card, { key: "Enter" });
    expect(mockHandlers.onViewCollection).toHaveBeenCalledWith(1);

    // Reset mock
    mockHandlers.onViewCollection.mockClear();

    // Test Space key
    fireEvent.keyDown(card, { key: " " });
    expect(mockHandlers.onViewCollection).toHaveBeenCalledWith(1);

    // Reset mock
    mockHandlers.onViewCollection.mockClear();

    // Test that other keys don't trigger action
    fireEvent.keyDown(card, { key: "Escape" });
    expect(mockHandlers.onViewCollection).not.toHaveBeenCalled();
  });
});
