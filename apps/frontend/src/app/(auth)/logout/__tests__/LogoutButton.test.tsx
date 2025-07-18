import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import LogoutButton from "../components/LogoutButton";

// Mock the useLogout hook
const mockHandleLogout = jest.fn();
jest.mock("../useLogout", () => ({
  useLogout: jest.fn(() => ({
    handleLogout: mockHandleLogout,
  })),
}));

describe("LogoutButton", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("renders a logout button", () => {
    render(<LogoutButton />);

    const button = screen.getByRole("button", { name: /logout/i });
    expect(button).toBeInTheDocument();
  });

  it("calls handleLogout when clicked", async () => {
    const user = userEvent.setup();
    render(<LogoutButton />);

    const button = screen.getByRole("button", { name: /logout/i });
    await user.click(button);

    expect(mockHandleLogout).toHaveBeenCalledTimes(1);
  });

  it("can accept custom className", () => {
    render(<LogoutButton className="custom-class" />);

    const button = screen.getByRole("button", { name: /logout/i });
    expect(button).toHaveClass("custom-class");
  });

  it("can accept custom children", () => {
    render(<LogoutButton>Sign Out</LogoutButton>);

    const button = screen.getByRole("button", { name: "Sign Out" });
    expect(button).toBeInTheDocument();
  });
});
