import { render, screen, fireEvent } from "@testing-library/react";
import DeleteConfirmationModal from "../DeleteConfirmationModal";

describe("DeleteConfirmationModal", () => {
  const mockProps = {
    isOpen: true,
    collectionName: "My Test Collection",
    onConfirm: jest.fn(),
    onCancel: jest.fn(),
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("renders modal when isOpen is true", () => {
    render(<DeleteConfirmationModal {...mockProps} />);

    expect(screen.getByRole("dialog")).toBeInTheDocument();
    expect(
      screen.getByRole("heading", { name: "Delete Collection" })
    ).toBeInTheDocument();
    expect(screen.getByText(/My Test Collection/)).toBeInTheDocument();
  });

  it("does not render when isOpen is false", () => {
    render(<DeleteConfirmationModal {...mockProps} isOpen={false} />);

    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  });

  it("calls onConfirm when Delete Collection button is clicked", () => {
    render(<DeleteConfirmationModal {...mockProps} />);

    const deleteButton = screen.getByRole("button", {
      name: "Delete Collection",
    });
    fireEvent.click(deleteButton);

    expect(mockProps.onConfirm).toHaveBeenCalledTimes(1);
  });

  it("calls onCancel when Cancel button is clicked", () => {
    render(<DeleteConfirmationModal {...mockProps} />);

    const cancelButton = screen.getByText("Cancel");
    fireEvent.click(cancelButton);

    expect(mockProps.onCancel).toHaveBeenCalledTimes(1);
  });

  it("calls onCancel when overlay is clicked", () => {
    render(<DeleteConfirmationModal {...mockProps} />);

    const overlay = screen.getByRole("dialog").parentElement;
    fireEvent.click(overlay!);

    expect(mockProps.onCancel).toHaveBeenCalledTimes(1);
  });

  it("calls onCancel when Escape key is pressed", () => {
    render(<DeleteConfirmationModal {...mockProps} />);

    const overlay = screen.getByRole("dialog").parentElement;
    fireEvent.keyDown(overlay!, { key: "Escape" });

    expect(mockProps.onCancel).toHaveBeenCalledTimes(1);
  });

  it("has proper accessibility attributes", () => {
    render(<DeleteConfirmationModal {...mockProps} />);

    const dialog = screen.getByRole("dialog");
    expect(dialog).toHaveAttribute("aria-modal", "true");
    expect(dialog).toHaveAttribute("aria-labelledby", "delete-modal-title");
    expect(dialog).toHaveAttribute(
      "aria-describedby",
      "delete-modal-description"
    );
  });

  it("focuses delete button on render", () => {
    render(<DeleteConfirmationModal {...mockProps} />);

    const deleteButton = screen.getByRole("button", {
      name: "Delete Collection",
    });
    expect(deleteButton).toHaveFocus();
  });

  it("displays collection name in the confirmation message", () => {
    const customProps = {
      ...mockProps,
      collectionName: "Favorite Games Collection",
    };

    render(<DeleteConfirmationModal {...customProps} />);

    expect(screen.getByText(/Favorite Games Collection/)).toBeInTheDocument();
  });

  it("shows warning about permanent deletion", () => {
    render(<DeleteConfirmationModal {...mockProps} />);

    expect(
      screen.getByText(/This action cannot be undone/)
    ).toBeInTheDocument();
  });
});
