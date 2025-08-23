export default function Home() {
  return (
    <div className="min-h-screen bg-gamer-dark flex items-center justify-center p-8">
      <div className="text-center max-w-4xl mx-auto">
        {/* Main Title */}
        <h1 className="text-6xl md:text-8xl font-bold text-gamer-text mb-8">
          GameHub
        </h1>

        {/* Description */}
        <div className="space-y-6">
          <p className="text-xl md:text-2xl text-gamer-muted mb-8">
            This is a work in progress site.
          </p>

          <p className="text-lg md:text-xl text-gamer-text max-w-2xl mx-auto leading-relaxed">
            Current functionality exists to manage collections of games using
            the IGDB database.
          </p>
        </div>

        {/* Optional: Navigation hint */}
        <div className="mt-12">
          <p className="text-gamer-muted mb-4">Get started by exploring:</p>
          <div className="flex gap-4 justify-center flex-wrap">
            <a
              href="/library"
              className="bg-gamer-primary hover:bg-gamer-primary-hover text-white px-6 py-3 rounded-lg font-medium transition-colors"
            >
              View Collections
            </a>
            <a
              href="/games/search"
              className="bg-gamer-secondary hover:bg-gamer-secondary-hover text-white px-6 py-3 rounded-lg font-medium transition-colors"
            >
              Search Games
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
