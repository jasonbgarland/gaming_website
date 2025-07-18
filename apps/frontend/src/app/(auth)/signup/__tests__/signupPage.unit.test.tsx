import React from "react";
import { render } from "@testing-library/react";
import SignupPage from "../page";
import SignupForm from "../components/SignupForm";

jest.mock("../components/SignupForm", () => jest.fn(() => null));
jest.mock("../useSignup", () => ({
  useSignup: jest.fn(() => ({
    handleSignup: jest.fn(),
    isLoading: false,
    error: "",
  })),
}));
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

describe("SignupPage", () => {
  it("passes correct props to SignupForm", () => {
    render(<SignupPage />);
    expect(SignupForm).toHaveBeenCalledWith(
      expect.objectContaining({
        onSubmit: expect.any(Function),
        isLoading: expect.any(Boolean),
        error: expect.any(String),
      }),
      undefined
    );
  });
});
