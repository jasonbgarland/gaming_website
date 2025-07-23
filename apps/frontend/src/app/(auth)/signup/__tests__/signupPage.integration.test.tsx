import React from "react";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import SignupPage from "../page";

// Shared mocks
const mockApi = jest.fn();
const mockSetItem = jest.fn();
const mockLogin = jest.fn();
const mockPush = jest.fn();

jest.mock("../../../../store/auth", () => ({
  useAuthStore: jest.fn(),
}));
jest.mock("next/navigation", () => ({
  useRouter: jest.fn(),
}));
import { useAuthStore } from "../../../../store/auth";
import { useRouter } from "next/navigation";
const mockUseAuthStore = useAuthStore as jest.MockedFunction<
  typeof useAuthStore
>;
const mockUseRouter = useRouter as jest.MockedFunction<typeof useRouter>;

global.fetch = mockApi;
const localStorageMock = {
  setItem: mockSetItem,
  getItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
  key: jest.fn(),
  length: 0,
};
global.localStorage = localStorageMock;
Object.defineProperty(window, "localStorage", {
  value: localStorageMock,
  writable: true,
});
const localStorageSetItemSpy = jest.spyOn(Storage.prototype, "setItem");
localStorageSetItemSpy.mockImplementation(mockSetItem);

beforeEach(() => {
  mockApi.mockReset();
  mockSetItem.mockReset();
  mockLogin.mockReset();
  mockPush.mockReset();
  localStorageSetItemSpy.mockReset();
  mockApi.mockClear();
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
  mockUseRouter.mockReturnValue({
    push: mockPush,
    back: jest.fn(),
    forward: jest.fn(),
    refresh: jest.fn(),
    replace: jest.fn(),
    prefetch: jest.fn(),
  });
});

describe("SignupPage integration", () => {
  it("submits signup form, stores token, updates global auth state, and redirects user", async () => {
    const mockJsonFn = jest.fn().mockResolvedValue({
      access_token: "fake-jwt-token",
      token_type: "bearer",
    });
    const mockResponse = { ok: true, json: mockJsonFn };
    mockApi.mockResolvedValueOnce(mockResponse);
    render(<SignupPage />);
    const user = userEvent.setup();
    const usernameInput = screen.getByLabelText(/username/i);
    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/^password$/i);
    const confirmInput = screen.getByLabelText(/confirm password/i);
    const submitButton = screen.getByRole("button", { name: /sign up/i });
    await user.type(usernameInput, "testuser");
    await user.type(emailInput, "test@example.com");
    await user.type(passwordInput, "password123");
    await user.type(confirmInput, "password123");
    expect(submitButton).not.toBeDisabled();
    await user.click(submitButton);
    await waitFor(() => {
      expect(mockApi).toHaveBeenCalledWith(
        "http://localhost:8001/signup",
        expect.objectContaining({
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            username: "testuser",
            email: "test@example.com",
            password: "password123",
          }),
        })
      );
    });
    // Verify store login was called with correct token
    await waitFor(() => {
      expect(mockLogin).toHaveBeenCalledWith("fake-jwt-token");
    });
    // Verify redirect happened
    await waitFor(() => {
      expect(mockPush).toHaveBeenCalledWith("/");
    });
  });

  it("shows error message on failed signup", async () => {
    mockApi.mockResolvedValueOnce({ ok: false });
    render(<SignupPage />);
    const user = userEvent.setup();
    await user.type(screen.getByLabelText(/username/i), "failuser");
    await user.type(screen.getByLabelText(/email/i), "fail@example.com");
    await user.type(screen.getByLabelText(/^password$/i), "badpassword");
    await user.type(screen.getByLabelText(/confirm password/i), "badpassword");
    await user.click(screen.getByRole("button", { name: /sign up/i }));
    await waitFor(() => {
      expect(screen.getByText(/invalid|error/i)).toBeInTheDocument();
    });
  });

  it("shows error on duplicate email/username (409)", async () => {
    mockApi.mockResolvedValueOnce({ ok: false, status: 409 });
    render(<SignupPage />);
    const user = userEvent.setup();
    await user.type(screen.getByLabelText(/username/i), "dupeuser");
    await user.type(screen.getByLabelText(/email/i), "dupe@example.com");
    await user.type(screen.getByLabelText(/^password$/i), "password123");
    await user.type(screen.getByLabelText(/confirm password/i), "password123");
    await user.click(screen.getByRole("button", { name: /sign up/i }));
    await waitFor(() => {
      expect(screen.getByText(/invalid|error|duplicate/i)).toBeInTheDocument();
    });
  });

  it("shows error on weak password (422)", async () => {
    mockApi.mockResolvedValueOnce({ ok: false, status: 422 });
    render(<SignupPage />);
    const user = userEvent.setup();
    await user.type(screen.getByLabelText(/username/i), "weakuser");
    await user.type(screen.getByLabelText(/email/i), "weak@example.com");
    await user.type(screen.getByLabelText(/^password$/i), "123");
    await user.type(screen.getByLabelText(/confirm password/i), "123");
    await user.click(screen.getByRole("button", { name: /sign up/i }));
    await waitFor(() => {
      expect(screen.getByText(/invalid|error|weak/i)).toBeInTheDocument();
    });
  });

  it("shows error on network error (fetch rejects)", async () => {
    mockApi.mockRejectedValueOnce(new Error("Network error"));
    render(<SignupPage />);
    const user = userEvent.setup();
    await user.type(screen.getByLabelText(/username/i), "netuser");
    await user.type(screen.getByLabelText(/email/i), "netfail@example.com");
    await user.type(screen.getByLabelText(/^password$/i), "password123");
    await user.type(screen.getByLabelText(/confirm password/i), "password123");
    await user.click(screen.getByRole("button", { name: /sign up/i }));
    await waitFor(() => {
      expect(screen.getByText(/network|error/i)).toBeInTheDocument();
    });
  });

  it("form fields stay filled after error", async () => {
    mockApi.mockResolvedValueOnce({ ok: false });
    render(<SignupPage />);
    const user = userEvent.setup();
    const usernameInput = screen.getByLabelText(/username/i);
    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/^password$/i);
    const confirmInput = screen.getByLabelText(/confirm password/i);
    await user.type(usernameInput, "failuser");
    await user.type(emailInput, "fail@example.com");
    await user.type(passwordInput, "badpassword");
    await user.type(confirmInput, "badpassword");
    await user.click(screen.getByRole("button", { name: /sign up/i }));
    await waitFor(() => {
      expect(screen.getByText(/invalid|error/i)).toBeInTheDocument();
    });
    expect(usernameInput).toHaveValue("failuser");
    expect(emailInput).toHaveValue("fail@example.com");
    expect(passwordInput).toHaveValue("badpassword");
    expect(confirmInput).toHaveValue("badpassword");
  });
});
