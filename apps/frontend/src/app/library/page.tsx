"use client";

import React from "react";
import { useRouter } from "next/navigation";
import CollectionGrid from "../../components/collections/CollectionGrid";
import { useCollectionsWithCounts } from "@/hooks/useCollectionsWithCounts";
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
      <div className="p-8 bg-gamer-dark min-h-screen">
        <h1 className="text-3xl font-bold text-gamer-text mb-6">Collections</h1>
        <div className="text-gamer-danger bg-gamer-surface border border-gamer-danger p-4 rounded-lg">
          Error loading collections: {error.message}
        </div>
      </div>
    );
  }

  return (
    <div className="p-8 bg-gamer-dark min-h-screen">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gamer-text">Collections</h1>
        <button
          type="button"
          onClick={() => setShowCreateCollectionModal(true)}
          className="bg-gamer-primary hover:bg-gamer-primary-hover text-white px-6 py-3 rounded-lg font-medium transition-colors"
        >
          Create Collection
        </button>
      </div>

      {isLoading ? (
        <div className="text-center py-12">
          <div className="text-gamer-muted text-lg">Loading collections...</div>
        </div>
      ) : (
        <React.Fragment>
          <CollectionGrid
            collections={collections}
            onDelete={handleDelete}
            onViewCollection={handleViewCollection}
          />
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
