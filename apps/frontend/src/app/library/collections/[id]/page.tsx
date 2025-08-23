"use client";

import React from "react";
import { useParams } from "next/navigation";
import { useCollection } from "@/hooks/useCollection";
import CollectionDetail from "@/components/collections/CollectionDetail";

const CollectionDetailPage: React.FC = () => {
  const params = useParams();
  const collectionId = params.id ? Number(params.id) : null;

  // Use SWR hook for consistency
  const { collection, isLoading, error } = useCollection(collectionId);

  if (isLoading) {
    return (
      <div className="p-8 bg-gamer-dark min-h-screen">
        <div className="text-center py-12">
          <div className="text-gamer-muted text-lg">Loading collection...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-8 bg-gamer-dark min-h-screen">
        <h1 className="text-3xl font-bold text-gamer-text mb-6">
          Collection Not Found
        </h1>
        <div className="text-gamer-danger bg-gamer-surface border border-gamer-danger p-4 rounded-lg">
          Error: {error.message || "Failed to load collection"}
        </div>
      </div>
    );
  }

  if (!collection) {
    return (
      <div className="p-8 bg-gamer-dark min-h-screen">
        <h1 className="text-3xl font-bold text-gamer-text mb-6">
          Collection Not Found
        </h1>
        <div className="text-gamer-muted bg-gamer-surface border border-gamer-border p-4 rounded-lg">
          Collection not found
        </div>
      </div>
    );
  }

  return (
    <div className="bg-gamer-dark min-h-screen">
      <CollectionDetail collection={collection} />
    </div>
  );
};

export default CollectionDetailPage;
