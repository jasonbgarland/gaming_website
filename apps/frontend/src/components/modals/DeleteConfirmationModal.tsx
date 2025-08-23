import React from "react";

interface DeleteConfirmationModalProps {
  isOpen: boolean;
  collectionName: string;
  onConfirm: () => void;
  onCancel: () => void;
}

const DeleteConfirmationModal: React.FC<DeleteConfirmationModalProps> = ({
  isOpen,
  collectionName,
  onConfirm,
  onCancel,
}) => {
  if (!isOpen) return null;

  const handleOverlayClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) {
      onCancel();
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Escape") {
      onCancel();
    }
  };

  return (
    <div
      className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
      onClick={handleOverlayClick}
      onKeyDown={handleKeyDown}
      tabIndex={-1}
    >
      <div
        className="bg-gamer-surface rounded-lg border border-gamer-border p-6 max-w-md w-full shadow-2xl"
        role="dialog"
        aria-modal="true"
        aria-labelledby="delete-modal-title"
        aria-describedby="delete-modal-description"
      >
        <h2
          id="delete-modal-title"
          className="text-xl font-semibold text-gamer-danger mb-4"
        >
          Delete Collection
        </h2>

        <p
          id="delete-modal-description"
          className="text-gamer-text mb-6 leading-relaxed"
        >
          Are you sure you want to delete &ldquo;
          <strong className="text-gamer-text font-medium">
            {collectionName}
          </strong>
          &rdquo;? This action cannot be undone and will remove all games from
          this collection.
        </p>

        <div className="flex gap-3 justify-end">
          <button
            onClick={onCancel}
            className="bg-gamer-secondary hover:bg-gamer-secondary-hover text-gamer-text font-medium py-2 px-4 rounded-md transition-colors duration-200 border border-gamer-border"
          >
            Cancel
          </button>

          <button
            onClick={onConfirm}
            autoFocus
            className="bg-gamer-danger hover:bg-gamer-danger-hover text-white font-medium py-2 px-4 rounded-md transition-colors duration-200"
          >
            Delete Collection
          </button>
        </div>
      </div>
    </div>
  );
};

export default DeleteConfirmationModal;
