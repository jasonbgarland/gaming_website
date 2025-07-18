import { renderHook } from "@testing-library/react";
import { useLogout } from "../useLogout";
import { useAuthStore, User } from "../../../../store/auth";

// Mock the auth store
jest.mock("../../../../store/auth", () => ({
  useAuthStore: jest.fn(),
}));

// Mock next/navigation
const mockPush = jest.fn();
jest.mock("next/navigation", () => ({
  useRouter: jest.fn(() => ({
    push: mockPush,
  })),
}));

// Mock localStorage
const mockRemoveItem = jest.fn();
Object.defineProperty(window, "localStorage", {
  value: {
    removeItem: mockRemoveItem,
  },
  writable: true,
});

const mockUseAuthStore = useAuthStore as jest.MockedFunction<
  typeof useAuthStore
>;

interface AuthState {
  isLoggedIn: boolean;
  token: string | null;
  user: User | null;
  login: (token: string, user?: User) => void;
  logout: () => void;
}

describe("useLogout", () => {
  const mockLogout = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
    mockUseAuthStore.mockImplementation(
      (selector: (state: AuthState) => unknown) => {
        const fakeState: AuthState = {
          isLoggedIn: false,
          token: null,
          user: null,
          login: jest.fn(),
          logout: mockLogout,
        };
        if (selector) {
          return selector(fakeState);
        }
        return fakeState;
      }
    );
  });

  it("should return handleLogout function", () => {
    const { result } = renderHook(() => useLogout());

    expect(typeof result.current.handleLogout).toBe("function");
  });

  it("should call store logout and clear localStorage when handleLogout is called", () => {
    const { result } = renderHook(() => useLogout());

    result.current.handleLogout();

    expect(mockLogout).toHaveBeenCalledTimes(1);
    expect(mockRemoveItem).toHaveBeenCalledWith("token");
  });

  it("should redirect to login page after logout", () => {
    const { result } = renderHook(() => useLogout());

    result.current.handleLogout();

    expect(mockPush).toHaveBeenCalledWith("/login");
  });

  it("should work correctly when called multiple times", () => {
    const { result } = renderHook(() => useLogout());

    result.current.handleLogout();
    result.current.handleLogout();

    expect(mockLogout).toHaveBeenCalledTimes(2);
    expect(mockRemoveItem).toHaveBeenCalledTimes(2);
    expect(mockPush).toHaveBeenCalledTimes(2);
  });
});
