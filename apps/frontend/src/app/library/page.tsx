"use client";

import React from "react";
import { useRouter } from "next/navigation";
import CollectionGrid from "./components/CollectionGrid";
import { useCollections } from "../../hooks/useCollections";
import CreateCollectionModal from "./components/CreateCollectionModal";

const LibraryPage: React.FC = () => {
  const router = useRouter();
  const { collections, isLoading, error, deleteCollection } = useCollections();
  const [showCreateCollectionModal, setShowCreateCollectionModal] =
    React.useState(false);
  const { createCollection } = useCollections();

  const handleEdit = (collectionId: number) => {
    console.log("Edit collection:", collectionId);
    // TODO: Navigate to edit page or open edit modal
  };

  const handleDelete = async (collectionId: number) => {
    console.log("Delete collection:", collectionId);
    try {
      await deleteCollection(collectionId);
    } catch (error) {
      console.error("Failed to delete collection:", error);
      // TODO: Show error toast/notification
    }
  };

  const handleViewCollection = (collectionId: number) => {
    console.log("View collection:", collectionId);
    router.push(`/library/${collectionId}`);
  };

  const handleCreateCollection = async ({
    name,
    description,
  }: {
    name: string;
    description: string;
  }) => {
    try {
      await createCollection({
        name,
        description,
      });
      setShowCreateCollectionModal(false);
    } catch (error) {
      console.error("Failed to create collection:", error);
      // Optionally show error feedback here
    }
  };

  if (error) {
    return (
      <div style={{ padding: "2rem" }}>
        <h1>My Library</h1>
        <div>Error loading collections: {error.message}</div>
      </div>
    );
  }

  return (
    <div style={{ padding: "2rem" }}>
      <h1>My Library</h1>
      {isLoading ? (
        <div>Loading...</div>
      ) : (
        <React.Fragment>
          <CollectionGrid
            collections={collections}
            onEdit={handleEdit}
            onDelete={handleDelete}
            onViewCollection={handleViewCollection}
          />
          <button
            type="button"
            onClick={() => setShowCreateCollectionModal(true)}
            style={{ marginTop: "1rem" }}
          >
            Create Collection
          </button>
          {showCreateCollectionModal && (
            <CreateCollectionModal
              open={showCreateCollectionModal}
              onClose={() => setShowCreateCollectionModal(false)}
              onCreate={handleCreateCollection}
            />
          )}
        </React.Fragment>
      )}
    </div>
  );
};

export default LibraryPage;
