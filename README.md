# 🚀 AlgPrompt — Reusable CLAUDE.md Generator for Algorithm Projects

A modular framework for generating **`CLAUDE.md`** agent instruction files.  
When you start a new algorithm / IC / platform project, use this tool to assemble a complete, battle-tested set of agent rules in seconds — instead of writing from scratch.

---

## ✨ Features

- **Modular rule blocks** — each rule is a standalone `.md` snippet in [`_rules/`](_rules/), easy to edit or extend.
- **Predefined profiles** — pick `python_research`, `python_to_c`, `full_ic`, or `webapp` to get a curated rule set instantly.
- **YAML config mode** — declare your project metadata + profile in a `.yaml` file, generate reproducibly.
- **Interactive mode** — step-by-step CLI wizard to build your first CLAUDE.md.
- **Custom sections** — append project-specific rules on top of the standard set.
- **Auto-numbering** — sections are numbered automatically based on the rules you select.

---

## 📦 Repository Structure

```text
AlgPrompt/
├── generate_claude_md.py        # Generator script (main entry point)
├── _template/
│   └── CLAUDE.md.template       # Master template skeleton
├── _rules/                      # Modular rule blocks (the building blocks)
│   ├── core_behavior.md         #   ├─ [essential] Core behavior constraints
│   ├── quality_first.md         #   ├─ [essential] Quality-first algorithm rule
│   ├── debug.md                 #   ├─ [essential] Debug methodology
│   ├── python_prototype.md      #   ├─ [essential] Python prototyping guidelines
│   ├── visualization.md         #   ├─ [essential] Visual observability mandate
│   ├── python_c_equivalence.md  #   ├─ [porting]   Python↔C comparison methodology
│   ├── fixed_point_c.md         #   ├─ [porting]   Fixed-point notation & tables
│   ├── rtl_friendly.md          #   ├─ [hardware]  RTL/line-buffer design rules
│   ├── config_register.md       #   ├─ [hardware]  Register table documentation
│   ├── report.md                #   ├─ [essential] Report & documentation standards
│   ├── handoff.md               #   ├─ [essential] Agent handoff template
│   └── ask_before_destructive.md #  └─ [essential] Destructive action safety
├── examples/                    # Example YAML configs
│   ├── denoiser.yaml            #   ├─ Python→C ISP denoiser
│   ├── warp_engine.yaml         #   ├─ Full IC distortion correction
│   └── web_platform.yaml        #   └─ Flask web platform
├── .gitignore
└── README.md                    # This file
```

---

## 🚀 Quick Start

### Option 1: Interactive Mode

```bash
python generate_claude_md.py --interactive
```

The wizard walks you through profile selection, project info, and rule picking.

### Option 2: YAML Config Mode

```bash
# Generate from a config
python generate_claude_md.py --config examples/denoiser.yaml

# Override output path
python generate_claude_md.py --config examples/denoiser.yaml --out D:\my_project\CLAUDE.md
```

### Option 3: List Available Rules & Profiles

```bash
python generate_claude_md.py --list-rules
python generate_claude_md.py --list-profiles
```

---

## 📋 Profiles

| Profile | Description | Included Rules |
|:---|:---|:---|
| `python_research` | Pure Python algorithm R&D | core, quality, debug, python, viz, report, handoff, safety |
| `python_to_c` | Algorithm R&D + planned C porting | Above + python/C equiv, fixed-point |
| `full_ic` | Full IC: Python → C → FP → RTL | Above + RTL-friendly, config register |
| `webapp` | Web application / platform | core, debug, report, handoff, safety |

---

## 🧩 Rule Tiers

| Tier | Rules | When to use |
|:---|:---|:---|
| **essential** | `core_behavior`, `quality_first`, `debug`, `python_prototype`, `visualization`, `report`, `handoff`, `ask_before_destructive` | Every algorithm project |
| **porting** | `python_c_equivalence`, `fixed_point_c` | When a C model is planned |
| **hardware** | `rtl_friendly`, `config_register` | When targeting ASIC / FPGA / RTL |

---

## 🔧 How to Add a New Rule

1. Create a new `.md` file in `_rules/`, for example `_rules/my_new_rule.md`.
2. Start the file with a `## Title` heading.
3. Register it in `generate_claude_md.py` → `RULE_CATALOG`:

```python
RULE_CATALOG = {
    ...
    "my_new_rule": {"file": "my_new_rule.md", "label": "My New Rule", "tier": "essential"},
}
```

4. Optionally add it to a profile in `PROFILES`.

---

## 📝 YAML Config Reference

```yaml
# Required
project_title: "My Algorithm"
agent_role: "You are an algorithm engineer."
project_description: |
  Multi-line description of the project.

# Profile OR explicit rule list (pick one)
profile: python_to_c          # Use a predefined profile
# rules:                      # OR list rules explicitly
#   - core_behavior
#   - debug
#   - python_prototype

# Optional
extra_rules:                   # Add on top of a profile
  - config_register
status: "Project just started."
contract: "def process(x) -> y"
file_structure: |
  src/
  tests/
  docs/
custom_sections: |             # Free-form markdown appended after rules
  ## My Project-Specific Rule
  Content here.
output: "./CLAUDE.md"          # Output path
```

---

## 📄 License

Internal use. Adapt freely for your algorithm development workflow.
