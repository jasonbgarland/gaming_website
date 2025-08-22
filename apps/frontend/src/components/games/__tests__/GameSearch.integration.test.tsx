import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import GameSearch from "../GameSearch";

// This test assumes your backend and IGDB integration are running and accessible.
// It will make a real request to the API Gateway endpoint.
// Make sure to set up any required environment variables or credentials before running.

// Skip this test unless INTEGRATION_TESTS environment variable is set
const runIntegrationTests = process.env.INTEGRATION_TESTS === "true";

describe("GameSearch integration (real IGDB data)", () => {
  // Use .skip to prevent this from running in regular test suites
  const testMethod = runIntegrationTests ? it : it.skip;

  testMethod(
    "fetches and displays real IGDB data via the backend",
    async () => {
      render(<GameSearch initialResults={[]} />);
      const input = screen.getByPlaceholderText("Search for games...");
      fireEvent.change(input, { target: { value: "Halo" } });

      // Wait for a real result to appear (may need to adjust timeout for network latency)
      await waitFor(
        () => {
          // Look for a known IGDB game title
          expect(screen.getByText(/halo/i)).toBeInTheDocument();
        },
        { timeout: 8000 }
      );
    }
  );
});
