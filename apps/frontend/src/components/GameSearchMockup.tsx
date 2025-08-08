"use client";

import React, { useState } from "react";

/**
 * UI Mockup for Enhanced Game Search with Filters
 * This shows the proposed design without full functionality
 */
const GameSearchMockup: React.FC = () => {
  const [query, setQuery] = useState("");
  const [showPlatformDropdown, setShowPlatformDropdown] = useState(false);
  const [showYearDropdown, setShowYearDropdown] = useState(false);
  const [selectedPlatforms, setSelectedPlatforms] = useState<string[]>([]);
  const [selectedYears, setSelectedYears] = useState<number[]>([]);

  // Mock data for dropdowns
  const platforms = [
    "PlayStation 5",
    "Xbox Series X/S",
    "Nintendo Switch",
    "PC (Windows)",
    "PlayStation 4",
    "Xbox One",
    "iOS",
    "Android",
  ];

  const years = [2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015];

  const mockResults = [
    {
      id: 1,
      name: "The Legend of Zelda: Tears of the Kingdom",
      platform: "Nintendo Switch",
      year: 2023,
      cover: "https://images.igdb.com/igdb/image/upload/t_cover_big/co5vmg.jpg",
    },
    {
      id: 2,
      name: "Spider-Man 2",
      platform: "PlayStation 5",
      year: 2023,
      cover: "https://images.igdb.com/igdb/image/upload/t_cover_big/co6qd4.jpg",
    },
    {
      id: 3,
      name: "Starfield",
      platform: "Xbox Series X/S",
      year: 2023,
      cover: "https://images.igdb.com/igdb/image/upload/t_cover_big/co6td8.jpg",
    },
  ];

  const removeFilter = (type: "platform" | "year", value: string | number) => {
    if (type === "platform") {
      setSelectedPlatforms((prev) => prev.filter((p) => p !== value));
    } else {
      setSelectedYears((prev) => prev.filter((y) => y !== value));
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-8">
        Enhanced Game Search - UI Mockup
      </h1>

      {/* Search Input */}
      <div className="mb-6">
        <div className="relative">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search for games..."
            className="w-full px-4 py-3 text-lg border-2 border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 transition-colors"
          />
          <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
            <svg
              className="w-5 h-5 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
          </div>
        </div>
      </div>

      {/* Filter Buttons */}
      <div className="mb-6">
        <div className="flex flex-wrap gap-3 mb-4">
          {/* Platform Filter */}
          <div className="relative">
            <button
              onClick={() => setShowPlatformDropdown(!showPlatformDropdown)}
              className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            >
              Platform
              <svg
                className={`w-4 h-4 transition-transform ${
                  showPlatformDropdown ? "rotate-180" : ""
                }`}
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M19 9l-7 7-7-7"
                />
              </svg>
            </button>

            {/* Platform Dropdown */}
            {showPlatformDropdown && (
              <div className="absolute top-full left-0 mt-1 w-64 bg-white border border-gray-200 rounded-lg shadow-lg z-10">
                <div className="max-h-64 overflow-y-auto">
                  {platforms.map((platform) => (
                    <button
                      key={platform}
                      onClick={() => {
                        if (!selectedPlatforms.includes(platform)) {
                          setSelectedPlatforms((prev) => [...prev, platform]);
                        }
                        setShowPlatformDropdown(false);
                      }}
                      className="w-full text-left px-4 py-2 hover:bg-gray-50 transition-colors"
                    >
                      {platform}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Year Filter */}
          <div className="relative">
            <button
              onClick={() => setShowYearDropdown(!showYearDropdown)}
              className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            >
              Year
              <svg
                className={`w-4 h-4 transition-transform ${
                  showYearDropdown ? "rotate-180" : ""
                }`}
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M19 9l-7 7-7-7"
                />
              </svg>
            </button>

            {/* Year Dropdown */}
            {showYearDropdown && (
              <div className="absolute top-full left-0 mt-1 w-32 bg-white border border-gray-200 rounded-lg shadow-lg z-10">
                <div className="max-h-64 overflow-y-auto">
                  {years.map((year) => (
                    <button
                      key={year}
                      onClick={() => {
                        if (!selectedYears.includes(year)) {
                          setSelectedYears((prev) => [...prev, year]);
                        }
                        setShowYearDropdown(false);
                      }}
                      className="w-full text-left px-4 py-2 hover:bg-gray-50 transition-colors"
                    >
                      {year}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Future Filters (Disabled) */}
          <button className="flex items-center gap-2 px-4 py-2 bg-gray-100 border border-gray-300 rounded-lg cursor-not-allowed opacity-50">
            Genre
            <svg
              className="w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 9l-7 7-7-7"
              />
            </svg>
          </button>

          <button className="flex items-center gap-2 px-4 py-2 bg-gray-100 border border-gray-300 rounded-lg cursor-not-allowed opacity-50">
            Rating
            <svg
              className="w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 9l-7 7-7-7"
              />
            </svg>
          </button>
        </div>

        {/* Active Filter Chips */}
        {(selectedPlatforms.length > 0 || selectedYears.length > 0) && (
          <div className="flex flex-wrap gap-2">
            {selectedPlatforms.map((platform) => (
              <div
                key={platform}
                className="flex items-center gap-2 px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm"
              >
                Platform: {platform}
                <button
                  onClick={() => removeFilter("platform", platform)}
                  className="w-4 h-4 flex items-center justify-center rounded-full hover:bg-blue-200 transition-colors"
                >
                  ×
                </button>
              </div>
            ))}
            {selectedYears.map((year) => (
              <div
                key={year}
                className="flex items-center gap-2 px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm"
              >
                Year: {year}
                <button
                  onClick={() => removeFilter("year", year)}
                  className="w-4 h-4 flex items-center justify-center rounded-full hover:bg-green-200 transition-colors"
                >
                  ×
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Results Count */}
      <div className="mb-4 text-gray-600">
        {query || selectedPlatforms.length > 0 || selectedYears.length > 0 ? (
          <>Showing 3 results {query && `for "${query}"`}</>
        ) : (
          "Enter search terms or select filters to find games"
        )}
      </div>

      {/* Mock Results */}
      {(query || selectedPlatforms.length > 0 || selectedYears.length > 0) && (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {mockResults.map((game) => (
            <div
              key={game.id}
              className="border border-gray-200 rounded-lg overflow-hidden hover:shadow-md transition-shadow"
            >
              <img
                src={game.cover}
                alt={game.name}
                className="w-full h-48 object-cover"
              />
              <div className="p-4">
                <h3 className="font-semibold text-lg mb-2">{game.name}</h3>
                <div className="flex items-center justify-between text-sm text-gray-600">
                  <span>{game.platform}</span>
                  <span>{game.year}</span>
                </div>
                <button className="w-full mt-3 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                  Add to Collection
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Design Notes */}
      <div className="mt-12 p-6 bg-gray-50 rounded-lg">
        <h3 className="font-semibold mb-4">🎨 Design Notes:</h3>
        <ul className="space-y-2 text-sm text-gray-700">
          <li>
            • <strong>Unified Search:</strong> Single search box searches all
            fields
          </li>
          <li>
            • <strong>Progressive Filters:</strong> Platform and Year dropdowns
            to refine results
          </li>
          <li>
            • <strong>Visual Feedback:</strong> Active filters shown as
            removable chips
          </li>
          <li>
            • <strong>Future Ready:</strong> Genre and Rating filters planned
            for later
          </li>
          <li>
            • <strong>Mobile Friendly:</strong> Responsive design with flexible
            layout
          </li>
          <li>
            • <strong>Accessibility:</strong> Keyboard navigation and screen
            reader support
          </li>
        </ul>
      </div>
    </div>
  );
};

export default GameSearchMockup;
