"use client";

import React from "react";

interface CreateCollectionModalProps {
  open: boolean;
  onClose: () => void;
  onCreate: (data: { name: string; description: string }) => void;
}

const CreateCollectionModal = ({
  open,
  onClose,
  onCreate,
}: CreateCollectionModalProps) => {
  const [name, setName] = React.useState("");
  const [description, setDescription] = React.useState("");
  const [isSubmitting, setIsSubmitting] = React.useState(false);
  const [errors, setErrors] = React.useState<{
    name?: string;
    description?: string;
    form?: string;
  }>({});

  // Ref for auto-focusing the name input
  const nameInputRef = React.useRef<HTMLInputElement>(null);

  // Auto-focus the name input when modal opens
  React.useEffect(() => {
    if (open && nameInputRef.current) {
      nameInputRef.current.focus();
    }
  }, [open]);

  // Handle keyboard events
  React.useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        onClose();
      }
    };

    if (open) {
      document.addEventListener("keydown", handleKeyDown);
      return () => document.removeEventListener("keydown", handleKeyDown);
    }
  }, [open, onClose]);

  if (!open) return null;

  const validateForm = () => {
    const errors: { name?: string; description?: string; form?: string } = {};
    if (!name.trim()) {
      errors.name = "Name is required";
    } else if (name.length < 2) {
      errors.name = "Name must be at least 2 characters";
    } else if (name.length > 50) {
      errors.name = "Name must be 50 characters or less";
    } else if (!/^[A-Za-z0-9 ]+$/.test(name)) {
      errors.name = "Name can only contain letters, numbers, and spaces";
    }
    if (description.length > 200) {
      errors.description = "Description must be 200 characters or less";
    }
    return errors;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const validationErrors = validateForm();
    setErrors(validationErrors);
    if (Object.keys(validationErrors).length === 0) {
      setIsSubmitting(true);
      try {
        await onCreate?.({ name, description });
        // Reset form and close modal only on success
        setName("");
        setDescription("");
        setErrors({});
        onClose();
      } catch (error) {
        console.error("Error creating collection:", error);
        const errorMessage =
          error instanceof Error
            ? error.message
            : "Failed to create collection. Please try again.";
        setErrors({ form: errorMessage });
      } finally {
        setIsSubmitting(false);
      }
    }
  };

  // Handle Enter key press in name field to submit form
  const handleNameKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      e.preventDefault();
      // Cast to FormEvent for handleSubmit compatibility
      handleSubmit(e as React.FormEvent);
    }
  };

  // Handle click outside to close modal
  const handleOverlayClick = (e: React.MouseEvent) => {
    // Only close if clicking on the overlay itself, not on the modal content
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <div
      role="dialog"
      aria-modal="true"
      onClick={handleOverlayClick}
      className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
    >
      <div className="bg-gamer-surface rounded-lg border border-gamer-border p-6 w-full max-w-md shadow-2xl">
        <h2 className="text-xl font-semibold text-gamer-text mb-6">
          Create New Collection
        </h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label
              htmlFor="collection-name"
              className="block text-gamer-text font-medium mb-2"
            >
              Collection Name
            </label>
            <input
              ref={nameInputRef}
              id="collection-name"
              aria-label="collection name"
              required
              maxLength={50}
              value={name}
              onChange={(e) => setName(e.target.value)}
              onKeyDown={handleNameKeyDown}
              className="w-full px-3 py-2 bg-gamer-input border border-gamer-input-border rounded-md text-gamer-text placeholder-gamer-muted focus:outline-none focus:ring-2 focus:ring-gamer-primary focus:border-transparent"
              placeholder="Enter collection name"
            />
            {errors.name && (
              <div
                className="bg-gamer-danger/10 border border-gamer-danger/20 text-gamer-danger px-3 py-2 rounded-md text-sm mt-2"
                role="alert"
              >
                {errors.name}
              </div>
            )}
          </div>

          <div>
            <label
              htmlFor="collection-description"
              className="block text-gamer-text font-medium mb-2"
            >
              Description
            </label>
            <textarea
              id="collection-description"
              aria-label="description"
              maxLength={200}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={3}
              className="w-full px-3 py-2 bg-gamer-input border border-gamer-input-border rounded-md text-gamer-text placeholder-gamer-muted focus:outline-none focus:ring-2 focus:ring-gamer-primary focus:border-transparent resize-none"
              placeholder="Optional description for your collection"
            />
            {errors.description && (
              <div
                className="bg-gamer-danger/10 border border-gamer-danger/20 text-gamer-danger px-3 py-2 rounded-md text-sm mt-2"
                role="alert"
              >
                {errors.description}
              </div>
            )}
          </div>

          {errors.form && (
            <div
              className="bg-gamer-danger/10 border border-gamer-danger/20 text-gamer-danger px-3 py-2 rounded-md text-sm"
              role="alert"
            >
              {errors.form}
            </div>
          )}

          <div className="flex gap-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 bg-gamer-secondary hover:bg-gamer-secondary-hover text-gamer-text font-medium py-2 px-4 rounded-md transition-colors duration-200 border border-gamer-border"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="flex-1 bg-gamer-primary hover:bg-gamer-primary-hover text-white font-medium py-2 px-4 rounded-md transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isSubmitting ? "Saving..." : "Save"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CreateCollectionModal;
