import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { YearRangeDropdown } from "../YearRangeDropdown";

describe("YearRangeDropdown", () => {
  const mockOnChange = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  // ─── Rendering ─────────────────────────────────────────

  it("renders a button labelled 'Year' when no range is set", () => {
    render(
      <YearRangeDropdown onChange={mockOnChange} />
    );
    expect(screen.getByRole("button", { name: /^year/i })).toBeInTheDocument();
  });

  it("shows 'Year: 2020–2023' in button label when both values are set", () => {
    render(
      <YearRangeDropdown yearStart={2020} yearEnd={2023} onChange={mockOnChange} />
    );
    expect(screen.getByRole("button", { name: /year.*2020.*2023/i })).toBeInTheDocument();
  });

  it("shows 'Year: 2020–' when only yearStart is set", () => {
    render(
      <YearRangeDropdown yearStart={2020} onChange={mockOnChange} />
    );
    expect(screen.getByRole("button", { name: /year.*2020/i })).toBeInTheDocument();
  });

  it("shows 'Year: –2023' when only yearEnd is set", () => {
    render(
      <YearRangeDropdown yearEnd={2023} onChange={mockOnChange} />
    );
    expect(screen.getByRole("button", { name: /year.*2023/i })).toBeInTheDocument();
  });

  // ─── Panel visibility ──────────────────────────────────

  it("does not show From/To inputs initially", () => {
    render(
      <YearRangeDropdown onChange={mockOnChange} />
    );
    expect(screen.queryByLabelText(/from/i)).not.toBeInTheDocument();
    expect(screen.queryByLabelText(/to/i)).not.toBeInTheDocument();
  });

  it("shows From and To inputs when button is clicked", async () => {
    const user = userEvent.setup();
    render(
      <YearRangeDropdown onChange={mockOnChange} />
    );
    await user.click(screen.getByRole("button", { name: /^year/i }));
    expect(screen.getByLabelText(/from/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/to/i)).toBeInTheDocument();
  });

  it("closes panel when button is clicked again", async () => {
    const user = userEvent.setup();
    render(
      <YearRangeDropdown onChange={mockOnChange} />
    );
    await user.click(screen.getByRole("button", { name: /^year/i }));
    expect(screen.getByLabelText(/from/i)).toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: /^year/i }));
    expect(screen.queryByLabelText(/from/i)).not.toBeInTheDocument();
  });

  it("closes panel when clicking outside", async () => {
    const user = userEvent.setup();
    render(
      <React.Fragment>
        <YearRangeDropdown onChange={mockOnChange} />
        <div data-testid="outside">Outside</div>
      </React.Fragment>
    );
    await user.click(screen.getByRole("button", { name: /^year/i }));
    expect(screen.getByLabelText(/from/i)).toBeInTheDocument();
    await user.click(screen.getByTestId("outside"));
    expect(screen.queryByLabelText(/from/i)).not.toBeInTheDocument();
  });

  // ─── Current values in inputs ──────────────────────────

  it("populates From input with yearStart value", async () => {
    const user = userEvent.setup();
    render(
      <YearRangeDropdown yearStart={2018} onChange={mockOnChange} />
    );
    await user.click(screen.getByRole("button", { name: /year/i }));
    expect(screen.getByLabelText(/from/i)).toHaveValue(2018);
  });

  it("populates To input with yearEnd value", async () => {
    const user = userEvent.setup();
    render(
      <YearRangeDropdown yearEnd={2022} onChange={mockOnChange} />
    );
    await user.click(screen.getByRole("button", { name: /year/i }));
    expect(screen.getByLabelText(/to/i)).toHaveValue(2022);
  });

  // ─── onChange callbacks ────────────────────────────────

  it("calls onChange with yearStart when From input changes", async () => {
    const user = userEvent.setup();
    render(
      <YearRangeDropdown onChange={mockOnChange} />
    );
    await user.click(screen.getByRole("button", { name: /^year/i }));
    // Use fireEvent.change for number inputs — userEvent.type fires per-keystroke
    // which causes jsdom to emit each digit individually rather than the full value.
    fireEvent.change(screen.getByLabelText(/from/i), { target: { value: "2019" } });
    expect(mockOnChange).toHaveBeenLastCalledWith(
      expect.objectContaining({ yearStart: 2019 })
    );
  });

  it("calls onChange with yearEnd when To input changes", async () => {
    const user = userEvent.setup();
    render(
      <YearRangeDropdown onChange={mockOnChange} />
    );
    await user.click(screen.getByRole("button", { name: /^year/i }));
    fireEvent.change(screen.getByLabelText(/to/i), { target: { value: "2024" } });
    expect(mockOnChange).toHaveBeenLastCalledWith(
      expect.objectContaining({ yearEnd: 2024 })
    );
  });

  it("calls onChange with undefined yearStart when From input is cleared", async () => {
    const user = userEvent.setup();
    render(
      <YearRangeDropdown yearStart={2020} onChange={mockOnChange} />
    );
    await user.click(screen.getByRole("button", { name: /year/i }));
    await user.clear(screen.getByLabelText(/from/i));
    expect(mockOnChange).toHaveBeenLastCalledWith(
      expect.objectContaining({ yearStart: undefined })
    );
  });

  it("calls onChange with undefined yearEnd when To input is cleared", async () => {
    const user = userEvent.setup();
    render(
      <YearRangeDropdown yearEnd={2022} onChange={mockOnChange} />
    );
    await user.click(screen.getByRole("button", { name: /year/i }));
    await user.clear(screen.getByLabelText(/to/i));
    expect(mockOnChange).toHaveBeenLastCalledWith(
      expect.objectContaining({ yearEnd: undefined })
    );
  });
});
