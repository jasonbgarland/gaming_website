"use client";

import React from "react";
import { Collection } from "../../../services/collectionsApi";

interface LibraryTableProps {
  collections: Collection[];
  onEdit: (collectionId: number) => void;
  onDelete: (collectionId: number) => void;
  onViewCollection: (collectionId: number) => void;
}

const LibraryTable: React.FC<LibraryTableProps> = ({
  collections,
  onEdit,
  onDelete,
  onViewCollection,
}) => {
  return (
    <table
      style={{
        width: "100%",
        borderCollapse: "collapse",
        marginTop: "1rem",
      }}
    >
      <thead>
        <tr>
          <th
            style={{
              textAlign: "left",
              padding: "0.5rem",
              borderBottom: "2px solid #eee",
            }}
          >
            Collection
          </th>
          <th
            style={{
              textAlign: "right",
              padding: "0.5rem",
              borderBottom: "2px solid #eee",
            }}
          >
            Actions
          </th>
        </tr>
      </thead>
      <tbody>
        {collections.map((collection) => (
          <tr key={collection.id} style={{ borderBottom: "1px solid #eee" }}>
            <td style={{ padding: "0.75rem 0.5rem" }}>
              <button
                onClick={() => onViewCollection(collection.id)}
                style={{
                  background: "none",
                  border: "none",
                  cursor: "pointer",
                  padding: 0,
                  color: "inherit",
                  textDecoration: "underline",
                  fontSize: "inherit",
                }}
              >
                {collection.name}
              </button>
            </td>
            <td style={{ textAlign: "right", padding: "0.75rem 0.5rem" }}>
              <button
                onClick={() => onEdit(collection.id)}
                style={{
                  background: "none",
                  border: "none",
                  cursor: "pointer",
                  marginRight: "0.5rem",
                  padding: 0,
                }}
                aria-label={`Edit ${collection.name}`}
              >
                {/* Pencil SVG */}
                <svg
                  width="20"
                  height="20"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  viewBox="0 0 24 24"
                >
                  <path d="M15.232 5.232l3.536 3.536M9 13l6.232-6.232a2 2 0 112.828 2.828L11.828 15.828a2 2 0 01-2.828 0L9 13z" />
                  <path d="M3 21h18" />
                </svg>
              </button>
              <button
                onClick={() => onDelete(collection.id)}
                style={{
                  background: "none",
                  border: "none",
                  cursor: "pointer",
                  padding: 0,
                }}
                aria-label={`Delete ${collection.name}`}
              >
                {/* Trashcan SVG */}
                <svg
                  width="20"
                  height="20"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  viewBox="0 0 24 24"
                >
                  <path d="M3 6h18" />
                  <path d="M8 6V4a2 2 0 012-2h4a2 2 0 012 2v2" />
                  <path d="M19 6l-1 14a2 2 0 01-2 2H8a2 2 0 01-2-2L5 6" />
                  <path d="M10 11v6" />
                  <path d="M14 11v6" />
                </svg>
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default LibraryTable;
