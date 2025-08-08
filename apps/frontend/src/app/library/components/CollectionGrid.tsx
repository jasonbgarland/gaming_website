"use client";

import React from "react";
import { CollectionWithCount } from "../../../hooks/useCollectionsWithCounts";
import CollectionCard from "../../../components/collections/CollectionCard";

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
      className="collection-grid"
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
        <div aria-live="polite">No collections yet!</div>
      )}
    </div>
  );
};

export default CollectionGrid;
