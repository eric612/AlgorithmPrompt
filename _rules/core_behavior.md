## Core Behavior

- Prefer correctness, observability, and reproducibility.
- If stuck on the same bug across more than 3 tool-call cycles, ask the user.
- If an assumption affects algorithm quality, hardware cost, register
  timing, or verification result, ask the user.
- Do not silently change the algorithm intent just to make tests pass.
- Always separate best-quality reference, practical implementation,
  fixed-point model, and RTL-friendly C model.
