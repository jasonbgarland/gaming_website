import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import SignupForm from "../../../../components/auth/SignupForm";

describe("SignupForm", () => {
  it("renders email and password fields and a submit button", () => {
    render(<SignupForm />);
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText("Password")).toBeInTheDocument();
    expect(screen.getByLabelText("Confirm Password")).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: /Sign Up/i })
    ).toBeInTheDocument();
  });

  it("shows loading state when form is being submitted", () => {
    render(<SignupForm isLoading={true} />);
    const submitButton = screen.getByRole("button", { name: /signing up/i });
    expect(submitButton).toBeDisabled();
    expect(screen.getByText(/signing up/i)).toBeInTheDocument();
  });

  it("displays error message when provided", () => {
    const errorMessage = "Email already exists";
    render(<SignupForm error={errorMessage} />);
    expect(screen.getByText(errorMessage)).toBeInTheDocument();
  });

  it("allows user to type in email, password, and confirm password fields", async () => {
    const user = userEvent.setup();
    render(<SignupForm />);

    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText("Password");
    const confirmPasswordInput = screen.getByLabelText("Confirm Password");

    await user.type(emailInput, "test@example.com");
    await user.type(passwordInput, "password123");
    await user.type(confirmPasswordInput, "password123");

    expect(emailInput).toHaveValue("test@example.com");
    expect(passwordInput).toHaveValue("password123");
    expect(confirmPasswordInput).toHaveValue("password123");
  });

  it("calls onSubmit when form is submitted with valid data", async () => {
    const user = userEvent.setup();
    const mockOnSubmit = jest.fn();
    render(<SignupForm onSubmit={mockOnSubmit} />);

    const usernameInput = screen.getByLabelText(/username/i);
    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText("Password");
    const confirmPasswordInput = screen.getByLabelText("Confirm Password");
    const submitButton = screen.getByRole("button", { name: /Sign Up/i });

    await user.type(usernameInput, "testuser");
    await user.type(emailInput, "test@example.com");
    await user.type(passwordInput, "password123");
    await user.type(confirmPasswordInput, "password123");
    await user.click(submitButton);

    expect(mockOnSubmit).toHaveBeenCalledWith({
      username: "testuser",
      email: "test@example.com",
      password: "password123",
      confirmPassword: "password123",
    });
  });
});
