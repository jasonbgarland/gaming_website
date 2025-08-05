import type { Config } from "jest";

const config: Config = {
  testEnvironment: "jsdom",
  preset: "ts-jest",
  roots: ["<rootDir>/src"],
  moduleFileExtensions: ["ts", "tsx", "js", "jsx", "json"],
  setupFilesAfterEnv: ["<rootDir>/jest.setup.ts"],
  transform: {
    "^.+\\.(ts|tsx)$": [
      "ts-jest",
      {
        tsconfig: {
          jsx: "react-jsx",
        },
      },
    ],
  },
  testMatch: ["**/__tests__/**/*.(test|spec).(ts|tsx|js|jsx)"],
  moduleNameMapper: {
    // Handle CSS imports (if using CSS modules)
    "\\.(css|less|scss|sass)$": "identity-obj-proxy",
    // Handle static assets
    "\\.(jpg|jpeg|png|gif|webp|svg)$": "<rootDir>/__mocks__/fileMock.js",
    // Support absolute imports from src directory (matching tsconfig baseUrl)
    "^services/(.*)$": "<rootDir>/src/services/$1",
    "^components/(.*)$": "<rootDir>/src/components/$1",
    "^hooks/(.*)$": "<rootDir>/src/hooks/$1",
    "^store/(.*)$": "<rootDir>/src/store/$1",
    "^utils/(.*)$": "<rootDir>/src/utils/$1",
    "^types/(.*)$": "<rootDir>/src/types/$1",
    // Handle @/* imports (if we want to use them)
    "^@/(.*)$": "<rootDir>/src/$1",
  },
};

export default config;
