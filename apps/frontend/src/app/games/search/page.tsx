import { EnhancedGameSearch } from "@components/games/EnhancedGameSearch";

export default function GameSearchPage() {
  return (
    <main className="min-h-screen bg-gamer-dark p-8">
      <div className="container mx-auto px-4">
        <h1 className="text-3xl font-bold mb-8 text-gamer-text">
          Search Games
        </h1>
        {/* platformOptions and genreOptions will be populated in task 2 (API fetch) */}
        <EnhancedGameSearch platformOptions={[]} genreOptions={[]} />
      </div>
    </main>
  );
}
