#!/bin/bash
# Script: run_tests.sh
# Purpose: Run frontend Jest tests with minimal output
# Output: Summary only — test counts. Only shows failure details if any fail.

cd "$(dirname "$0")"

# Run jest, capture full output to temp file, show summary only
TMPFILE=$(mktemp)
npx jest --no-cache ${1:-} &> "$TMPFILE"

# Always show summary line (Tests: X passed, Y failed, etc.)
grep -E "^Tests:" "$TMPFILE"

# Show suite summary if there are failures
FAIL_COUNT=$(grep "^Test Suites:" "$TMPFILE" | grep -o '[0-9]* failed' | head -1 | grep -o '[0-9]*')
FAIL_COUNT=${FAIL_COUNT:-0}
if [ "$FAIL_COUNT" -gt 0 ]; then
  echo ""
  echo "=== FAILURES ==="
  # Show failing test names and error details
  grep -E "(FAIL |● )" "$TMPFILE"
  # Show relevant error context (first 5 lines after each ● )
  grep -A5 "● " "$TMPFILE" | head -80
fi

rm "$TMPFILE"