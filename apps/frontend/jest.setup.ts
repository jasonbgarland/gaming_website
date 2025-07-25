import "@testing-library/jest-dom";

// Set up environment variables for tests
process.env.NEXT_PUBLIC_AUTH_API_URL = "http://localhost:8001";

// Suppress act warnings for async operations that are hard to control
// These warnings occur when async state updates happen in finally blocks
// after Promise rejections, which are difficult to wrap in act() properly
const originalError = console.error;

beforeAll(() => {
  console.error = (...args) => {
    if (
      typeof args[0] === "string" &&
      (args[0].includes("An update to") ||
        args[0].includes("was not wrapped in act") ||
        args[0].includes("Warning: An update to"))
    ) {
      // Suppress act warnings and expected error logs during tests
      return;
    }
    return originalError.call(console, ...args);
  };
});

afterAll(() => {
  console.error = originalError;
});
