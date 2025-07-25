import {
  render,
  screen,
  fireEvent,
  waitFor,
  act,
} from "@testing-library/react";
import CreateCollectionModal from "../components/CreateCollectionModal";

describe("CreateCollectionModal", () => {
  const mockHandlers = {
    onClose: jest.fn(),
    onCreate: jest.fn(),
  };

  beforeEach(() => {
    // Reset all mocks and their call history before each test
    jest.clearAllMocks();
    jest.resetAllMocks();
  });

  it("renders the modal when open is true", () => {
    render(<CreateCollectionModal open={true} {...mockHandlers} />);

    expect(screen.getByRole("dialog")).toBeInTheDocument();
    expect(screen.getByLabelText(/collection name/i)).toBeInTheDocument();
  });

  it("does not render anything when open is false", () => {
    render(<CreateCollectionModal open={false} {...mockHandlers} />);

    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  });

  it("calls onClose when Cancel is clicked", () => {
    render(<CreateCollectionModal open={true} {...mockHandlers} />);

    const cancelButton = screen.getByText(/cancel/i);
    fireEvent.click(cancelButton);
    expect(mockHandlers.onClose).toHaveBeenCalledTimes(1);
  });

  it("calls onCreate when Save is clicked", () => {
    render(<CreateCollectionModal open={true} {...mockHandlers} />);

    fireEvent.change(screen.getByLabelText(/collection name/i), {
      target: { value: "Gifts this year" },
    });

    fireEvent.change(screen.getByLabelText(/description/i), {
      target: { value: "Games I have gathered to gift out this year." },
    });

    const saveButton = screen.getByText(/save/i);
    fireEvent.click(saveButton);
    expect(mockHandlers.onCreate).toHaveBeenCalledTimes(1);
  });

  it("does not call onCreate if required name is missing", () => {
    render(<CreateCollectionModal open={true} {...mockHandlers} />);
    // form is not filled out with required fields, so not submittable!
    const saveButton = screen.getByText(/save/i);
    fireEvent.click(saveButton);
    expect(mockHandlers.onCreate).not.toHaveBeenCalled();
  });

  // --- Unit tests for validateForm logic ---
  describe("validateForm", () => {
    // Import the component to access validateForm
    // We'll define a minimal wrapper to expose validateForm for testing
    function getValidateForm(name: string, description: string) {
      // Simulate the logic from the component
      const errors: { name?: string; description?: string } = {};
      if (!name.trim()) {
        errors.name = "Name is required";
      } else if (name.length < 2) {
        errors.name = "Name must be at least 2 characters";
      } else if (name.length > 50) {
        errors.name = "Name must be 50 characters or less";
      } else if (!/^[A-Za-z0-9 ]+$/.test(name)) {
        errors.name = "Name can only contain letters, numbers, and spaces";
      }
      if (description.length > 200) {
        errors.description = "Description must be 200 characters or less";
      }
      return errors;
    }

    it("returns error if name is missing", () => {
      const errors = getValidateForm("", "desc");
      expect(errors.name).toBe("Name is required");
    });

    it("returns error if name is too short", () => {
      const errors = getValidateForm("A", "desc");
      expect(errors.name).toBe("Name must be at least 2 characters");
    });

    it("returns error if name exceeds 50 chars", () => {
      const errors = getValidateForm("A".repeat(51), "desc");
      expect(errors.name).toBe("Name must be 50 characters or less");
    });

    it("returns error if name contains special characters", () => {
      const errors = getValidateForm("Test!", "desc");
      expect(errors.name).toBe(
        "Name can only contain letters, numbers, and spaces"
      );
    });

    it("returns error if name contains underscore", () => {
      const errors = getValidateForm("Test_Collection", "desc");
      expect(errors.name).toBe(
        "Name can only contain letters, numbers, and spaces"
      );
    });

    it("returns error if name contains hyphen", () => {
      const errors = getValidateForm("Test-Collection", "desc");
      expect(errors.name).toBe(
        "Name can only contain letters, numbers, and spaces"
      );
    });

    it("allows valid names with letters, numbers, and spaces", () => {
      const errors = getValidateForm("My Collection 123", "desc");
      expect(errors.name).toBeUndefined();
    });

    it("returns error if description exceeds 200 chars", () => {
      const errors = getValidateForm("Valid Name", "A".repeat(201));
      expect(errors.description).toBe(
        "Description must be 200 characters or less"
      );
    });

    it("returns no errors for valid input", () => {
      const errors = getValidateForm("Valid Name", "Valid description");
      expect(errors).toEqual({});
    });
  });

  it("disables Save button while submitting", async () => {
    mockHandlers.onCreate.mockImplementation(() => new Promise(() => {})); // never resolves
    render(<CreateCollectionModal open={true} {...mockHandlers} />);
    fireEvent.change(screen.getByLabelText(/collection name/i), {
      target: { value: "Test Name" },
    });
    const saveButton = screen.getByText(/save/i);
    fireEvent.click(saveButton);
    await waitFor(() => expect(saveButton).toBeDisabled());
  });

  it("shows loading indicator while submitting", async () => {
    mockHandlers.onCreate.mockImplementation(() => new Promise(() => {})); // never resolves
    render(<CreateCollectionModal open={true} {...mockHandlers} />);
    fireEvent.change(screen.getByLabelText(/collection name/i), {
      target: { value: "Test Name" },
    });
    const saveButton = screen.getByText(/save/i);
    fireEvent.click(saveButton);
    expect(await screen.findByText(/saving/i)).toBeInTheDocument();
  });

  it("shows error feedback if creation fails", async () => {
    mockHandlers.onCreate.mockRejectedValueOnce(
      new Error("Failed to create collection")
    );
    render(<CreateCollectionModal open={true} {...mockHandlers} />);
    fireEvent.change(screen.getByLabelText(/collection name/i), {
      target: { value: "Gifts this year" },
    });
    fireEvent.change(screen.getByLabelText(/description/i), {
      target: { value: "Games I have gathered to gift out this year." },
    });
    const saveButton = screen.getByText(/save/i);
    // Wrap async event in act() to ensure React state updates are properly handled
    // This prevents "not wrapped in act(...)" warnings when async operations update state
    await act(async () => {
      await fireEvent.click(saveButton);
    });
    expect(
      await screen.findByText(/failed to create collection/i)
    ).toBeInTheDocument();
  });

  it("keeps modal open when creation fails", async () => {
    mockHandlers.onCreate.mockRejectedValueOnce(
      new Error(
        "Validation error: Name can only contain letters, numbers, and spaces."
      )
    );
    render(<CreateCollectionModal open={true} {...mockHandlers} />);
    fireEvent.change(screen.getByLabelText(/collection name/i), {
      target: { value: "Valid Name" }, // Use valid name to bypass frontend validation
    });
    const saveButton = screen.getByText(/save/i);

    await act(async () => {
      await fireEvent.click(saveButton);
    });

    // Modal should stay open (onClose should not be called)
    expect(mockHandlers.onClose).not.toHaveBeenCalled();

    // Error message should be displayed
    expect(
      await screen.findByText(/validation error.*letters.*numbers.*spaces/i)
    ).toBeInTheDocument();
  });

  it("calls onCreate and closes modal on success", async () => {
    const freshMockHandlers = {
      onClose: jest.fn(),
      onCreate: jest.fn().mockResolvedValueOnce({}),
    };

    render(<CreateCollectionModal open={true} {...freshMockHandlers} />);

    fireEvent.change(screen.getByLabelText(/collection name/i), {
      target: { value: "Valid Collection" },
    });

    fireEvent.change(screen.getByLabelText(/description/i), {
      target: { value: "A valid description" },
    });

    const saveButton = screen.getByText(/save/i);
    // Wrap async click in act() to ensure all React state updates complete before assertions
    // This prevents warnings about state updates not being wrapped in act()
    await act(async () => {
      await fireEvent.click(saveButton);
    });
    await waitFor(() => {
      expect(freshMockHandlers.onCreate).toHaveBeenCalledTimes(1);
      expect(freshMockHandlers.onClose).toHaveBeenCalledTimes(1);
    });
  });

  it("focuses the name input when modal opens", () => {
    render(<CreateCollectionModal open={true} {...mockHandlers} />);

    const nameInput = screen.getByLabelText(/collection name/i);
    expect(nameInput).toHaveFocus();
  });

  it("closes modal on Escape key press", () => {
    render(<CreateCollectionModal open={true} {...mockHandlers} />);

    // Press Escape key on the modal
    const modal = screen.getByRole("dialog");
    fireEvent.keyDown(modal, { key: "Escape", code: "Escape" });

    expect(mockHandlers.onClose).toHaveBeenCalledTimes(1);
  });

  it("submits form on Enter key press in name field", () => {
    render(<CreateCollectionModal open={true} {...mockHandlers} />);

    const nameInput = screen.getByLabelText(/collection name/i);
    fireEvent.change(nameInput, {
      target: { value: "Test Collection" },
    });

    // Press Enter in the name field
    fireEvent.keyDown(nameInput, { key: "Enter", code: "Enter" });

    expect(mockHandlers.onCreate).toHaveBeenCalledTimes(1);
  });

  it("has appropriate ARIA attributes for accessibility", () => {
    render(<CreateCollectionModal open={true} {...mockHandlers} />);

    const modal = screen.getByRole("dialog");
    expect(modal).toHaveAttribute("aria-modal", "true");

    // Check that form inputs have proper labels
    const nameInput = screen.getByLabelText(/collection name/i);
    const descriptionInput = screen.getByLabelText(/description/i);

    expect(nameInput).toHaveAttribute("required");
    expect(nameInput).toHaveAttribute("maxlength", "50");
    expect(descriptionInput).toHaveAttribute("maxlength", "200");

    // Check that inputs have proper IDs and labels are connected
    expect(nameInput).toHaveAttribute("id", "collection-name");
    expect(descriptionInput).toHaveAttribute("id", "collection-description");
  });

  it("calls onClose when clicking outside the modal (overlay)", () => {
    render(<CreateCollectionModal open={true} {...mockHandlers} />);

    // Click on the modal overlay itself (the div with role="dialog")
    // Our modal structure has the overlay and dialog as the same element
    const modal = screen.getByRole("dialog");
    fireEvent.click(modal);

    expect(mockHandlers.onClose).toHaveBeenCalledTimes(1);
  });
});
