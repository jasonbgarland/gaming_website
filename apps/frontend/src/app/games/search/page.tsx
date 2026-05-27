import { GameSearch } from "@components/games/GameSearch";
import { type FilterOption } from "@/components/filters/FilterDropdown";

interface GenreOut {
  id: number;
  name: string;
}

interface PlatformOut {
  id: number;
  name: string;
}

async function fetchPlatformsAndGenres(): Promise<{
  platforms: FilterOption[];
  genres: FilterOption[];
}> {
  // Server-side fetch needs internal Docker service name, not localhost
  const gameServiceUrl =
    process.env.GAME_SERVICE_INTERNAL_URL || // For server-side in Docker
    process.env.NEXT_PUBLIC_GAME_SERVICE_URL || // Fallback for local dev
    "http://localhost:8002";

  try {
    const fetchOptions =
      process.env.NODE_ENV === "development"
        ? { cache: "no-store" as RequestCache }
        : { next: { revalidate: 604800 } }; // 7 days in production

    const [platformsRes, genresRes] = await Promise.all([
      fetch(`${gameServiceUrl}/igdb/platforms`, fetchOptions),
      fetch(`${gameServiceUrl}/igdb/genres`, fetchOptions),
    ]);

    if (!platformsRes.ok || !genresRes.ok) {
      console.error("Failed to fetch filter options", {
        platformsStatus: platformsRes.status,
        genresStatus: genresRes.status,
      });
      return { platforms: [], genres: [] };
    }

    const [platformsData, genresData] = await Promise.all([
      platformsRes.json() as Promise<PlatformOut[]>,
      genresRes.json() as Promise<GenreOut[]>,
    ]);

    return {
      platforms: platformsData.map((p) => ({ id: p.id, label: p.name })),
      genres: genresData.map((g) => ({ id: g.id, label: g.name })),
    };
  } catch (err) {
    // Serialize error safely for Next.js
    const errorMessage = err instanceof Error ? err.message : String(err);
    console.error("Error fetching filter options:", errorMessage);
    return { platforms: [], genres: [] };
  }
}

export default async function GameSearchPage() {
  const { platforms, genres } = await fetchPlatformsAndGenres();

  return (
    <main className="min-h-screen bg-gamer-dark p-8">
      <div className="container mx-auto px-4">
        <h1 className="text-3xl font-bold mb-8 text-gamer-text">
          Search Games
        </h1>
        <GameSearch
          platformOptions={platforms}
          genreOptions={genres}
        />
      </div>
    </main>
  );
}
