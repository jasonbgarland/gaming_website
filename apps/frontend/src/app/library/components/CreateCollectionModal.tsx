"use client";

import React from "react";

interface CreateCollectionModalProps {
  open: boolean;
  onClose: () => void;
  onCreate: (e: React.FormEvent) => void;
}

export function CreateCollectionModal({
  open,
  onClose,
  onCreate,
}: CreateCollectionModalProps) {
  if (!open) return null;
  return (
    <div
      role="dialog"
      aria-modal="true"
      style={
        {
          /* overlay styles */
        }
      }
    >
      <form onSubmit={onCreate}>
        <label htmlFor="collection-name">Collection Name</label>
        <input id="collection-name" aria-label="collection name" required />
        <label htmlFor="collection-description">Description</label>
        <input id="collection-description" aria-label="description" />
        <button type="submit">Save</button>
        <button type="button" onClick={onClose}>
          Cancel
        </button>
      </form>
    </div>
  );
}
