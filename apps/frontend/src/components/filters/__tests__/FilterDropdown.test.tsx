import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { FilterDropdown, type FilterOption } from "../FilterDropdown";

const mockOptions: FilterOption[] = [
  { id: 6, label: "PC (Windows)" },
  { id: 48, label: "PlayStation 4" },
  { id: 130, label: "Nintendo Switch" },
  { id: 167, label: "PlayStation 5" },
];

describe("FilterDropdown", () => {
  const mockOnChange = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  // ─── Rendering ─────────────────────────────────────────
  it("renders a button with the given label", () => {
    render(
      <FilterDropdown
        label="Platform"
        options={mockOptions}
        selected={[]}
        onChange={mockOnChange}
      />
    );
    expect(screen.getByRole("button", { name: /platform/i })).toBeInTheDocument();
  });

  it("shows badge count when items are selected", () => {
    render(
      <FilterDropdown
        label="Platform"
        options={mockOptions}
        selected={[6, 130]}
        onChange={mockOnChange}
      />
    );
    // Button should show "2" as a badge
    expect(screen.getByText("2")).toBeInTheDocument();
  });

  it("does not show badge when no items are selected", () => {
    render(
      <FilterDropdown
        label="Platform"
        options={mockOptions}
        selected={[]}
        onChange={mockOnChange}
      />
    );
    // No badge number should be present (only the label text)
    const button = screen.getByRole("button", { name: /platform/i });
    expect(button.textContent).not.toMatch(/\d+/);
  });

  // ─── Dropdown toggle ───────────────────────────────────
  it("does not show dropdown options initially", () => {
    render(
      <FilterDropdown
        label="Platform"
        options={mockOptions}
        selected={[]}
        onChange={mockOnChange}
      />
    );
    expect(screen.queryByText("PC (Windows)")).not.toBeInTheDocument();
    expect(screen.queryByText("PlayStation 4")).not.toBeInTheDocument();
  });

  it("shows dropdown options when button is clicked", async () => {
    const user = userEvent.setup();
    render(
      <FilterDropdown
        label="Platform"
        options={mockOptions}
        selected={[]}
        onChange={mockOnChange}
      />
    );
    await user.click(screen.getByRole("button", { name: /platform/i }));
    expect(screen.getByText("PC (Windows)")).toBeInTheDocument();
    expect(screen.getByText("PlayStation 4")).toBeInTheDocument();
    expect(screen.getByText("Nintendo Switch")).toBeInTheDocument();
    expect(screen.getByText("PlayStation 5")).toBeInTheDocument();
  });

  it("closes dropdown when button is clicked again", async () => {
    const user = userEvent.setup();
    render(
      <FilterDropdown
        label="Platform"
        options={mockOptions}
        selected={[]}
        onChange={mockOnChange}
      />
    );
    // Open
    await user.click(screen.getByRole("button", { name: /platform/i }));
    expect(screen.getByText("PC (Windows)")).toBeInTheDocument();
    // Close
    await user.click(screen.getByRole("button", { name: /platform/i }));
    expect(screen.queryByText("PC (Windows)")).not.toBeInTheDocument();
  });

  // ─── Selection ─────────────────────────────────────────
  it("calls onChange with selected ID when an option is clicked", async () => {
    const user = userEvent.setup();
    render(
      <FilterDropdown
        label="Platform"
        options={mockOptions}
        selected={[]}
        onChange={mockOnChange}
      />
    );
    await user.click(screen.getByRole("button", { name: /platform/i }));
    await user.click(screen.getByText("PC (Windows)"));
    expect(mockOnChange).toHaveBeenCalledWith([6]);
  });

  it("adds to existing selection when clicking a new option", async () => {
    const user = userEvent.setup();
    render(
      <FilterDropdown
        label="Platform"
        options={mockOptions}
        selected={[6]}
        onChange={mockOnChange}
      />
    );
    await user.click(screen.getByRole("button", { name: /platform/i }));
    await user.click(screen.getByText("Nintendo Switch"));
    expect(mockOnChange).toHaveBeenCalledWith([6, 130]);
  });

  it("removes from selection when clicking an already-selected option", async () => {
    const user = userEvent.setup();
    render(
      <FilterDropdown
        label="Platform"
        options={mockOptions}
        selected={[6, 130]}
        onChange={mockOnChange}
      />
    );
    await user.click(screen.getByRole("button", { name: /platform/i }));
    await user.click(screen.getByText("PC (Windows)"));
    expect(mockOnChange).toHaveBeenCalledWith([130]);
  });

  // ─── Visual selection indicators ────────────────────────
  it("visually indicates which options are currently selected", async () => {
    const user = userEvent.setup();
    render(
      <FilterDropdown
        label="Platform"
        options={mockOptions}
        selected={[6]}
        onChange={mockOnChange}
      />
    );
    await user.click(screen.getByRole("button", { name: /platform/i }));
    // Selected option should have a checkmark or distinct styling
    const selectedOption = screen.getByText("PC (Windows)").closest("button") || screen.getByText("PC (Windows)").parentElement;
    expect(selectedOption).toHaveAttribute("aria-pressed", "true");
  });

  it("unselected options do not have aria-pressed true", async () => {
    const user = userEvent.setup();
    render(
      <FilterDropdown
        label="Platform"
        options={mockOptions}
        selected={[6]}
        onChange={mockOnChange}
      />
    );
    await user.click(screen.getByRole("button", { name: /platform/i }));
    const unselectedOption = screen.getByText("PlayStation 4").closest("button") || screen.getByText("PlayStation 4").parentElement;
    expect(unselectedOption).toHaveAttribute("aria-pressed", "false");
  });

  // ─── Click outside closes ──────────────────────────────
  it("closes dropdown when clicking outside", async () => {
    const user = userEvent.setup();
    render(
      <React.Fragment>
        <FilterDropdown
          label="Platform"
          options={mockOptions}
          selected={[]}
          onChange={mockOnChange}
        />
        <div data-testid="outside">Outside area</div>
      </React.Fragment>
    );
    // Open dropdown
    await user.click(screen.getByRole("button", { name: /platform/i }));
    expect(screen.getByText("PC (Windows)")).toBeInTheDocument();
    // Click outside
    await user.click(screen.getByTestId("outside"));
    expect(screen.queryByText("PC (Windows)")).not.toBeInTheDocument();
  });

  // ─── Empty options ─────────────────────────────────────
  it("shows empty state when options list is empty", async () => {
    const user = userEvent.setup();
    render(
      <FilterDropdown
        label="Platform"
        options={[]}
        selected={[]}
        onChange={mockOnChange}
      />
    );
    await user.click(screen.getByRole("button", { name: /platform/i }));
    expect(screen.getByText(/no options available/i)).toBeInTheDocument();
  });
});