"use client";

import React from "react";
import { useRouter } from "next/navigation";
import CollectionGrid from "../../components/collections/CollectionGrid";
import { useCollectionsWithCounts } from "hooks/useCollectionsWithCounts";
import CreateCollectionModal from "../../components/modals/CreateCollectionModal";
import DeleteConfirmationModal from "../../components/modals/DeleteConfirmationModal";

const LibraryPage: React.FC = () => {
  const router = useRouter();
  const { collections, isLoading, error, deleteCollection, createCollection } =
    useCollectionsWithCounts();
  const [showCreateCollectionModal, setShowCreateCollectionModal] =
    React.useState(false);

  // State for delete confirmation modal
  const [showDeleteModal, setShowDeleteModal] = React.useState(false);
  const [collectionToDelete, setCollectionToDelete] = React.useState<{
    id: number;
    name: string;
  } | null>(null);

  const handleDelete = (collectionId: number) => {
    // Find the collection to get its name for the confirmation modal
    const collection = collections.find((c) => c.id === collectionId);
    if (collection) {
      setCollectionToDelete({ id: collection.id, name: collection.name });
      setShowDeleteModal(true);
    }
  };

  const handleConfirmDelete = async () => {
    if (!collectionToDelete) return;

    try {
      await deleteCollection(collectionToDelete.id);
      setShowDeleteModal(false);
      setCollectionToDelete(null);
    } catch (error) {
      console.error("Failed to delete collection:", error);
      // TODO: Show error toast/notification
      // Keep modal open so user can try again
    }
  };

  const handleCancelDelete = () => {
    setShowDeleteModal(false);
    setCollectionToDelete(null);
  };

  const handleViewCollection = (collectionId: number) => {
    console.log("View collection:", collectionId);
    router.push(`/library/collections/${collectionId}`);
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

          <DeleteConfirmationModal
            isOpen={showDeleteModal}
            collectionName={collectionToDelete?.name || ""}
            onConfirm={handleConfirmDelete}
            onCancel={handleCancelDelete}
          />
        </React.Fragment>
      )}
    </div>
  );
};

export default LibraryPage;
