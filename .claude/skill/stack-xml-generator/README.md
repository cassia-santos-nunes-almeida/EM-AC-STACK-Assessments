# stack-xml-generator

A Claude skill for generating randomized Moodle STACK assessment questions with Maxima CAS, PRT grading trees, and progressive hints.

## What It Does

- Generates well-structured STACK XML ready for Moodle import
- Enforces mandatory syntax hints after every input field
- Builds robust PRT grading trees with correct answer test selection
- Includes progressive hints for student learning
- Validates XML/CAS safety (CDATA wrapping, exact arithmetic, etc.)
- Supports numerical, algebraic, MCQ (dropdown/radio), and essay inputs

## Files

```
stack-xml-generator/
├── SKILL.md                           # Skill instructions
├── README.md                          # This file
└── references/
    └── stack-xml-conventions.md       # Complete XML structure reference with examples
```

## Usage

### Claude Code

```bash
cp -r stack-xml-generator/ /path/to/your-project/.claude/skill/
```

### Claude Projects (ZIP)

```bash
cd stack-xml-generator
zip -r ../stack-xml-generator.zip SKILL.md references/
```

Upload to **Claude.ai -> Settings -> Skills**.

## Domain-Specific Extensions

This skill is **generic** — it works for any subject. To add domain-specific rules (e.g., specific formulas, grading policies, content constraints), use the [project-context-manager](../project-context-manager/) skill alongside it and document your domain conventions in `context.md`.

## License

CC0 1.0 Universal — public domain, no restrictions.
