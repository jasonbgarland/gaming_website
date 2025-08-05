"use client";

import React from "react";
import { useParams } from "next/navigation";
import { useCollection } from "hooks/useCollection";
import CollectionDetail from "components/collections/CollectionDetail";

const CollectionDetailPage: React.FC = () => {
  const params = useParams();
  const collectionId = params.id ? Number(params.id) : null;

  // Use SWR hook for consistency
  const { collection, isLoading, error } = useCollection(collectionId);

  if (isLoading) {
    return (
      <div style={{ padding: "2rem" }}>
        <div>Loading collection...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ padding: "2rem" }}>
        <h1>Collection Not Found</h1>
        <div>Error: {error.message || "Failed to load collection"}</div>
      </div>
    );
  }

  if (!collection) {
    return (
      <div style={{ padding: "2rem" }}>
        <h1>Collection Not Found</h1>
        <div>Collection not found</div>
      </div>
    );
  }

  return <CollectionDetail collection={collection} />;
};

export default CollectionDetailPage;
