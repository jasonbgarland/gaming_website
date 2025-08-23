"use client";

import React from "react";
import SignupForm from "../../../components/auth/SignupForm";
import { useSignup } from "./useSignup";

/**
 * SignupPage component for the /signup route.
 * Renders the SignupForm for user registration.
 */
const SignupPage: React.FC = () => {
  const { handleSignup, isLoading, error } = useSignup();
  return (
    <main className="min-h-screen bg-gamer-dark flex items-center justify-center p-8">
      <div className="w-full max-w-md">
        <h1 className="text-3xl font-bold text-gamer-text mb-8 text-center">
          Sign Up
        </h1>
        <SignupForm
          onSubmit={handleSignup}
          isLoading={isLoading}
          error={error}
        />
      </div>
    </main>
  );
};

export default SignupPage;
