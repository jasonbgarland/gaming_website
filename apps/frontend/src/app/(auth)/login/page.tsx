"use client";

import React from "react";
import LoginForm from "../../../components/auth/LoginForm";
import { useLogin } from "./useLogin";

/**
 * LoginPage component for the /login route.
 * Renders the LoginForm for user authentication.
 */
const LoginPage: React.FC = () => {
  const { handleLogin, isLoading, error } = useLogin();
  return (
    <main className="min-h-screen bg-gamer-dark flex items-center justify-center p-8">
      <div className="w-full max-w-md">
        <h1 className="text-3xl font-bold text-gamer-text mb-8 text-center">
          Login
        </h1>
        <LoginForm onSubmit={handleLogin} isLoading={isLoading} error={error} />
      </div>
    </main>
  );
};

export default LoginPage;
