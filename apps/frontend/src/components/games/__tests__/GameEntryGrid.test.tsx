import React from "react";
import { render, screen } from "@testing-library/react";
import GameEntryGrid from "../GameEntryGrid";

describe("GameEntryGrid", () => {
  const mockEntries = [
    {
      id: 1,
      collection_id: 42,
      game_id: 101,
      notes: "Amazing RPG",
      status: "completed",
      rating: 9,
      custom_tags: { genre: "rpg" },
      added_at: "2025-07-30T12:00:00Z",
      game: {
        id: 101,
        name: "Test RPG",
        platform: "PC",
        cover_url: "https://example.com/rpg.jpg",
      },
    },
    {
      id: 2,
      collection_id: 42,
      game_id: 102,
      notes: "Great shooter",
      status: "playing",
      rating: 8,
      custom_tags: { genre: "fps" },
      added_at: "2025-07-31T14:30:00Z",
      game: {
        id: 102,
        name: "Test Shooter",
        platform: "PlayStation",
        cover_url: "https://example.com/shooter.jpg",
      },
    },
  ];

  it("renders multiple game entry cards", () => {
    render(<GameEntryGrid entries={mockEntries} />);

    // Should show both games by their names and notes
    expect(screen.getByText("Test RPG")).toBeInTheDocument();
    expect(screen.getByText("Test Shooter")).toBeInTheDocument();
    expect(screen.getByText("Amazing RPG")).toBeInTheDocument();
    expect(screen.getByText("Great shooter")).toBeInTheDocument();
  });

  it("renders empty state when no entries", () => {
    render(<GameEntryGrid entries={[]} />);

    expect(
      screen.getByText(/no games yet!/i)
    ).toBeInTheDocument();
  });

  it("applies grid styling", () => {
    const { container } = render(<GameEntryGrid entries={mockEntries} />);

    expect(container.firstChild).toHaveClass("game-entry-grid");
  });
});
