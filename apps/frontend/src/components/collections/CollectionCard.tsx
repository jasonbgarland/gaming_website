"use client";

import React, { useState } from "react";
import { Collection } from "../../services/collectionsApi";

interface CollectionCardProps {
  collection: Collection & { gameCount?: number };
  onEdit: (collectionId: number) => void;
  onDelete: (collectionId: number) => void;
  onViewCollection: (collectionId: number) => void;
}

const CollectionCard: React.FC<CollectionCardProps> = ({
  collection,
  onEdit,
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
      className="collection-card"
      onClick={handleCardClick}
      onKeyDown={handleKeyDown}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      aria-label={`View ${collection.name} collection`}
      style={{
        display: "block",
        width: "100%",
        padding: "1rem",
        border: "1px solid #e5e5e5",
        borderRadius: "8px",
        backgroundColor: "white",
        cursor: "pointer",
        textAlign: "left",
        position: "relative",
        transition: "box-shadow 0.2s ease",
        boxShadow: isHovered ? "0 4px 12px rgba(0,0,0,0.1)" : "none",
        outline: "none", // We'll handle focus styling manually
      }}
      onFocus={() => setIsHovered(true)}
      onBlur={() => setIsHovered(false)}
    >
      <div className="card-content">
        <h3
          style={{
            margin: "0 0 0.5rem 0",
            fontSize: "1.25rem",
            fontWeight: "600",
            color: "#1f2937",
          }}
        >
          {collection.name}
        </h3>
        <p
          style={{
            margin: "0 0 0.75rem 0",
            color: "#6b7280",
            fontSize: "0.875rem",
            lineHeight: "1.4",
          }}
        >
          {collection.description}
        </p>
        <span
          style={{
            fontSize: "0.75rem",
            color: "#9ca3af",
            fontWeight: "500",
          }}
        >
          {collection.gameCount ?? 0} games
        </span>
      </div>

      <div
        className="card-actions"
        style={{
          position: "absolute",
          top: "1rem",
          right: "1rem",
          display: "flex",
          gap: "0.5rem",
          opacity: isHovered ? 1 : 0,
          visibility: isHovered ? "visible" : "hidden",
          transition: "opacity 0.2s ease, visibility 0.2s ease",
        }}
      >
        <button
          onClick={(e) => handleActionClick(e, onEdit)}
          aria-label={`Edit ${collection.name} collection`}
          style={{
            padding: "0.25rem 0.5rem",
            fontSize: "0.75rem",
            backgroundColor: "#f3f4f6",
            border: "1px solid #d1d5db",
            borderRadius: "4px",
            cursor: "pointer",
            color: "#374151",
          }}
        >
          Edit
        </button>
        <button
          onClick={(e) => handleActionClick(e, onDelete)}
          aria-label={`Delete ${collection.name} collection`}
          style={{
            padding: "0.25rem 0.5rem",
            fontSize: "0.75rem",
            backgroundColor: "#fef2f2",
            border: "1px solid #fecaca",
            borderRadius: "4px",
            cursor: "pointer",
            color: "#dc2626",
          }}
        >
          Delete
        </button>
      </div>
    </div>
  );
};

export default CollectionCard;
