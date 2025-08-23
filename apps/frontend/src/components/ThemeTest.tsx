"use client";

import React, { useState } from "react";
import Navigation from "@/components/Navigation";
import { GameSearch } from "@/components/games/GameSearch";
import { GameImage } from "@/components/games/GameImage";
import GameEntryCard from "@/components/games/GameEntryCard";
import CollectionCard from "@/components/collections/CollectionCard";
import LoginForm from "@/components/auth/LoginForm";
import SignupForm from "@/components/auth/SignupForm";
import LogoutButton from "@/components/auth/LogoutButton";
import CreateCollectionModal from "@/components/modals/CreateCollectionModal";
import DeleteConfirmationModal from "@/components/modals/DeleteConfirmationModal";

// Mock data for demonstrations
const mockGame = {
  id: 1,
  name: "The Witcher 3: Wild Hunt",
  cover_url: "https://images.igdb.com/igdb/image/upload/t_cover_big/co2ott.jpg",
  summary: "An epic RPG adventure in a fantasy world.",
  rating: 95,
};

const mockGameOut = {
  id: 1,
  igdb_id: 1942,
  name: "The Witcher 3: Wild Hunt",
  platform: "PC",
  cover_url: "https://images.igdb.com/igdb/image/upload/t_cover_big/co2ott.jpg",
  genre: "RPG",
};

const mockCollectionEntry = {
  id: 1,
  collection_id: 1,
  game_id: 1,
  notes: "Amazing game!",
  status: "completed",
  rating: 9,
  added_at: new Date().toISOString(),
  game: mockGameOut,
};

const mockCollection = {
  id: 1,
  name: "Favorite RPGs",
  description: "My collection of the best role-playing games",
  user_id: 1,
  created_at: new Date().toISOString(),
  updated_at: new Date().toISOString(),
};

const mockCollectionWithCount = {
  ...mockCollection,
  gameCount: 5,
};

export default function ThemeTest() {
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [activeTab, setActiveTab] = useState<
    "colors" | "components" | "forms" | "modals"
  >("colors");

  return (
    <div className="min-h-screen bg-gamer-dark">
      {/* Navigation Demo */}
      <div className="mb-8">
        <Navigation
          user={{ username: "testuser", email: "test@example.com" }}
        />
      </div>

      <div className="p-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gamer-text mb-2">
            Gaming Website Component Showcase
          </h1>
          <p className="text-gamer-muted">
            Professional theme with all components - designed for employer
            review
          </p>
        </div>

        {/* Tab Navigation */}
        <div className="flex space-x-1 mb-8">
          {[
            { key: "colors" as const, label: "Color Palette" },
            { key: "components" as const, label: "Game Components" },
            { key: "forms" as const, label: "Auth Forms" },
            { key: "modals" as const, label: "Modals" },
          ].map((tab) => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              className={`px-4 py-2 rounded-md transition-colors duration-200 font-medium ${
                activeTab === tab.key
                  ? "bg-gamer-primary text-white"
                  : "bg-gamer-surface text-gamer-text hover:bg-gamer-elevated"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Color Palette Tab */}
        {activeTab === "colors" && (
          <div className="space-y-8">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {/* Primary Colors */}
              <div className="bg-gamer-surface border border-gamer-border rounded-lg p-6 shadow-gaming">
                <h2 className="text-xl font-semibold text-gamer-text mb-4">
                  Primary Actions
                </h2>
                <div className="space-y-3">
                  <button className="bg-gamer-primary hover:bg-gamer-primary-hover text-white px-4 py-2 rounded-md transition-colors duration-200 font-medium w-full">
                    Primary Button
                  </button>
                  <div className="bg-gamer-elevated text-gamer-text p-3 rounded text-sm">
                    Primary subtle background
                  </div>
                </div>
              </div>

              {/* Secondary Colors */}
              <div className="bg-gamer-elevated border border-gamer-border rounded-lg p-6 shadow-gaming">
                <h2 className="text-xl font-semibold text-gamer-text mb-4">
                  Secondary Actions
                </h2>
                <div className="space-y-3">
                  <button className="bg-gamer-secondary hover:bg-gamer-secondary-hover text-white px-4 py-2 rounded-md transition-colors duration-200 font-medium w-full">
                    Secondary Button
                  </button>
                  <div className="bg-gamer-subtle text-gamer-text p-3 rounded text-sm">
                    Secondary subtle background
                  </div>
                </div>
              </div>

              {/* Status Colors */}
              <div className="bg-gamer-subtle border border-gamer-border rounded-lg p-6 shadow-gaming">
                <h2 className="text-xl font-semibold text-gamer-text mb-4">
                  Status Colors
                </h2>
                <div className="space-y-2">
                  <div className="bg-gamer-success text-white px-3 py-2 rounded text-sm text-center">
                    Success State
                  </div>
                  <div className="bg-gamer-warning text-white px-3 py-2 rounded text-sm text-center">
                    Warning State
                  </div>
                  <div className="bg-gamer-danger text-white px-3 py-2 rounded text-sm text-center">
                    Danger State
                  </div>
                </div>
              </div>
            </div>

            {/* Typography Showcase */}
            <div className="bg-gamer-surface border border-gamer-border rounded-lg p-6 shadow-gaming">
              <h2 className="text-xl font-semibold text-gamer-text mb-4">
                Typography
              </h2>
              <div className="space-y-2">
                <p className="text-gamer-text text-lg">
                  Primary text (large) - #e2e8f0
                </p>
                <p className="text-gamer-text">
                  Primary text (normal) - High contrast
                </p>
                <p className="text-gamer-muted">
                  Muted text - Secondary information
                </p>
                <p className="text-gamer-subtle-text">
                  Subtle text - Tertiary information
                </p>
              </div>
            </div>

            {/* Input Components */}
            <div className="bg-gamer-surface border border-gamer-border rounded-lg p-6 shadow-2xl">
              <h2 className="text-xl font-semibold text-gamer-text mb-4">
                Input Components
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <input
                  type="text"
                  placeholder="Search games..."
                  className="bg-gamer-input border border-gamer-input-border rounded-md px-3 py-2 text-gamer-text placeholder-gamer-muted focus:ring-2 focus:ring-gamer-primary focus:border-transparent transition-all duration-200"
                />
                <select className="bg-gamer-input border border-gamer-input-border rounded-md px-3 py-2 text-gamer-text focus:ring-2 focus:ring-gamer-primary focus:border-transparent transition-all duration-200">
                  <option>Select a genre...</option>
                  <option>Action</option>
                  <option>RPG</option>
                  <option>Strategy</option>
                </select>
                <textarea
                  placeholder="Collection description..."
                  rows={3}
                  className="bg-gamer-input border border-gamer-input-border rounded-md px-3 py-2 text-gamer-text placeholder-gamer-muted focus:ring-2 focus:ring-gamer-primary focus:border-transparent transition-all duration-200 md:col-span-2 resize-none"
                />
              </div>
            </div>
          </div>
        )}

        {/* Game Components Tab */}
        {activeTab === "components" && (
          <div className="space-y-8">
            {/* Game Search */}
            <div className="bg-background-surface border border-border rounded-lg p-6 shadow-gaming">
              <h2 className="text-xl font-semibold text-foreground mb-4">
                Game Search Component
              </h2>
              <GameSearch className="w-full" />
            </div>

            {/* Game Image */}
            <div className="bg-background-surface border border-border rounded-lg p-6 shadow-gaming">
              <h2 className="text-xl font-semibold text-foreground mb-4">
                Game Image Component
              </h2>
              <div className="flex flex-wrap gap-4">
                <GameImage
                  fallbackUrl={mockGame.cover_url}
                  alt={mockGame.name}
                  className="w-48 h-72 rounded-lg"
                />
                <GameImage
                  fallbackUrl={mockGame.cover_url}
                  alt={mockGame.name}
                  className="w-36 h-54 rounded-lg"
                />
                <GameImage
                  fallbackUrl={mockGame.cover_url}
                  alt={mockGame.name}
                  className="w-24 h-36 rounded-lg"
                />
              </div>
            </div>

            {/* Game Entry Card */}
            <div className="bg-background-surface border border-border rounded-lg p-6 shadow-gaming">
              <h2 className="text-xl font-semibold text-foreground mb-4">
                Game Entry Card
              </h2>
              <div className="max-w-sm">
                <GameEntryCard
                  entry={mockCollectionEntry}
                  onRemove={() => console.log("Remove game")}
                />
              </div>
            </div>

            {/* Collection Card */}
            <div className="bg-background-surface border border-border rounded-lg p-6 shadow-gaming">
              <h2 className="text-xl font-semibold text-foreground mb-4">
                Collection Card
              </h2>
              <div className="max-w-sm">
                <CollectionCard
                  collection={mockCollectionWithCount}
                  onDelete={(id) => console.log("Delete collection", id)}
                  onViewCollection={(id) => console.log("View collection", id)}
                />
              </div>
            </div>
          </div>
        )}

        {/* Auth Forms Tab */}
        {activeTab === "forms" && (
          <div className="space-y-8">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Login Form */}
              <div className="bg-background-surface border border-border rounded-lg p-6 shadow-gaming">
                <h2 className="text-xl font-semibold text-foreground mb-4">
                  Login Form
                </h2>
                <LoginForm />
              </div>

              {/* Signup Form */}
              <div className="bg-background-surface border border-border rounded-lg p-6 shadow-gaming">
                <h2 className="text-xl font-semibold text-foreground mb-4">
                  Signup Form
                </h2>
                <SignupForm />
              </div>
            </div>

            {/* Logout Button */}
            <div className="bg-background-surface border border-border rounded-lg p-6 shadow-gaming">
              <h2 className="text-xl font-semibold text-foreground mb-4">
                Logout Button
              </h2>
              <LogoutButton />
            </div>
          </div>
        )}

        {/* Modals Tab */}
        {activeTab === "modals" && (
          <div className="space-y-8">
            {/* Modal Triggers */}
            <div className="bg-background-surface border border-border rounded-lg p-6 shadow-gaming">
              <h2 className="text-xl font-semibold text-foreground mb-4">
                Modal Components
              </h2>
              <div className="flex flex-wrap gap-4">
                <button
                  onClick={() => setShowCreateModal(true)}
                  className="bg-primary hover:bg-primary-hover text-primary-foreground px-4 py-2 rounded-md transition-colors duration-200 font-medium"
                >
                  Show Create Collection Modal
                </button>
                <button
                  onClick={() => setShowDeleteModal(true)}
                  className="bg-danger hover:bg-danger text-danger-foreground px-4 py-2 rounded-md transition-colors duration-200 font-medium"
                >
                  Show Delete Confirmation Modal
                </button>
              </div>
            </div>

            {/* Modal Demo Info */}
            <div className="bg-background-elevated border border-border rounded-lg p-6 shadow-gaming">
              <h3 className="text-lg font-semibold text-foreground mb-2">
                Modal Showcase
              </h3>
              <p className="text-foreground-muted">
                Click the buttons above to see our modal components in action.
                They demonstrate overlay styling, form inputs, and user
                interactions.
              </p>
            </div>
          </div>
        )}

        {/* Modals */}
        {showCreateModal && (
          <CreateCollectionModal
            open={showCreateModal}
            onClose={() => setShowCreateModal(false)}
            onCreate={(data: { name: string; description: string }) => {
              console.log("Create collection:", data);
              setShowCreateModal(false);
            }}
          />
        )}

        {showDeleteModal && (
          <DeleteConfirmationModal
            isOpen={showDeleteModal}
            collectionName="Test Collection"
            onConfirm={() => {
              console.log("Delete confirmed");
              setShowDeleteModal(false);
            }}
            onCancel={() => setShowDeleteModal(false)}
          />
        )}
      </div>
    </div>
  );
}
