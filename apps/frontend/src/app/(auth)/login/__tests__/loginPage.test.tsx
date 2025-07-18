jest.mock("next/navigation", () => ({
  useRouter: () => ({
    push: jest.fn(),
    back: jest.fn(),
    forward: jest.fn(),
    refresh: jest.fn(),
    replace: jest.fn(),
    prefetch: jest.fn(),
  }),
}));
import React from "react";
import { render, screen } from "@testing-library/react";
import LoginPage from "../page";
jest.mock("next/navigation", () => ({
  useRouter: () => ({
    push: jest.fn(),
    back: jest.fn(),
    forward: jest.fn(),
    refresh: jest.fn(),
    replace: jest.fn(),
    prefetch: jest.fn(),
  }),
}));

// Test suite for the /login page

describe("/login page", () => {
  it("renders the LoginForm component", () => {
    render(<LoginPage />);
    // Check for the presence of the LoginForm by its email input
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    // Optionally, check for a heading
    // expect(screen.getByRole('heading', { name: /login/i })).toBeInTheDocument();
  });
});
