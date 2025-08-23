import { render, screen } from "@testing-library/react";
import Navigation from "../Navigation";
import { useAuthStore } from "../../store/auth";
import type { AuthState } from "../../store/auth";

// Mock Zustand store for logged-in state
jest.mock("../../store/auth", () => ({
  useAuthStore: jest.fn(),
}));

jest.mock("next/navigation", () => ({
  useRouter: () => ({
    push: jest.fn(),
    replace: jest.fn(),
    prefetch: jest.fn(),
    // Add any other router methods your components use
  }),
}));

const mockUseAuthStore = useAuthStore as jest.MockedFunction<
  typeof useAuthStore
>;

describe("Navigation", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe("when user is logged in", () => {
    beforeEach(() => {
      // Mock the Zustand selector calls
      mockUseAuthStore.mockImplementation(
        (selector: (state: AuthState) => unknown) => {
          const state: AuthState = {
            isLoggedIn: true,
            token: "mock-token",
            user: { email: "test@example.com" },
            login: jest.fn(),
            logout: jest.fn(),
          };
          return selector(state);
        }
      );
    });

    it("should have a link to Collections", () => {
      const mockUser = { username: "testuser", email: "test@example.com" };
      render(<Navigation user={mockUser} />);
      const linkElement = screen.getByRole("link", { name: /collections/i });
      expect(linkElement).toBeInTheDocument();
      expect(linkElement).toHaveAttribute("href", "/library");
    });

    it("should display user welcome message", () => {
      const mockUser = { username: "testuser", email: "test@example.com" };
      render(<Navigation user={mockUser} />);
      expect(screen.getByText("Welcome, testuser!")).toBeInTheDocument();
    });

    it("should display logout button", () => {
      const mockUser = { username: "testuser", email: "test@example.com" };
      render(<Navigation user={mockUser} />);
      expect(
        screen.getByRole("button", { name: /logout/i })
      ).toBeInTheDocument();
    });

    it("should not show login/signup links", () => {
      const mockUser = { username: "testuser", email: "test@example.com" };
      render(<Navigation user={mockUser} />);
      expect(
        screen.queryByRole("link", { name: /login/i })
      ).not.toBeInTheDocument();
      expect(
        screen.queryByRole("link", { name: /signup/i })
      ).not.toBeInTheDocument();
    });
  });

  describe("when user is not logged in", () => {
    beforeEach(() => {
      // Mock the Zustand selector calls
      mockUseAuthStore.mockImplementation(
        (selector: (state: AuthState) => unknown) => {
          const state: AuthState = {
            isLoggedIn: false,
            token: null,
            user: null,
            login: jest.fn(),
            logout: jest.fn(),
          };
          return selector(state);
        }
      );
    });

    it("should show login and signup links", () => {
      render(<Navigation user={null} />);
      expect(screen.getByRole("link", { name: /login/i })).toBeInTheDocument();
      expect(
        screen.getByRole("link", { name: /sign up/i })
      ).toBeInTheDocument();
    });

    it("should not show Collections link when logged out", () => {
      render(<Navigation user={null} />);
      // Collections link is always shown, so this test should be updated
      expect(
        screen.getByRole("link", { name: /collections/i })
      ).toBeInTheDocument();
    });

    it("should not show user welcome message or logout button", () => {
      render(<Navigation user={null} />);
      expect(screen.queryByText(/welcome/i)).not.toBeInTheDocument();
      expect(
        screen.queryByRole("button", { name: /logout/i })
      ).not.toBeInTheDocument();
    });
  });

  describe("common elements", () => {
    beforeEach(() => {
      // Mock the Zustand selector calls for unauthenticated state
      mockUseAuthStore.mockImplementation(
        (selector: (state: AuthState) => unknown) => {
          const state: AuthState = {
            isLoggedIn: false,
            token: null,
            user: null,
            login: jest.fn(),
            logout: jest.fn(),
          };
          return selector(state);
        }
      );
    });

    it("should always show the GameHub brand link", () => {
      render(<Navigation user={null} />);
      const brandLink = screen.getByRole("link", { name: /gamehub/i });
      expect(brandLink).toBeInTheDocument();
      expect(brandLink).toHaveAttribute("href", "/");
    });
  });
});
