## Input Sources and Outcome Definition

Purpose
-------
When a task or request does not include an explicit input data source or a clear target outcome, the agent (person or automated tool) must proactively define and document both before running experiments, tuning parameters, or producing deliverables.

Required steps
--------------
1. Propose candidate input sources (2–3 options)
   - For each candidate provide: source/location, data format, representative sample or snippet, expected size, and any privacy/licensing constraints.
   - Candidates may include: public datasets, internal datasets (location + access instructions), or a synthetic-data generator specification.

2. Generate or acquire inputs when necessary
   - If no suitable source exists and the user allows, provide a reproducible synthetic-data generator (script + seed + parameters) and produce example outputs.
   - Record provenance: generator code, seed, parameters, and any external downloads (URL + checksum).

3. Define measurable target outcomes
   - Specify metrics (examples: MAE, RMSE, PSNR, accuracy, throughput, memory, latency), numeric thresholds, and visual acceptance criteria.
   - Provide a baseline (reference) and pass/fail rules for each metric.
   - Where applicable include qualitative acceptance notes ("no visible banding", "no frame tearing").

4. Require explicit approval or an auto-approve policy
   - Present the chosen inputs and outcome definitions and request user confirmation before running large experiments.
   - If an `auto-approve` policy is provided by the user, proceed but log the choices and notify the user of actions taken.

5. Record decisions, tests, and artifacts
   - Commit the chosen input spec, generator, and outcome criteria into the repository (docs or `tests/`) and include a minimal regression vector or smoke test demonstrating the acceptance check.
   - Log provenance metadata alongside artifacts (who picked it, when, and why).

6. Re-evaluate before tuning
   - If results fail the defined outcomes, diagnose algorithmic issues first (see `tune_algorithm_first.md`) rather than immediately adjusting parameters to mask failures.

PR checklist
------------
- Add or update a document under `_rules/` or `docs/` describing the chosen input and outcome definitions.
- Include sample data or a small synthetic generator example, plus provenance metadata.
- For long-running or costly experiments, require user approval or an explicit `auto-approve` in the PR description.

Example minimal workflow
------------------------
1. Agent proposes three candidate sources: public_sample_A (URL), internal_bundle_B (`data/calibration/v1/`), synthetic_generator_C (script + seed).
2. User approves candidate C.
3. Agent runs generator_C with seed `42`, produces `tests/sample_input_42.bin` and commits the generator and sample.
4. Agent defines acceptance metrics: RMSE < 0.5 px and no visible ghosting on the provided sample, and runs smoke tests.
5. Results and artifacts are committed and linked in PR for review.

Notes
-----
- This rule prevents ad-hoc assumptions about inputs and outcomes, improves reproducibility, and makes experimental choices auditable.
- Keep the generated samples small and documented; do not embed large binary blobs in PRs—use artifact storage or `outputs/` with references when needed.
