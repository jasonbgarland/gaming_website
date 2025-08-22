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
    <main>
      <h1>Sign Up</h1>
      <SignupForm onSubmit={handleSignup} isLoading={isLoading} error={error} />
    </main>
  );
};

export default SignupPage;
