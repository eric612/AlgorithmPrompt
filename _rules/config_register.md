## Config Register Rule

Purpose
-------
Define how configuration registers are documented for RTL-facing work. This file prescribes register categories, required table fields, and policies. The canonical timing semantics for register updates (the `Shadow` field) are defined in `_rules/shadow_update_semantics.md` and MUST be referenced for any register table.

Categories
----------
- `CONTROL` — platform, timing, or integration registers that affect how the pipeline runs (performance, memory partitioning, feature enable/disable) but do not directly change the algorithm math. Examples: resolution, buffer depth, bandwidth thresholds.
- `ALGORITHM` — calibration, model, or input-data registers that change the numeric result of the algorithm. Examples: LUT bases, per-pixel gains, color-matrix coefficients, sensor-derived offsets.

Key rules
---------
- Every runtime parameter MUST appear in the register table and include the required metadata fields (see Register Table Format).
- If a `CONTROL` register causes visible changes to algorithm outputs (pixel-level or numeric differences), one of the following MUST be done:
	- reclassify the register to `ALGORITHM`, or
	- provide a C-simulatable equivalent and a regression vector in the PR; the register's `Shadow` semantics must be reproducible (e.g. `FRAME_BOUNDARY` or `STAGED_COMMIT`).
- `ALGORITHM` registers MUST be C-simulatable and covered by a minimal regression test demonstrating equivalence to the reference implementation.

Register Table Format (required)
--------------------------------
All register tables must include the columns below. When in doubt, fill them explicitly.

| Register | Bits | Type | Default | Shadow | Lifetime | UpdateTrigger | Category | Description |
|---|---:|---|---:|---:|---:|---:|---:|---|

- `Shadow`: One of the enumerations defined in `_rules/shadow_update_semantics.md` (e.g. `FRAME_BOUNDARY`, `STAGED_COMMIT`, `IMMEDIATE`).
- `Lifetime`: `BOOT_ONLY` or `RUNTIME`.
- `UpdateTrigger` (optional): further detail for staged flows (`COMMIT`, `AUTO_FRAME`, `IMMEDIATE`).
- `Category`: `CONTROL` or `ALGORITHM`.

Example rows
------------

| Register | Bits | Type | Default | Shadow | Lifetime | UpdateTrigger | Category | Description |
|---|---:|---|---:|---:|---:|---:|---:|---|
| LUT_BASE_A | AXI_ADDR | - | 0 | DOUBLE_BUFFER | RUNTIME | COMMIT | ALGORITHM | Primary LUT slot A base address (double-buffered; swap on COMMIT) |
| GLOBAL_GAIN | U12.10 | - | 1024 | FRAME_BOUNDARY | RUNTIME | AUTO_FRAME | ALGORITHM | Global multiplicative gain; valid per-frame |
| OUTPUT_RING_DEPTH | U8 | - | 32 | STATIC | BOOT_ONLY | - | CONTROL | SoC integration choice; set at boot only |

Policies and PR checklist
-------------------------
- Any change to registers must: include the updated register table with `Shadow`, `Lifetime`, and `Category` columns filled; explain why the change is necessary; list expected impact and required regression tests.
- For `ALGORITHM` registers, provide a minimal C↔reference regression vector or a link to an existing validated test set in the PR.
- For `STAGED_COMMIT` / `DOUBLE_BUFFER` flows, include pre-write validation (checksum/length), commit-time checks, and a post-commit smoke/regression vector.

Reference
---------
Use `_rules/shadow_update_semantics.md` as the single source of truth for `Shadow` semantics and related enforcement rules. Integrate simple CI checks to validate presence of required fields in register tables.

Every runtime parameter must be included in the register table.
