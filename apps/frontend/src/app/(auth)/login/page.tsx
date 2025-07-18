"use client";

import React from "react";
import LoginForm from "./components/LoginForm";
import { useLogin } from "./useLogin";

/**
 * LoginPage component for the /login route.
 * Renders the LoginForm for user authentication.
 */
const LoginPage: React.FC = () => {
  const { handleLogin, isLoading, error } = useLogin();
  return (
    <main>
      <h1>Login</h1>
      <LoginForm onSubmit={handleLogin} isLoading={isLoading} error={error} />
    </main>
  );
};

export default LoginPage;
