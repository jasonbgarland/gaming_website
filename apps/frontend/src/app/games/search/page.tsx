import { GameSearch } from "@components/games/GameSearch";

export default function GameSearchPage() {
  return (
    <main className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Search Games</h1>
      <GameSearch />
    </main>
  );
}
