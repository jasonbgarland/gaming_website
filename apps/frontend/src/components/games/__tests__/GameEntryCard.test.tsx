import React from "react";
import { render, screen } from "@testing-library/react";
import GameEntryCard from "../GameEntryCard";

describe("GameEntryCard", () => {
  const mockEntry = {
    id: 1,
    collection_id: 42,
    game_id: 101,
    notes: "Amazing RPG with great story",
    status: "completed",
    rating: 9,
    custom_tags: { genre: "rpg", platform: "pc" },
    added_at: "2025-07-30T12:00:00Z",
    game: {
      id: 101,
      igdb_id: 1234,
      name: "Test Game",
      platform: "PC",
      cover_url: "https://example.com/cover.jpg",
      genre: "RPG",
    },
  };

  it("renders game entry information", () => {
    render(<GameEntryCard entry={mockEntry} />);

    // Should show game name and platform
    expect(screen.getByText("Test Game")).toBeInTheDocument();
    expect(screen.getByText("PC")).toBeInTheDocument();

    // Should show user's notes
    expect(
      screen.getByText("Amazing RPG with great story")
    ).toBeInTheDocument();

    // Should show status
    expect(screen.getByText(/completed/i)).toBeInTheDocument();

    // Should show rating
    expect(screen.getByText("9/10")).toBeInTheDocument();

    // Should show custom tags
    expect(screen.getByText("Tags:")).toBeInTheDocument();
    // Check for tags specifically in the tags section
    const tagsSection = screen.getByText("Tags:").parentElement;
    expect(tagsSection).toHaveTextContent("rpg");
    expect(tagsSection).toHaveTextContent("pc");
  });

  it("renders entry without optional fields", () => {
    const minimalEntry = {
      id: 2,
      collection_id: 42,
      game_id: 102,
      game: {
        id: 102,
        name: "Minimal Game",
        platform: "PlayStation",
      },
    };

    render(<GameEntryCard entry={minimalEntry} />);

    // Should not crash when optional fields are missing
    // Should show game name and platform
    expect(screen.getByText("Minimal Game")).toBeInTheDocument();
    expect(screen.getByText("PlayStation")).toBeInTheDocument();
  });

  it("applies correct styling classes", () => {
    const { container } = render(<GameEntryCard entry={mockEntry} />);

    // Should have gamer theme card styling
    expect(container.firstChild).toHaveClass("bg-gamer-surface");
    expect(container.firstChild).toHaveClass("border-gamer-border");
    expect(container.firstChild).toHaveClass("rounded-lg");
  });
});
