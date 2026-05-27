"use client";

import React, { useState, useRef, useEffect } from "react";

export interface YearRangeValue {
  yearStart?: number;
  yearEnd?: number;
}

export interface YearRangeDropdownProps {
  yearStart?: number;
  yearEnd?: number;
  onChange: (range: YearRangeValue) => void;
  className?: string;
}

/**
 * A dropdown filter for selecting a year range (From / To).
 * The trigger button shows the active range in its label when set.
 * Clicking outside closes the panel.
 */
export function YearRangeDropdown({
  yearStart,
  yearEnd,
  onChange,
  className = "",
}: YearRangeDropdownProps) {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Close when clicking outside
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

  // Build the button label
  function buildLabel() {
    if (yearStart !== undefined && yearEnd !== undefined) {
      return `Year: ${yearStart}–${yearEnd}`;
    }
    if (yearStart !== undefined) {
      return `Year: ${yearStart}–`;
    }
    if (yearEnd !== undefined) {
      return `Year: –${yearEnd}`;
    }
    return "Year";
  }

  function handleFromChange(e: React.ChangeEvent<HTMLInputElement>) {
    const raw = e.target.value;
    onChange({
      yearStart: raw === "" ? undefined : Number(raw),
      yearEnd,
    });
  }

  function handleToChange(e: React.ChangeEvent<HTMLInputElement>) {
    const raw = e.target.value;
    onChange({
      yearStart,
      yearEnd: raw === "" ? undefined : Number(raw),
    });
  }

  const label = buildLabel();
  const isActive = yearStart !== undefined || yearEnd !== undefined;

  return (
    <div ref={dropdownRef} className={`relative ${className}`}>
      {/* Trigger button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-4 py-2 bg-gamer-surface border border-gamer-border rounded-lg hover:bg-gamer-elevated transition-colors text-gamer-text"
        aria-expanded={isOpen}
        aria-haspopup="dialog"
      >
        {label}
        {isActive && (
          <span className="bg-gamer-primary text-white text-xs px-2 py-0.5 rounded-full">
            1
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

      {/* Panel */}
      {isOpen && (
        <div
          className="absolute top-full left-0 mt-1 w-56 bg-gamer-elevated border border-gamer-border rounded-lg shadow-lg z-10 p-4"
          role="dialog"
          aria-label="Year range filter"
        >
          <div className="flex flex-col gap-3">
            <div className="flex flex-col gap-1">
              <label
                htmlFor="year-from"
                className="text-xs font-medium text-gamer-muted uppercase tracking-wide"
              >
                From
              </label>
              <input
                id="year-from"
                type="number"
                value={yearStart ?? ""}
                onChange={handleFromChange}
                placeholder="e.g. 2010"
                className="w-full px-3 py-1.5 border border-gamer-border rounded bg-gamer-input text-gamer-text focus:outline-none focus:ring-2 focus:ring-gamer-primary text-sm"
              />
            </div>
            <div className="flex flex-col gap-1">
              <label
                htmlFor="year-to"
                className="text-xs font-medium text-gamer-muted uppercase tracking-wide"
              >
                To
              </label>
              <input
                id="year-to"
                type="number"
                value={yearEnd ?? ""}
                onChange={handleToChange}
                placeholder="e.g. 2024"
                className="w-full px-3 py-1.5 border border-gamer-border rounded bg-gamer-input text-gamer-text focus:outline-none focus:ring-2 focus:ring-gamer-primary text-sm"
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
