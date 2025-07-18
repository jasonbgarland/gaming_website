"use client";

import React from "react";
import { useLogout } from "../useLogout";

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
    <button type="button" onClick={handleLogout} className={className}>
      {children}
    </button>
  );
};

export default LogoutButton;
