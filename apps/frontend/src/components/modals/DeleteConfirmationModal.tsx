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
      className="modal-overlay"
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: "rgba(0, 0, 0, 0.5)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 1000,
      }}
      onClick={handleOverlayClick}
      onKeyDown={handleKeyDown}
      tabIndex={-1}
    >
      <div
        className="modal-content"
        style={{
          backgroundColor: "white",
          borderRadius: "8px",
          padding: "2rem",
          maxWidth: "400px",
          width: "90%",
          boxShadow: "0 10px 25px rgba(0, 0, 0, 0.15)",
          outline: "none",
        }}
        role="dialog"
        aria-modal="true"
        aria-labelledby="delete-modal-title"
        aria-describedby="delete-modal-description"
      >
        <h2
          id="delete-modal-title"
          style={{
            margin: "0 0 1rem 0",
            fontSize: "1.25rem",
            fontWeight: "600",
            color: "#dc2626",
          }}
        >
          Delete Collection
        </h2>

        <p
          id="delete-modal-description"
          style={{
            margin: "0 0 2rem 0",
            color: "#4b5563",
            lineHeight: "1.5",
          }}
        >
          Are you sure you want to delete &ldquo;
          <strong>{collectionName}</strong>&rdquo;? This action cannot be undone
          and will remove all games from this collection.
        </p>

        <div
          className="modal-actions"
          style={{
            display: "flex",
            gap: "0.75rem",
            justifyContent: "flex-end",
          }}
        >
          <button
            onClick={onCancel}
            style={{
              padding: "0.5rem 1rem",
              border: "1px solid #d1d5db",
              borderRadius: "6px",
              backgroundColor: "white",
              color: "#374151",
              cursor: "pointer",
              fontSize: "0.875rem",
              fontWeight: "500",
            }}
            onMouseOver={(e) => {
              e.currentTarget.style.backgroundColor = "#f9fafb";
            }}
            onMouseOut={(e) => {
              e.currentTarget.style.backgroundColor = "white";
            }}
          >
            Cancel
          </button>

          <button
            onClick={onConfirm}
            style={{
              padding: "0.5rem 1rem",
              border: "1px solid #dc2626",
              borderRadius: "6px",
              backgroundColor: "#dc2626",
              color: "white",
              cursor: "pointer",
              fontSize: "0.875rem",
              fontWeight: "500",
            }}
            onMouseOver={(e) => {
              e.currentTarget.style.backgroundColor = "#b91c1c";
            }}
            onMouseOut={(e) => {
              e.currentTarget.style.backgroundColor = "#dc2626";
            }}
            autoFocus
          >
            Delete Collection
          </button>
        </div>
      </div>
    </div>
  );
};

export default DeleteConfirmationModal;
