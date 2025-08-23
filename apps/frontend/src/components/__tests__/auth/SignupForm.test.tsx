import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import SignupForm from "../../auth/SignupForm";

describe("SignupForm", () => {
  it("disables the submit button when loading", () => {
    render(<SignupForm isLoading={true} />);
    const button = screen.getByRole("button", { name: /signing up/i });
    expect(button).toBeDisabled();
  });

  it("shows error messages when error prop is set", () => {
    render(<SignupForm error="Something went wrong" />);
    expect(screen.getByText(/something went wrong/i)).toBeInTheDocument();
  });

  it("calls onSubmit with correct values", () => {
    const handleSubmit = jest.fn();
    render(<SignupForm onSubmit={handleSubmit} />);
    fireEvent.change(screen.getByLabelText(/username/i), {
      target: { value: "testuser" },
    });
    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: "test@example.com" },
    });
    fireEvent.change(screen.getByLabelText(/^password$/i), {
      target: { value: "password123" },
    });
    fireEvent.change(screen.getByLabelText(/confirm password/i), {
      target: { value: "password123" },
    });
    fireEvent.click(screen.getByRole("button", { name: /sign up/i }));
    expect(handleSubmit).toHaveBeenCalledWith({
      username: "testuser",
      email: "test@example.com",
      password: "password123",
      confirmPassword: "password123",
    });
  });

  it("does not call onSubmit if required fields are missing", () => {
    const handleSubmit = jest.fn();
    render(<SignupForm onSubmit={handleSubmit} />);
    fireEvent.click(screen.getByRole("button", { name: /sign up/i }));
    // Since we have required fields now, the browser will prevent form submission
    // when required fields are empty, so onSubmit should not be called
    expect(handleSubmit).not.toHaveBeenCalled();
  });
});
