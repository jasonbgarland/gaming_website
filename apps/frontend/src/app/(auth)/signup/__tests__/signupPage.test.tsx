import React from "react";
import { render, screen } from "@testing-library/react";
import SignupPage from "../page";

jest.mock("next/navigation", () => ({
  useRouter: jest.fn(() => ({
    push: jest.fn(),
    back: jest.fn(),
    forward: jest.fn(),
    refresh: jest.fn(),
    replace: jest.fn(),
    prefetch: jest.fn(),
  })),
}));

describe("/signup page", () => {
  it("renders the SignupForm component", () => {
    render(<SignupPage />);
    // Check for the presence of the SignupForm by its email input
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    // Optionally, check for a heading
    // expect(screen.getByRole('heading', { name: /sign up/i })).toBeInTheDocument();
  });
});
