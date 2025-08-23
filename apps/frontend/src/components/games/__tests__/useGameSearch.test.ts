import { useGameSearch } from "../../../hooks/useGameSearch";

describe("useGameSearch", () => {
  it("should export useGameSearch function", () => {
    expect(typeof useGameSearch).toBe("function");
  });
});
