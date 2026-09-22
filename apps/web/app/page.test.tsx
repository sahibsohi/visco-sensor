import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import Home from "./page";

describe("Home", () => {
  it("describes the Day 1 platform foundation", () => {
    render(<Home />);

    expect(screen.getByRole("heading", { name: /turning sensor data/i })).toBeInTheDocument();
    expect(screen.getByText(/educational prototype/i)).toBeInTheDocument();
    expect(screen.getByText(/simulated device telemetry/i)).toBeInTheDocument();
  });
});
