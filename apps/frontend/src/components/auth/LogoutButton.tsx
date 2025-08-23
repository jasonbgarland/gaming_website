"use client";

import React from "react";
import { useLogout } from "../../app/(auth)/logout/useLogout";

type LogoutButtonProps = {
  className?: string;
  children?: React.ReactNode;
};

/**
 * LogoutButton component for user logout functionality.
 * Uses the useLogout hook to handle logout process.
 */
const LogoutButton: React.FC<LogoutButtonProps> = ({
  className,
  children = "Logout",
}) => {
  const { handleLogout } = useLogout();

  return (
    <button
      type="button"
      onClick={handleLogout}
      className={
        className ||
        "bg-gamer-secondary hover:bg-gamer-secondary-hover text-gamer-text font-medium px-4 py-2 rounded-md transition-colors duration-200 border border-gamer-border"
      }
    >
      {children}
    </button>
  );
};

export default LogoutButton;
