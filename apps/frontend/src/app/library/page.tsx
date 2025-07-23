"use client";

import React from "react";
import { useRouter } from "next/navigation";
import LibraryTable from "./components/LibraryTable";
import { useCollections } from "../../hooks/useCollections";
import { CreateCollectionModal } from "./components/CreateCollectionModal";

const LibraryPage: React.FC = () => {
  const router = useRouter();
  const { collections, isLoading, error, deleteCollection } = useCollections();
  const [showCreateCollectionModal, setShowCreateCollectionModal] =
    React.useState(false);

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

  const handleCreateCollection = (formData: any) => {
    // TODO: Call useCollections().createCollection(formData)
    console.log("Create collection:", formData);
    setShowCreateCollectionModal(false);
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
          <LibraryTable
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
