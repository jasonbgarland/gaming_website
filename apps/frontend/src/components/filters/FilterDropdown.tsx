"use client";

import React, { useState, useRef, useEffect } from "react";

export interface FilterOption {
  id: number;
  label: string;
}

export interface FilterDropdownProps {
  label: string;
  options: FilterOption[];
  selected: number[];
  onChange: (selected: number[]) => void;
  className?: string;
}

/**
 * A reusable dropdown filter component with multi-select support.
 * Shows a button with the filter label and an optional badge showing
 * how many items are selected. Clicking the button toggles a dropdown
 * with selectable options. Includes search functionality for easier navigation
 * when there are many options.
 */
export function FilterDropdown({
  label,
  options,
  selected,
  onChange,
  className = "",
}: FilterDropdownProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const dropdownRef = useRef<HTMLDivElement>(null);
  const searchInputRef = useRef<HTMLInputElement>(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node)
      ) {
        setIsOpen(false);
      }
    }

    if (isOpen) {
      document.addEventListener("mousedown", handleClickOutside);
      return () => document.removeEventListener("mousedown", handleClickOutside);
    }
  }, [isOpen]);

  // Focus search input when dropdown opens
  useEffect(() => {
    if (isOpen && searchInputRef.current) {
      searchInputRef.current.focus();
    }
  }, [isOpen]);

  // Clear search when dropdown closes
  useEffect(() => {
    if (!isOpen) {
      setSearchQuery("");
    }
  }, [isOpen]);

  function handleToggleOption(optionId: number) {
    if (selected.includes(optionId)) {
      // Deselect — remove from list
      onChange(selected.filter((id) => id !== optionId));
    } else {
      // Select — add to list
      onChange([...selected, optionId]);
    }
  }

  // Filter options based on search query
  const filteredOptions = searchQuery.trim()
    ? options.filter((option) =>
        option.label.toLowerCase().includes(searchQuery.toLowerCase())
      )
    : options;

  return (
    <div ref={dropdownRef} className={`relative ${className}`}>
      {/* Filter button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-4 py-2 bg-gamer-surface border border-gamer-border rounded-lg hover:bg-gamer-elevated transition-colors text-gamer-text"
        aria-expanded={isOpen}
        aria-haspopup="listbox"
      >
        {label}
        {selected.length > 0 && (
          <span className="bg-gamer-primary text-white text-xs px-2 py-0.5 rounded-full">
            {selected.length}
          </span>
        )}
        <svg
          className={`w-4 h-4 transition-transform ${isOpen ? "rotate-180" : ""}`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M19 9l-7 7-7-7"
          />
        </svg>
      </button>

      {/* Dropdown list */}
      {isOpen && (
        <div
          className="absolute top-full left-0 mt-1 w-64 bg-gamer-elevated border border-gamer-border rounded-lg shadow-lg z-10"
          role="listbox"
          aria-label={`${label} options`}
        >
          {/* Search input */}
          {options.length > 5 && (
            <div className="p-2 border-b border-gamer-border">
              <input
                ref={searchInputRef}
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search..."
                className="w-full px-3 py-1.5 bg-gamer-surface border border-gamer-border rounded text-gamer-text placeholder-gamer-muted focus:outline-none focus:ring-2 focus:ring-gamer-primary"
                onClick={(e) => e.stopPropagation()}
              />
            </div>
          )}

          <div className="max-h-64 overflow-y-auto">
            {filteredOptions.length === 0 ? (
              <div className="px-4 py-3 text-gamer-muted text-sm">
                {searchQuery.trim() ? "No matches found" : "No options available"}
              </div>
            ) : (
              filteredOptions.map((option) => (
                <button
                  key={option.id}
                  onClick={() => handleToggleOption(option.id)}
                  className="w-full text-left px-4 py-2 hover:bg-gamer-subtle transition-colors text-gamer-text flex items-center justify-between"
                  role="option"
                  aria-selected={selected.includes(option.id)}
                >
                  <span>{option.label}</span>
                  {selected.includes(option.id) && (
                    <svg
                      className="w-4 h-4 text-gamer-primary"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path
                        fillRule="evenodd"
                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                        clipRule="evenodd"
                      />
                    </svg>
                  )}
                </button>
              ))
            )}
          </div>
        </div>
      )}
    </div>
  );
}