import { useAuthStore } from "../auth";

describe("Auth Store", () => {
  beforeEach(() => {
    // Reset the store state before each test
    useAuthStore.getState().logout();
  });

  describe("initial state", () => {
    it("should have correct initial state", () => {
      const state = useAuthStore.getState();
      expect(state.isLoggedIn).toBe(false);
      expect(state.token).toBe(null);
      expect(state.user).toBe(null);
    });
  });

  describe("login method", () => {
    it("should update state correctly when logging in", () => {
      const testToken = "test-jwt-token";
      const testUser = { id: 1, email: "test@example.com" };

      useAuthStore.getState().login(testToken, testUser);

      const state = useAuthStore.getState();
      expect(state.isLoggedIn).toBe(true);
      expect(state.token).toBe(testToken);
      expect(state.user).toBe(testUser);
    });

    it("should handle login without user data", () => {
      const testToken = "test-jwt-token";

      useAuthStore.getState().login(testToken);

      const state = useAuthStore.getState();
      expect(state.isLoggedIn).toBe(true);
      expect(state.token).toBe(testToken);
      expect(state.user).toBe(undefined);
    });
  });

  describe("logout method", () => {
    it("should clear all auth state when logging out", () => {
      // First login to have some state
      const testToken = "test-jwt-token";
      const testUser = { id: 1, email: "test@example.com" };
      useAuthStore.getState().login(testToken, testUser);

      // Verify we're logged in
      expect(useAuthStore.getState().isLoggedIn).toBe(true);

      // Now logout
      useAuthStore.getState().logout();

      // Verify all state is cleared
      const state = useAuthStore.getState();
      expect(state.isLoggedIn).toBe(false);
      expect(state.token).toBe(null);
      expect(state.user).toBe(null);
    });

    it("should work correctly when called multiple times", () => {
      // Login first
      useAuthStore.getState().login("token", { id: 1 });

      // Logout multiple times
      useAuthStore.getState().logout();
      useAuthStore.getState().logout();

      // Should still be logged out
      const state = useAuthStore.getState();
      expect(state.isLoggedIn).toBe(false);
      expect(state.token).toBe(null);
      expect(state.user).toBe(null);
    });
  });
});
