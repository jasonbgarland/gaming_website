"use client";

import React, { useState } from "react";
import { Collection } from "@/services/collectionsApi";

interface CollectionCardProps {
  collection: Collection & { gameCount?: number };
  onDelete: (collectionId: number) => void;
  onViewCollection: (collectionId: number) => void;
}

const CollectionCard: React.FC<CollectionCardProps> = ({
  collection,
  onDelete,
  onViewCollection,
}) => {
  const [isHovered, setIsHovered] = useState(false);

  const handleCardClick = () => {
    onViewCollection(collection.id);
  };

  const handleActionClick = (
    event: React.MouseEvent,
    action: (id: number) => void
  ) => {
    event.stopPropagation(); // Prevent card click
    action(collection.id);
  };

  const handleKeyDown = (event: React.KeyboardEvent) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault(); // Prevent page scroll on space
      handleCardClick();
    }
  };

  return (
    <div
      role="button"
      tabIndex={0}
      className="w-full p-4 border border-gamer-border rounded-lg bg-gamer-surface cursor-pointer text-left relative transition-all duration-200 hover:bg-gamer-elevated hover:scale-[1.02] hover:shadow-lg focus:bg-gamer-elevated focus:outline-none focus:ring-2 focus:ring-gamer-primary"
      onClick={handleCardClick}
      onKeyDown={handleKeyDown}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      aria-label={`View ${collection.name} collection`}
      onFocus={() => setIsHovered(true)}
      onBlur={() => setIsHovered(false)}
    >
      <div className="card-content">
        <h3 className="m-0 mb-2 text-xl font-semibold text-gamer-text">
          {collection.name}
        </h3>
        <p className="m-0 mb-3 text-gamer-muted text-sm leading-relaxed">
          {collection.description}
        </p>
        <span className="text-xs text-gamer-subtle-text font-medium">
          {collection.gameCount ?? 0} games
        </span>
      </div>

      <div
        className={`absolute top-4 right-4 flex gap-2 transition-all duration-200 ${
          isHovered ? "opacity-100 visible" : "opacity-0 invisible"
        }`}
      >
        <button
          onClick={(e) => handleActionClick(e, onDelete)}
          aria-label={`Delete ${collection.name} collection`}
          className="px-2 py-1 text-xs bg-gamer-surface border border-gamer-danger rounded text-gamer-danger cursor-pointer hover:bg-gamer-danger hover:text-white transition-colors"
        >
          Delete
        </button>
      </div>
    </div>
  );
};

export default CollectionCard;
