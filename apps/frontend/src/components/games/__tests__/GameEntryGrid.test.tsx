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
    },
  ];

  it("renders multiple game entry cards", () => {
    render(<GameEntryGrid entries={mockEntries} />);

    // Should show both game entries
    expect(screen.getByText("Game ID: 101")).toBeInTheDocument();
    expect(screen.getByText("Game ID: 102")).toBeInTheDocument();

    // Should show notes from both entries
    expect(screen.getByText("Amazing RPG")).toBeInTheDocument();
    expect(screen.getByText("Great shooter")).toBeInTheDocument();
  });

  it("renders empty state when no entries", () => {
    render(<GameEntryGrid entries={[]} />);

    expect(
      screen.getByText(/no games in this collection/i)
    ).toBeInTheDocument();
  });

  it("applies grid styling", () => {
    const { container } = render(<GameEntryGrid entries={mockEntries} />);

    expect(container.firstChild).toHaveClass("game-entry-grid");
  });
});
