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

    it("should have a link to My Library", () => {
      render(<Navigation />);
      const linkElement = screen.getByRole("link", { name: /my library/i });
      expect(linkElement).toBeInTheDocument();
      expect(linkElement).toHaveAttribute("href", "/library");
    });

    it("should display user email", () => {
      render(<Navigation />);
      expect(screen.getByText("test@example.com")).toBeInTheDocument();
    });

    it("should display logout button", () => {
      render(<Navigation />);
      expect(
        screen.getByRole("button", { name: /logout/i })
      ).toBeInTheDocument();
    });

    it("should not show login/signup links", () => {
      render(<Navigation />);
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
      render(<Navigation />);
      expect(screen.getByRole("link", { name: /login/i })).toBeInTheDocument();
      expect(screen.getByRole("link", { name: /signup/i })).toBeInTheDocument();
    });

    it("should not show My Library link", () => {
      render(<Navigation />);
      expect(
        screen.queryByRole("link", { name: /my library/i })
      ).not.toBeInTheDocument();
    });

    it("should not show user email or logout button", () => {
      render(<Navigation />);
      expect(screen.queryByText("test@example.com")).not.toBeInTheDocument();
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

    it("should always show the Gaming Website brand link", () => {
      render(<Navigation />);
      const brandLink = screen.getByRole("link", { name: /gaming website/i });
      expect(brandLink).toBeInTheDocument();
      expect(brandLink).toHaveAttribute("href", "/");
    });
  });
});
