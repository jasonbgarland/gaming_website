import { render, screen, fireEvent } from "@testing-library/react";
import LibraryTable from "../components/LibraryTable";

describe("LibraryTable", () => {
  const mockCollections = [
    { id: 1, name: "Library", user_id: 1, description: "Library" },
    { id: 2, name: "Backlog", user_id: 1, description: "Backlog" },
    { id: 3, name: "Favorites", user_id: 1, description: "Favorites" },
  ];

  const mockHandlers = {
    onEdit: jest.fn(),
    onDelete: jest.fn(),
    onViewCollection: jest.fn(),
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("renders table headers", () => {
    render(<LibraryTable collections={mockCollections} {...mockHandlers} />);

    expect(screen.getByText("Collection")).toBeInTheDocument();
    expect(screen.getByText("Actions")).toBeInTheDocument();
  });

  it("renders all collections", () => {
    render(<LibraryTable collections={mockCollections} {...mockHandlers} />);

    expect(screen.getByText("Library")).toBeInTheDocument();
    expect(screen.getByText("Backlog")).toBeInTheDocument();
    expect(screen.getByText("Favorites")).toBeInTheDocument();
  });

  it("renders edit and delete buttons for each collection", () => {
    render(<LibraryTable collections={mockCollections} {...mockHandlers} />);

    // Should have 3 edit buttons (one per collection)
    const editButtons = screen.getAllByLabelText(/edit/i);
    expect(editButtons).toHaveLength(3);

    // Should have 3 delete buttons (one per collection)
    const deleteButtons = screen.getAllByLabelText(/delete/i);
    expect(deleteButtons).toHaveLength(3);
  });

  it("calls onViewCollection when collection name is clicked", () => {
    render(<LibraryTable collections={mockCollections} {...mockHandlers} />);

    const libraryButton = screen.getByRole("button", { name: "Library" });
    fireEvent.click(libraryButton);

    expect(mockHandlers.onViewCollection).toHaveBeenCalledWith(1);
  });

  it("calls onEdit when edit button is clicked", () => {
    render(<LibraryTable collections={mockCollections} {...mockHandlers} />);

    const editButton = screen.getByLabelText("Edit Library");
    fireEvent.click(editButton);

    expect(mockHandlers.onEdit).toHaveBeenCalledWith(1);
  });

  it("calls onDelete when delete button is clicked", () => {
    render(<LibraryTable collections={mockCollections} {...mockHandlers} />);

    const deleteButton = screen.getByLabelText("Delete Library");
    fireEvent.click(deleteButton);

    expect(mockHandlers.onDelete).toHaveBeenCalledWith(1);
  });
});
