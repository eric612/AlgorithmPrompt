## Report Rule

Use Markdown as the source of truth.

Reports must be readable in GitLab / GitHub.

Use relative paths for images.

Avoid PDF-only, PPT-only, HTML-only, or font-dependent documentation.

For each algorithm stage, documentation should include:

- concept
- formula
- how to run
- expected visual result
- known limitations
- next step

Recommended docs layout:

```text
docs/00_problem_definition.md
docs/01_algorithm_principle.md
docs/02_algorithm_flow.md
docs/03_visual_debugging.md
docs/04_future_porting.md
docs/handoff.md
```
