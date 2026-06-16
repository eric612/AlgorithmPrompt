
## Shadow / Update Timing Semantics

Purpose
-------
Standardize register effective-timing and shadow/commit semantics to avoid runtime ambiguity and to provide a single authoritative source for C↔RTL parity and verification.

Required enumerations
---------------------
Each register must specify one of the following `Shadow` semantics.

- `STATIC` (BOOT_ONLY)
  - Description: Set at build or boot time and not changeable at runtime.
  - Use case: hardware-structural choices (e.g. mesh density, scratchpad layout).

- `IMMEDIATE`
  - Description: Writes take effect as soon as possible and may be observed within the current control flow. No line/frame boundary guarantees.
  - Use case: debug toggles or non-pixel-path controls that do not cause visible transient states.

- `LINE_BOUNDARY`
  - Description: The new value becomes visible at the next source-line boundary. Prevents discontinuities inside a scanline.
  - Use case: registers that affect line-level caches or per-line sampling windows.

- `FRAME_BOUNDARY`
  - Description: The new value becomes visible at the next frame boundary; remains constant within a frame to avoid visible intra-frame jumps.
  - Use case: algorithm calibration parameters (color matrices, global gains, LUT swaps, etc.).

- `STAGED_COMMIT`
  - Description: Writes are placed into a shadow copy. An explicit `COMMIT`/`CONFIG_COMMIT` action (or an agreed protocol) atomically replaces the active copy, typically at a `FRAME_BOUNDARY`.
  - Use case: atomic, verifiable bulk parameter swaps during calibration flows.

- `DOUBLE_BUFFER` (swap-trigger)
  - Description: The data (table or register file) is double-buffered. A `swap_trigger` causes the active buffer to switch, typically at a `FRAME_BOUNDARY` or `COMMIT` event.
  - Use case: large tables (LUTs, meshes) that must be pre-written and swapped in without transient inconsistency.

Required table fields and constraints
-----------------------------------
Every register entry in the register table must include the following fields:

- `Shadow`: One of `STATIC|IMMEDIATE|LINE_BOUNDARY|FRAME_BOUNDARY|STAGED_COMMIT|DOUBLE_BUFFER`.
- `Lifetime`: `BOOT_ONLY` or `RUNTIME` (whether the register can be modified at runtime).
- `UpdateTrigger` (optional): further detail for `STAGED_COMMIT` / `DOUBLE_BUFFER` such as `IMMEDIATE|COMMIT|AUTO_FRAME`.
- `Category`: `CONTROL` or `ALGORITHM` (see the register classification rule).

Example rows:

| Register | Bits | Type | Default | Shadow | Lifetime | UpdateTrigger | Category | Description |
|---|---:|---|---:|---:|---:|---:|---:|---|
| LUT_BASE_A | AXI_ADDR | - | 0 | DOUBLE_BUFFER | RUNTIME | COMMIT | ALGORITHM | Primary LUT slot A base address (double-buffered; swap on COMMIT) |
| GLOBAL_GAIN | U12.10 | - | 1024 | FRAME_BOUNDARY | RUNTIME | AUTO_FRAME | ALGORITHM | Global multiplicative gain; valid per-frame |
| OUTPUT_RING_DEPTH | U8 | - | 32 | STATIC | BOOT_ONLY | - | CONTROL | SoC integration choice; set at boot only |

Conflict resolution and enforcement
-----------------------------------

- If a register is classified `CONTROL` but changing it causes a change to the algorithm's numeric output (visible pixel/result differences), then one of the following must be done:
  - Reclassify the register as `ALGORITHM`, or
  - Provide a C-simulatable equivalent and a regression vector in the PR (see `validation_and_ci` guidance), and mark `Shadow` with a reproducible semantics (e.g. `FRAME_BOUNDARY` or `STAGED_COMMIT`).

- Do not use `IMMEDIATE` for algorithm parameters that can cause visible pixel interruptions (for example, direct color-matrix or LUT index updates).

- All `STAGED_COMMIT` and `DOUBLE_BUFFER` flows must include verification checkpoints: pre-write validation (checksum/length), commit-time compliance checks, and a post-commit smoke/regression vector.

PR and documentation checklist (required)
---------------------------------------

Every PR that adds or modifies registers must include:

- A register table with `Shadow`, `Lifetime`, and `Category` columns filled.
- If `Category` or `Shadow` is changed, an explanation in the PR plus regression test steps.
- For `ALGORITHM` registers, a minimal C↔reference regression vector or a link to an existing validated test set.

Adoption practices (recommended)
--------------------------------

- Default algorithm parameters to `FRAME_BOUNDARY` or `STAGED_COMMIT`.
- Default control parameters to `IMMEDIATE` when they do not affect the pixel pipeline, otherwise `LINE_BOUNDARY`.
- Use `DOUBLE_BUFFER` + `COMMIT` for large tables or data blobs.

Automation suggestions
----------------------

- Provide a small script that generates header files from the register markdown table and validates presence of `Shadow`/`Lifetime`/`Category` fields. Prefer blocking CI when required fields are missing.

Canonical source
----------------

This file is the canonical definition for shadow/update timing semantics. Other rule files should reference this document as the single source of truth for `Shadow` semantics.

