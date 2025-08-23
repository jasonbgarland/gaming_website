"use client";

import React from "react";
import { CollectionWithCount } from "@/hooks/useCollectionsWithCounts";
import CollectionCard from "./CollectionCard";

interface CollectionGridProps {
  collections: CollectionWithCount[];
  onDelete: (collectionId: number) => void;
  onViewCollection: (collectionId: number) => void;
}

const CollectionGrid: React.FC<CollectionGridProps> = ({
  collections,
  onDelete,
  onViewCollection,
}) => {
  return (
    <div
      className={collections.length > 0 ? "collection-grid" : "w-full"}
      role="region"
      aria-label="Collections grid"
    >
      {collections.length > 0 ? (
        collections.map((collection) => (
          <CollectionCard
            key={collection.id}
            collection={collection}
            onDelete={onDelete}
            onViewCollection={onViewCollection}
          />
        ))
      ) : (
        <div
          className="text-center py-16 text-gamer-muted w-full flex flex-col items-center justify-center"
        >
          <div className="mb-4">
            <svg
              className="mx-auto h-12 w-12 text-gamer-subtle-text"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
              />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-gamer-text mb-2" aria-live="polite">
            No collections yet!
          </h3>
          <p className="text-gamer-muted">
            Create your first collection to organize your games.
          </p>
        </div>
      )}
    </div>
  );
};

export default CollectionGrid;
