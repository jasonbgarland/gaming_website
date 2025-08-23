"use client";

import React, { useState } from "react";

type LoginFormProps = {
  onSubmit?: (data: { email: string; password: string }) => void;
  isLoading?: boolean;
  error?: string;
};

/**
 * LoginForm component for user authentication.
 * Renders a form with email and password fields and a submit button.
 */

const LoginForm: React.FC<LoginFormProps> = ({
  onSubmit,
  isLoading,
  error,
}) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit?.({ email, password });
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-gamer-surface p-6 rounded-lg border border-gamer-border space-y-4 max-w-md mx-auto"
    >
      <div>
        <label
          htmlFor="email"
          className="block text-gamer-text font-medium mb-2"
        >
          Email
        </label>
        <input
          id="email"
          name="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full px-3 py-2 bg-gamer-input border border-gamer-input-border rounded-md text-gamer-text placeholder-gamer-muted focus:outline-none focus:ring-2 focus:ring-gamer-primary focus:border-transparent"
          placeholder="Enter your email"
        />
      </div>

      <div>
        <label
          htmlFor="password"
          className="block text-gamer-text font-medium mb-2"
        >
          Password
        </label>
        <input
          id="password"
          name="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full px-3 py-2 bg-gamer-input border border-gamer-input-border rounded-md text-gamer-text placeholder-gamer-muted focus:outline-none focus:ring-2 focus:ring-gamer-primary focus:border-transparent"
          placeholder="Enter your password"
        />
      </div>

      {error && (
        <div className="bg-gamer-danger/10 border border-gamer-danger/20 text-gamer-danger px-3 py-2 rounded-md text-sm">
          {error}
        </div>
      )}

      <button
        type="submit"
        disabled={isLoading}
        className="w-full bg-gamer-primary hover:bg-gamer-primary-hover text-white font-medium py-3 px-4 rounded-md transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {isLoading ? "Logging in..." : "Login"}
      </button>
    </form>
  );
};

export default LoginForm;
