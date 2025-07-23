import React from "react";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import LoginPage from "../page";

// Define mock functions that will be shared
const mockApi = jest.fn();
const mockSetItem = jest.fn();
const mockLogin = jest.fn();
const mockPush = jest.fn();

// Mock Zustand auth store module - use a factory function to ensure fresh mocks
jest.mock("../../../../store/auth", () => ({
  useAuthStore: jest.fn(),
}));

// Mock next/navigation
jest.mock("next/navigation", () => ({
  useRouter: jest.fn(),
}));

// Import the mocked modules after mocking
import { useAuthStore } from "../../../../store/auth";
import { useRouter } from "next/navigation";

// Cast to jest mocks
const mockUseAuthStore = useAuthStore as jest.MockedFunction<
  typeof useAuthStore
>;
const mockUseRouter = useRouter as jest.MockedFunction<typeof useRouter>;

// Mock fetch at the global level
global.fetch = mockApi;

// Mock global fetch and localStorage
const localStorageMock = {
  setItem: mockSetItem,
  getItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
  key: jest.fn(),
  length: 0,
};

global.localStorage = localStorageMock;

// Ensure localStorage is properly defined
Object.defineProperty(window, "localStorage", {
  value: localStorageMock,
  writable: true,
});

beforeEach(() => {
  // Reset all mocks before each test
  mockApi.mockReset();
  mockSetItem.mockReset();
  mockLogin.mockReset();
  mockPush.mockReset();

  // Clear any previous mock implementations
  mockApi.mockClear();

  // Configure Zustand store mock
  mockUseAuthStore.mockImplementation((selector) => {
    const store = {
      login: mockLogin,
      logout: jest.fn(),
      user: null,
      token: null,
      isLoggedIn: false,
    };
    return selector ? selector(store) : store;
  });

  // Configure router mock
  mockUseRouter.mockReturnValue({
    push: mockPush,
    back: jest.fn(),
    forward: jest.fn(),
    refresh: jest.fn(),
    replace: jest.fn(),
    prefetch: jest.fn(),
  });
});

// Test suite for login flow
describe("LoginPage integration", () => {
  it("submits login form, stores token, updates global auth state, and redirects user", async () => {
    const mockJsonFn = jest.fn().mockResolvedValue({ token: "fake-jwt-token" });
    const mockResponse = { ok: true, json: mockJsonFn };
    mockApi.mockResolvedValueOnce(mockResponse);
    render(<LoginPage />);
    const user = userEvent.setup();
    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);
    const submitButton = screen.getByRole("button", { name: /login/i });
    await user.type(emailInput, "test@example.com");
    await user.type(passwordInput, "password123");
    expect(submitButton).not.toBeDisabled();
    expect(screen.queryByText(/logging in/i)).not.toBeInTheDocument();
    await user.click(submitButton);
    await waitFor(() => {
      expect(mockApi).toHaveBeenCalledWith(
        "http://localhost:8001/login",
        expect.objectContaining({
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            email: "test@example.com",
            password: "password123",
          }),
        })
      );
    });
    // Verify store login was called with correct token
    await waitFor(() => {
      expect(mockLogin).toHaveBeenCalledWith("fake-jwt-token", undefined);
    });
    // Verify redirect happened
    await waitFor(() => {
      expect(mockPush).toHaveBeenCalledWith("/");
    });
  });

  it("shows error if API returns no token in JSON (malformed response)", async () => {
    const mockJsonFn = jest.fn().mockResolvedValue({}); // No token
    const mockResponse = { ok: true, json: mockJsonFn };
    mockApi.mockResolvedValueOnce(mockResponse);
    render(<LoginPage />);
    const user = userEvent.setup();
    await user.type(screen.getByLabelText(/email/i), "test@example.com");
    await user.type(screen.getByLabelText(/password/i), "password123");
    await user.click(screen.getByRole("button", { name: /login/i }));
    await waitFor(() => {
      expect(
        screen.getByText(/invalid credentials|unexpected|error/i)
      ).toBeInTheDocument();
    });

    expect(mockLogin).not.toHaveBeenCalled();
    expect(mockPush).not.toHaveBeenCalled();
  });

  it("shows error if API returns invalid JSON (throws on .json())", async () => {
    const mockJsonFn = jest.fn().mockRejectedValue(new Error("Invalid JSON"));
    const mockResponse = { ok: true, json: mockJsonFn };
    mockApi.mockResolvedValueOnce(mockResponse);
    render(<LoginPage />);
    const user = userEvent.setup();
    await user.type(screen.getByLabelText(/email/i), "test@example.com");
    await user.type(screen.getByLabelText(/password/i), "password123");
    await user.click(screen.getByRole("button", { name: /login/i }));
    await waitFor(() => {
      expect(
        screen.getByText(/invalid credentials|unexpected|error/i)
      ).toBeInTheDocument();
    });

    expect(mockLogin).not.toHaveBeenCalled();
    expect(mockPush).not.toHaveBeenCalled();
  });

  it("shows error if network error occurs (fetch rejects)", async () => {
    mockApi.mockRejectedValueOnce(new Error("Network error"));
    render(<LoginPage />);
    const user = userEvent.setup();
    await user.type(screen.getByLabelText(/email/i), "test@example.com");
    await user.type(screen.getByLabelText(/password/i), "password123");
    await user.click(screen.getByRole("button", { name: /login/i }));
    await waitFor(() => {
      expect(screen.getByText(/network|unexpected|error/i)).toBeInTheDocument();
    });

    expect(mockLogin).not.toHaveBeenCalled();
    expect(mockPush).not.toHaveBeenCalled();
  });

  it("prevents multiple rapid submissions (button disables, only one request)", async () => {
    const mockJsonFn = jest.fn().mockResolvedValue({ token: "fake-jwt-token" });
    const mockResponse = { ok: true, json: mockJsonFn };
    mockApi.mockResolvedValueOnce(mockResponse);
    render(<LoginPage />);
    const user = userEvent.setup();
    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);
    const submitButton = screen.getByRole("button", { name: /login/i });
    await user.type(emailInput, "test@example.com");
    await user.type(passwordInput, "password123");
    // Rapidly click submit multiple times
    await Promise.all([
      user.click(submitButton),
      user.click(submitButton),
      user.click(submitButton),
    ]);
    await waitFor(() => {
      expect(mockApi).toHaveBeenCalledTimes(1);
    });
    await waitFor(() => {
      expect(submitButton).not.toBeDisabled();
    });
  });

  // Note: Zustand persistence now handles token rehydration automatically
  // so we don't need a specific test for localStorage rehydration

  it("shows error message on failed login", async () => {
    mockApi.mockResolvedValueOnce({ ok: false });
    render(<LoginPage />);
    const user = userEvent.setup();
    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);
    const submitButton = screen.getByRole("button", { name: /login/i });

    await user.type(emailInput, "wrong@example.com");
    await user.type(passwordInput, "badpassword");
    await user.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/invalid credentials/i)).toBeInTheDocument();
      expect(submitButton).not.toBeDisabled();
    });
  });
});
