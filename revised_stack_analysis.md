# REVISED: STACK Content Overlap Analysis

> **IMPORTANT:** Before executing ANY file edits from this plan or from `analysis.md`, 
> create a git snapshot commit of all current files. See `analysis.md` Phase 0.

## The key insight I missed

The `stack-xml-generator` skill (from the separate my-claude-skill repo) is a **generic, reusable skill** 
that already contains most of the STACK conventions currently duplicated in CLAUDE.md. 

This means my earlier recommendation to create a "new stack-authoring/SKILL.md" was WRONG — 
that skill already exists. The real problem is a THREE-WAY duplication.

---

## Side-by-side: What lives where NOW

| Content | CLAUDE.md | stack-xml-generator/SKILL.md | stack-xml-conventions.md | PATTERNS.md |
|---------|-----------|------------------------------|--------------------------|-------------|
| Syntax hints table | ✅ Lines 196-215 | ✅ (identical) | — | — |
| Progressive hints spec | ✅ Lines 217-224 | ✅ (identical) | ✅ example in XML | — |
| Grading (PRT) rules table | ✅ Lines 226-234 | ✅ (identical) | ✅ PRT patterns | P-STACK-02,05,07 |
| Input configuration table | ✅ Lines 237-244 | ✅ (identical) | ✅ input types | P-STACK-10,13 |
| PRT Validation (4 tiers) | ✅ Lines 372-398 | ✅ (identical) | — | P-STACK-08 |
| Maxima randomization | ✅ Lines 249-255 | ✅ (identical) | ✅ quick reference | P-STACK-09 |
| Exact arithmetic rule | ✅ (in Maxima section) | ✅ Common Mistakes #2 | ✅ in quick ref | P-STACK-06 |
| CDATA wrapping | ✅ Tier 3 | ✅ Common Mistakes #3 | — | P-STACK-04 |
| **RLC circuit formulas** | ✅ Lines 257-273 | ❌ | ❌ | ❌ |
| **Damping classification** | ✅ Lines 269-273 | ❌ | ❌ | ❌ |
| **Multi-switch topology** | ✅ Lines 345-370 | ❌ | ❌ | ❌ |
| **JSXGraph patterns** | ❌ | ❌ | ❌ | ✅ P-STACK-16–20 |
| Common Mistakes list | ❌ (scattered) | ✅ 7 items | — | ✅ 20 entries |

### What this reveals:

**Generic STACK rules** (syntax hints, PRT rules, validation, input config, Maxima patterns):
→ Exist in THREE places: CLAUDE.md, stack-xml-generator/SKILL.md, and PATTERNS.md
→ This is the worst duplication in the entire system

**Project-specific content** (RLC formulas, damping, multi-switch topology):
→ Exists ONLY in CLAUDE.md — these are the lines that MUST stay somewhere in this repo

**JSXGraph authoring knowledge**:
→ Exists ONLY in PATTERNS.md as 5 individual entries — no consolidated guide anywhere

---

## Corrected recommendation

### ❌ DO NOT create a new stack-authoring/SKILL.md
That skill already exists as `stack-xml-generator`. Creating another one would make the duplication WORSE.

### ✅ DO THIS instead:

**Step 1: Remove generic STACK content from CLAUDE.md**
The following sections can be removed because they are fully covered by stack-xml-generator/SKILL.md:
- Syntax hints table (lines 196-215) → covered by skill
- Progressive hints spec (lines 217-224) → covered by skill  
- Grading (PRT) rules table (lines 226-234) → covered by skill
- Input configuration table (lines 237-244) → covered by skill
- PRT Validation Methodology (lines 372-398) → covered by skill
- Maxima randomization example (lines 249-255) → covered by skill

Replace with a single reference line:
```markdown
## STACK Conventions
All generic STACK XML, Maxima CAS, and PRT validation rules → see stack-xml-generator skill.
```

**Step 2: Keep project-specific STACK content in CLAUDE.md (much smaller)**
These lines stay because they are EM&AC course-specific and NOT in the generic skill:
- RLC Circuit Formulas table (lines 257-268) — ~12 lines
- Damping classification (lines 269-273) — ~5 lines  
- Multi-switch topology rules (lines 345-370) — ~25 lines

Total: ~42 lines instead of ~205 lines of STACK content.

**Step 3: Add JSXGraph section to stack-xml-generator (not a new skill)**
JSXGraph is a STACK feature, not a separate domain. The 5 patterns (P-STACK-16 to P-STACK-20) 
should be consolidated into a new section in the generic skill:
- Add `## JSXGraph Integration` section to stack-xml-generator/SKILL.md
- Add `references/jsxgraph-conventions.md` for the detailed patterns
- Patterns STAY in PATTERNS.md (they're corrections, not conventions)
- The skill section is the "how to do it right" guide; patterns are "what went wrong"

**Step 4: Add stack-xml-generator to the Skill Index in CLAUDE.md**
Currently only 2 skills listed. This should show all skills including the stack generator.

---

## Updated line count projection for CLAUDE.md

| Section | Current lines | After migration |
|---------|--------------|----------------|
| §1 Project Identity | 21 | 21 (no change) |
| §2 Behavior Defaults | 15 | 15 (no change) |
| §3 Task Decomposition | 30 | 30 (merge with §Workflow, net same) |
| §4 Self-Verification | 8 | 8 (no change) |
| §5 Session Protocols | 28 | 30 (+preferences.md in read list) |
| §6 Cross-Skill Rules | 20 | 20 (no change) |
| §7 Skill Index | 6 | 12 (expand to all skills) |
| Project Overview | 12 | 0 (→ context.md only) |
| Repo Structure | 33 | 0 (→ context.md only) |
| Adding New Content | 7 | 0 (→ context.md only) |
| STACK Conventions (generic) | ~160 | 2 (reference to skill) |
| STACK (project-specific: RLC, damping, switches) | ~42 | 42 (stays) |
| CircuiTikZ section | ~95 | 0 (→ circuitikz/SKILL.md) |
| Diagram Style | ~30 | 0 (→ circuitikz/SKILL.md) |
| PRT Validation | 27 | 0 (→ skill) |
| Known Issues | 7 | 0 (→ SESSION.md) |
| Workflow Guidelines | 23 | 0 (merged into §3) |
| **TOTAL** | **465** | **~180** |

---

## Updated migration checklist (STACK-related items only)

| # | Content | Source | Destination | Action |
|---|---------|--------|-------------|--------|
| 17 | Syntax hints table | CLAUDE.md + stack-skill | stack-xml-generator ONLY | Delete from CLAUDE.md |
| 18 | Progressive hints spec | CLAUDE.md + stack-skill | stack-xml-generator ONLY | Delete from CLAUDE.md |
| 19 | Grading (PRT) rules | CLAUDE.md + stack-skill | stack-xml-generator ONLY | Delete from CLAUDE.md |
| 20 | Input config table | CLAUDE.md + stack-skill | stack-xml-generator ONLY | Delete from CLAUDE.md |
| 21 | PRT Validation (4 tiers) | CLAUDE.md + stack-skill | stack-xml-generator ONLY | Delete from CLAUDE.md |
| 22 | Maxima randomization | CLAUDE.md + stack-skill | stack-xml-generator ONLY | Delete from CLAUDE.md |
| 23 | **RLC formulas** | CLAUDE.md only | **CLAUDE.md (stays)** | No change |
| 24 | **Damping classification** | CLAUDE.md only | **CLAUDE.md (stays)** | No change |
| 25 | **Multi-switch topology** | CLAUDE.md only | **CLAUDE.md (stays)** | No change |
| 34 | JSXGraph patterns | PATTERNS.md | PATTERNS.md (stays) + stack-xml-generator (new section) | Add to skill |

---

## Full revised file structure

```
EM-AC-STACK-Assessments/           # (confirm repo name)
├── CLAUDE.md                       # ~180 lines: identity + rules + EM&AC-specific conventions
├── PATTERNS.md                     # Keep as-is (clean up duplicate template)
├── SESSION.md                      # Keep as-is (ephemeral)
├── .claude/
│   ├── context.md                  # Single source: project overview, tree, content summaries, 
│   │                               #   constraints, Never Suggest (remove duplicates)
│   ├── decisions-log.md            # Keep + catch-up weeks 12-13
│   ├── preferences.md              # Keep (clean placeholder, update date)
│   └── skills/
│       ├── context-evaluator/
│       │   └── SKILL.md            # Keep (thin router)
│       └── circuitikz/
│           └── SKILL.md + refs     # Absorb CLAUDE.md CircuiTikZ content
├── docs/
│   ├── 00_prompt_evaluation.md     # Keep (documentation, not context)
│   └── 01_exam_overview.md         # Keep (documentation, not context)
└── ...

my-claude-skill/ (separate repo)
└── stack-xml-generator/
    ├── SKILL.md                    # Generic STACK conventions (already exists)
    ├── references/
    │   ├── stack-xml-conventions.md  # XML reference (already exists)
    │   └── jsxgraph-conventions.md   # NEW: consolidated JSXGraph authoring guide
    └── README.md
```

### Key difference from my earlier plan:
- **No new stack-authoring skill** — the generic one already exists
- **No new jsxgraph skill folder** — it's a section within stack-xml-generator
- **CLAUDE.md keeps only 42 lines of STACK content** (the EM&AC-specific parts)
- **Everything else is deduplication**, not creation

---

## Self-Verification Rule (applies to entire migration)

Self-verify your work by testing it end to end. Do not return control until you have met the requirements and the result is working as expected and optimized.

After completing all edits, walk the full migration checklist in `analysis.md` §8 row by row, open each destination file, and confirm the content is present. Check that every duplication now exists in exactly one file, every orphaned item survived, and every cross-reference points to an existing file and section. Run the original audit prompt again and confirm all scores improved. If anything regressed, fix it before returning control.
