#!/usr/bin/env python3
from __future__ import annotations
"""
AlgPrompt CLAUDE.md Generator
==============================

Assembles a project-specific CLAUDE.md from reusable rule blocks.

Usage:
    python generate_claude_md.py --interactive
    python generate_claude_md.py --config my_project.yaml
    python generate_claude_md.py --config my_project.yaml --out /path/to/CLAUDE.md

The generator reads rule snippets from `_rules/` and fills the template
structure defined in `_template/CLAUDE.md.template`.
"""

import argparse
import os
import sys
import textwrap
from pathlib import Path

# ──────────────────────────────────────────────────────────
# Rule registry — order matters (determines section numbering)
# ──────────────────────────────────────────────────────────
RULE_CATALOG = {
    "core_behavior":        {"file": "core_behavior.md",        "label": "Core Behavior",             "tier": "essential"},
    "quality_first":        {"file": "quality_first.md",        "label": "Quality-First Algorithm",   "tier": "essential"},
    "debug":                {"file": "debug.md",                "label": "Debug",                     "tier": "essential"},
    "python_prototype":     {"file": "python_prototype.md",     "label": "Python Prototype",          "tier": "essential"},
    "visualization":        {"file": "visualization.md",        "label": "Visualization",             "tier": "essential"},
    "python_c_equivalence": {"file": "python_c_equivalence.md", "label": "Python/C Equivalence",      "tier": "porting"},
    "fixed_point_c":        {"file": "fixed_point_c.md",        "label": "Fixed-Point C",             "tier": "porting"},
    "rtl_friendly":         {"file": "rtl_friendly.md",         "label": "RTL-Friendly",              "tier": "hardware"},
    "config_register":      {"file": "config_register.md",      "label": "Config Register",           "tier": "hardware"},
    "report":               {"file": "report.md",               "label": "Report",                    "tier": "essential"},
    "handoff":              {"file": "handoff.md",              "label": "Handoff",                   "tier": "essential"},
    "ask_before_destructive": {"file": "ask_before_destructive.md", "label": "Ask-Before-Destructive", "tier": "essential"},
}

# Predefined profiles — pick rules quickly
PROFILES = {
    "python_research": {
        "description": "Pure Python algorithm R&D (no C / no RTL)",
        "rules": [
            "core_behavior", "quality_first", "debug",
            "python_prototype", "visualization",
            "report", "handoff", "ask_before_destructive",
        ],
    },
    "python_to_c": {
        "description": "Algorithm R&D with planned C model porting",
        "rules": [
            "core_behavior", "quality_first", "debug",
            "python_prototype", "visualization",
            "python_c_equivalence", "fixed_point_c",
            "report", "handoff", "ask_before_destructive",
        ],
    },
    "full_ic": {
        "description": "Full IC pipeline: Python → C → Fixed-point → RTL",
        "rules": [
            "core_behavior", "quality_first", "debug",
            "python_prototype", "visualization",
            "python_c_equivalence", "fixed_point_c",
            "rtl_friendly", "config_register",
            "report", "handoff", "ask_before_destructive",
        ],
    },
    "webapp": {
        "description": "Web application / automation platform",
        "rules": [
            "core_behavior", "debug",
            "report", "handoff", "ask_before_destructive",
        ],
    },
}

SCRIPT_DIR = Path(__file__).resolve().parent
RULES_DIR = SCRIPT_DIR / "_rules"


def load_rule(rule_key: str) -> str:
    """Load a rule markdown snippet from _rules/ directory."""
    meta = RULE_CATALOG[rule_key]
    path = RULES_DIR / meta["file"]
    if not path.exists():
        print(f"  ⚠ Warning: rule file not found: {path}")
        return f"## {meta['label']}\n\n> TODO: fill in rule content\n"
    return path.read_text(encoding="utf-8").strip()


def generate_claude_md(
    project_title: str,
    agent_role: str,
    project_description: str,
    status_block: str,
    contract_block: str,
    file_structure: str,
    selected_rules: list[str],
    custom_sections: str = "",
) -> str:
    """Assemble the final CLAUDE.md content."""

    lines = []

    # ── Header ──
    lines.append(f"# Agent Instructions — {project_title}\n")
    lines.append(f"{agent_role}\n")
    lines.append(f"{project_description}\n")
    lines.append("---\n")

    # ── Status ──
    lines.append("## 0. STATUS\n")
    lines.append(f"{status_block}\n")
    lines.append("---\n")

    # ── Contract ──
    lines.append("## 1. The Contract\n")
    lines.append(f"{contract_block}\n")
    lines.append("---\n")

    # ── Rules (auto-numbered from 2) ──
    for i, rule_key in enumerate(selected_rules, start=2):
        content = load_rule(rule_key)
        # Replace the leading "## Title" with the numbered version
        first_line_end = content.find("\n")
        if first_line_end > 0:
            original_title = content[:first_line_end].lstrip("#").strip()
            numbered_content = f"## {i}. {original_title}\n{content[first_line_end:]}"
        else:
            numbered_content = f"## {i}. {rule_key}\n\n{content}"
        lines.append(numbered_content)
        lines.append("\n---\n")

    # ── Custom sections ──
    if custom_sections.strip():
        lines.append(custom_sections.strip())
        lines.append("\n\n---\n")

    # ── File Structure ──
    next_num = len(selected_rules) + 2
    lines.append(f"## {next_num}. File Structure\n")
    lines.append("```text")
    lines.append(file_structure)
    lines.append("```\n")
    lines.append("---\n")

    # ── Agent Response Format ──
    lines.append(f"## {next_num + 1}. Agent Response Format\n")
    lines.append(textwrap.dedent("""\
        After making changes, report:

        1. Files created or modified
        2. How to run
        3. What the user should see
        4. Current limitations
        5. Suggested next step

        Keep the report concise and actionable.
    """))

    return "\n".join(lines)


def interactive_mode() -> None:
    """Walk the user through project setup interactively."""

    print("=" * 60)
    print("  AlgPrompt — CLAUDE.md Generator (Interactive)")
    print("=" * 60)

    # ── Profile selection ──
    print("\n📋 Available profiles:\n")
    profile_keys = list(PROFILES.keys())
    for i, key in enumerate(profile_keys, 1):
        p = PROFILES[key]
        print(f"  [{i}] {key:20s} — {p['description']}")
    print(f"  [{len(profile_keys) + 1}] {'custom':20s} — Pick rules individually")

    choice = input("\nSelect profile number: ").strip()
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(profile_keys):
            selected_profile = profile_keys[idx]
            selected_rules = PROFILES[selected_profile]["rules"]
            print(f"\n✓ Using profile: {selected_profile}")
            print(f"  Rules: {', '.join(selected_rules)}")
        else:
            # Custom mode
            selected_rules = _pick_rules_interactively()
    except ValueError:
        selected_rules = _pick_rules_interactively()

    # ── Project info ──
    print("\n" + "-" * 40)
    project_title = input("Project title (e.g., 'Image Denoiser'): ").strip()
    if not project_title:
        project_title = "My Algorithm Project"

    agent_role = input("Agent role (e.g., 'You are an ISP algorithm engineer.'): ").strip()
    if not agent_role:
        agent_role = "You are an algorithm development assistant."

    print("\nProject description (multi-line, end with empty line):")
    desc_lines = []
    while True:
        line = input()
        if not line:
            break
        desc_lines.append(line)
    project_description = "\n".join(desc_lines) if desc_lines else "TODO: describe this project."

    status_block = input("\nInitial status (one line, or 'TODO'): ").strip() or "Project initialized. No milestones yet."
    contract_block = input("API contract (one line summary, or 'TODO'): ").strip() or "TODO: define the primary API / function signature."

    print("\nFile structure (multi-line, end with empty line):")
    fs_lines = []
    while True:
        line = input()
        if not line:
            break
        fs_lines.append(line)
    file_structure = "\n".join(fs_lines) if fs_lines else "src/          # main source\ntests/        # tests\ndocs/         # documentation\noutputs/      # results (gitignored)"

    # ── Output path ──
    out_path = input("\nOutput path (default: ./CLAUDE.md): ").strip() or "./CLAUDE.md"

    # ── Generate ──
    result = generate_claude_md(
        project_title=project_title,
        agent_role=agent_role,
        project_description=project_description,
        status_block=status_block,
        contract_block=contract_block,
        file_structure=file_structure,
        selected_rules=selected_rules,
    )

    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(result, encoding="utf-8")
    print(f"\n✅ Generated: {out.resolve()}")
    print(f"   Total rules: {len(selected_rules)}")
    print(f"   Total lines: {result.count(chr(10)) + 1}")


def _pick_rules_interactively() -> list[str]:
    """Let the user pick individual rules."""
    print("\n📋 Available rules:\n")
    keys = list(RULE_CATALOG.keys())
    for i, key in enumerate(keys, 1):
        meta = RULE_CATALOG[key]
        print(f"  [{i:2d}] {key:25s} [{meta['tier']:9s}]  {meta['label']}")

    picks = input("\nEnter rule numbers (comma-separated, e.g., 1,2,3,5): ").strip()
    selected = []
    for token in picks.split(","):
        token = token.strip()
        if token.isdigit():
            idx = int(token) - 1
            if 0 <= idx < len(keys):
                selected.append(keys[idx])
    if not selected:
        print("  ⚠ No valid rules selected, using essential set.")
        selected = [k for k, v in RULE_CATALOG.items() if v["tier"] == "essential"]
    return selected


def config_mode(config_path: str, out_path: str | None) -> None:
    """Generate from a YAML config file."""
    try:
        import yaml
    except ImportError:
        print("ERROR: PyYAML is required for config mode.")
        print("  pip install pyyaml")
        sys.exit(1)

    cfg_path = Path(config_path)
    if not cfg_path.exists():
        print(f"ERROR: config file not found: {cfg_path}")
        sys.exit(1)

    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    # Resolve profile -> rules
    if "profile" in cfg and cfg["profile"] in PROFILES:
        rules = list(PROFILES[cfg["profile"]]["rules"])
    elif "rules" in cfg:
        rules = cfg["rules"]
    else:
        rules = [k for k, v in RULE_CATALOG.items() if v["tier"] == "essential"]

    # Add extra rules
    if "extra_rules" in cfg:
        for r in cfg["extra_rules"]:
            if r not in rules:
                rules.append(r)

    result = generate_claude_md(
        project_title=cfg.get("project_title", "My Project"),
        agent_role=cfg.get("agent_role", "You are an algorithm development assistant."),
        project_description=cfg.get("project_description", "TODO"),
        status_block=cfg.get("status", "Project initialized."),
        contract_block=cfg.get("contract", "TODO: define API contract."),
        file_structure=cfg.get("file_structure", "src/\ntests/\ndocs/"),
        selected_rules=rules,
        custom_sections=cfg.get("custom_sections", ""),
    )

    dest = Path(out_path) if out_path else Path(cfg.get("output", "./CLAUDE.md"))
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(result, encoding="utf-8")
    print(f"✅ Generated: {dest.resolve()}")
    print(f"   Profile: {cfg.get('profile', 'custom')}")
    print(f"   Rules: {len(rules)}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate a CLAUDE.md from reusable rule blocks.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              python generate_claude_md.py --interactive
              python generate_claude_md.py --config examples/denoiser.yaml
              python generate_claude_md.py --config examples/denoiser.yaml --out ../MyProject/CLAUDE.md
              python generate_claude_md.py --list-rules
              python generate_claude_md.py --list-profiles
        """),
    )
    parser.add_argument("--interactive", "-i", action="store_true",
                        help="Interactive mode: walk through setup step by step")
    parser.add_argument("--config", "-c", type=str,
                        help="YAML config file for the project")
    parser.add_argument("--out", "-o", type=str, default=None,
                        help="Output file path (overrides config)")
    parser.add_argument("--list-rules", action="store_true",
                        help="List all available rule blocks and exit")
    parser.add_argument("--list-profiles", action="store_true",
                        help="List all predefined profiles and exit")

    args = parser.parse_args()

    if args.list_rules:
        print("\n📋 Available rule blocks:\n")
        for key, meta in RULE_CATALOG.items():
            print(f"  {key:25s} [{meta['tier']:9s}]  {meta['label']}")
            print(f"  {'':25s}  → _rules/{meta['file']}")
        return

    if args.list_profiles:
        print("\n📋 Predefined profiles:\n")
        for key, prof in PROFILES.items():
            print(f"  {key:20s} — {prof['description']}")
            print(f"  {'':20s}   Rules: {', '.join(prof['rules'])}\n")
        return

    if args.interactive:
        interactive_mode()
    elif args.config:
        config_mode(args.config, args.out)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
