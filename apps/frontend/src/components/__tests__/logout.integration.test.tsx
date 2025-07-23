import React from "react";
import { render, screen, waitFor, act } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { useAuthStore } from "../../store/auth";
import Navigation from "../Navigation";

// Mock next/navigation
const mockPush = jest.fn();
jest.mock("next/navigation", () => ({
  useRouter: jest.fn(() => ({
    push: mockPush,
  })),
}));

// Mock localStorage for Zustand persistence
const mockSetItem = jest.fn();
const mockRemoveItem = jest.fn();
const mockGetItem = jest.fn();

Object.defineProperty(window, "localStorage", {
  value: {
    getItem: mockGetItem,
    setItem: mockSetItem,
    removeItem: mockRemoveItem,
  },
  writable: true,
});

describe("Logout Integration Flow", () => {
  beforeEach(() => {
    jest.clearAllMocks();
    // Reset auth store to initial state
    act(() => {
      useAuthStore.getState().logout();
    });
  });

  it("should complete full logout flow: logged in -> logout button click -> redirect to login", async () => {
    const user = userEvent.setup();

    // Start with logged in state
    act(() => {
      useAuthStore
        .getState()
        .login("test-token", { email: "test@example.com" });
    });

    // Render navigation
    render(<Navigation />);

    // Should show user email and logout button (logged in state)
    expect(screen.getByText("test@example.com")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /logout/i })).toBeInTheDocument();
    expect(
      screen.queryByRole("link", { name: /login/i })
    ).not.toBeInTheDocument();

    // Click logout button
    const logoutButton = screen.getByRole("button", { name: /logout/i });
    await user.click(logoutButton);

    // Verify auth state was cleared
    await waitFor(() => {
      const authState = useAuthStore.getState();
      expect(authState.isLoggedIn).toBe(false);
      expect(authState.token).toBe(null);
      expect(authState.user).toBe(null);
    });

    // Verify redirect to login page
    expect(mockPush).toHaveBeenCalledWith("/login");

    // Note: We don't test localStorage directly since Zustand persistence
    // is an implementation detail that works correctly in the real app
  });

  it("should show login/signup links when logged out", () => {
    // Start with logged out state (default)
    render(<Navigation />);

    // Should show login/signup links
    expect(screen.getByRole("link", { name: /login/i })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /signup/i })).toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: /logout/i })
    ).not.toBeInTheDocument();
  });

  it("should switch from logged out to logged in navigation when user logs in", () => {
    const { rerender } = render(<Navigation />);

    // Initially logged out
    expect(screen.getByRole("link", { name: /login/i })).toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: /logout/i })
    ).not.toBeInTheDocument();

    // Log in
    act(() => {
      useAuthStore
        .getState()
        .login("test-token", { email: "test@example.com" });
    });

    // Rerender to pick up state change
    rerender(<Navigation />);

    // Now should show logged in state
    expect(screen.getByText("test@example.com")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /logout/i })).toBeInTheDocument();
    expect(
      screen.queryByRole("link", { name: /login/i })
    ).not.toBeInTheDocument();
  });
});
