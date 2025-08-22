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
      style={
        {
          /* overlay styles */
        }
      }
    >
      <form onSubmit={handleSubmit}>
        <label htmlFor="collection-name">Collection Name</label>
        <input
          ref={nameInputRef}
          id="collection-name"
          aria-label="collection name"
          required
          maxLength={50}
          value={name}
          onChange={(e) => setName(e.target.value)}
          onKeyDown={handleNameKeyDown}
        />
        {errors.name && (
          <div style={{ color: "red" }} role="alert">
            {errors.name}
          </div>
        )}
        <label htmlFor="collection-description">Description</label>
        <input
          id="collection-description"
          aria-label="description"
          maxLength={200}
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        {errors.description && (
          <div style={{ color: "red" }} role="alert">
            {errors.description}
          </div>
        )}
        {errors.form && (
          <div style={{ color: "red" }} role="alert">
            {errors.form}
          </div>
        )}

        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? "Saving..." : "Save"}
        </button>
        <button type="button" onClick={onClose}>
          Cancel
        </button>
      </form>
    </div>
  );
};

export default CreateCollectionModal;
