# Business Expert Skill

MBB-style business strategy consultant skill for Claude Code. Provides structured, hypothesis-driven, MECE approach to business problems — grounded in data, supported by evidence, and delivered as compelling narratives.

## Overview

This skill enables Claude to act as an MBB-caliber strategy consultant, helping users solve business problems using:
- **MECE decomposition** — Break problems into mutually exclusive, collectively exhaustive components
- **Hypothesis-driven approach** — Form a point of view early, then seek data to prove or disprove it
- **Pyramid principle** — Lead with the answer, support with storylines, back each with evidence
- **BCG patterns** — Action-oriented headlines, "Implications to [client]", specific numbers, named competitors

## When to Use

Use this skill for:
- Market entry strategy, pricing strategy, M&A analysis
- Competitive analysis, market research, market sizing
- Growth strategy, go-to-market strategy, channel strategy
- Business plans, investment thesis, due diligence
- Operational optimization, cost reduction, supply chain
- Unit economics, profitability analysis, benchmarking
- Industry analysis, competitive landscape, TAM/SAM/SOM

## Key Features

### 6-Phase Workflow

1. **Phase 0: Environment Check** — Setup and configuration
2. **Phase 1: Scope & Clarification** — Align on problem statement and deliverable format
3. **Phase 2: Landscape Research & Preliminary Findings** — Initial research, form hypotheses, mandatory checkpoint
4. **Phase 3: Hypothesis Validation & Recommendations** — Deep dive, validate hypotheses, develop recommendations
5. **Phase 4: Final Checkpoint** — User sign-off on storyline before deliverable
6. **Phase 5: Deliverable Creation** — Build slides + companion .md document
7. **Phase 6: Next Steps & Resumability** — Follow-up actions and save state

### Agent Teams

- **Project Lead (PL)** — You, managing phases and narrative direction
- **Partner** — Quality gate, reviews all work before user sees it
- **Business Experts** — Problem-scoped research (not data-scoped)
- **Deliverable Advisor** — Builds final output with format-specific expertise

### Output Formats

- **Markdown** (.md) — Always produced, provides depth and detail
- **HTML slides** (.html) — Animated, runs in browser, zero dependencies
- **PowerPoint** (.pptx) — Traditional slide deck
- **Word document** (.docx) — Formal report format
- **Notion** — Collaborative, team-editable

**Important:** When user requests slides, BOTH slides and .md document are produced (slides for presenting, .md for depth).

### Parameters

- `--format` — Output format (md, slides, pptx, docx, notion)
- `--length` — Content coverage (3min, 5min, 10min, 10min+)
- `--level` — User knowledge level (executive, analyst, technical)
- `--sources` — Source credibility threshold (strict, balanced, broad)
- `--lang` — Output language (en, zh, etc.)

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/business-expert-skill.git

# Copy to Claude skills directory
cp -r business-expert-skill ~/.claude/skills/business-expert
```

## Usage

```bash
# Basic usage
claude "Analyze the EU paint market for B2C entry"

# With parameters
claude "Should we enter the EU market? --format pptx --length 10min --level executive"

# Resume previous engagement
claude "Continue the market analysis --resume"
```

## Directory Structure

```
business-expert/
├── SKILL.md                    # Main skill definition
├── CHANGES.md                  # Version history and updates
├── references/
│   ├── workflow/               # How to execute
│   │   ├── phases-overview.md  # 6-phase workflow details
│   │   ├── setup-guide.md      # Installation and configuration
│   │   ├── data-sources.md     # Available MCPs, APIs, libraries
│   │   └── pre-delivery-checklist.md  # Quality gates
│   ├── methodology/            # Consulting principles
│   │   ├── agent-teams-guide.md  # Agent teamwork and coordination
│   │   ├── partner-guide.md    # Partner review standards
│   │   └── bcg-patterns.md     # Presentation patterns
│   └── templates/              # Formats and schemas
│       ├── yaml-formats.md     # YAML schemas for process files
│       ├── output-documents.md # Document structure and standards
│       └── output-slides.md    # Slide structure and standards
├── scripts/
│   └── validate_process.py     # Data quality validation
├── skills/                     # Nested output skills
│   ├── frontend-slides/        # HTML slides generation
│   ├── pptx/                   # PowerPoint generation
│   └── docx/                   # Word document generation
└── evals/
    └── evals.json              # Test cases
```

## Key Concepts

### Phase 2 & 3: Internally Iterative

Both research phases are internally iterative — not rigid one-shot:
- **Phase 2:** Research → insights → refine → repeat until preliminary findings are solid
- **Phase 3:** Validate → gaps → research deeper → repeat until satisfied

### The Square Analogy

Think of research space as 2D: X-axis = breadth, Y-axis = depth.
- **Phase 2:** Covers 1/4 of the square (moderate breadth, shallow depth) — preliminary findings
- **Phase 3:** Can go anywhere in remaining space (deep on specific areas, or broader if needed)

### Issue Tree: Two Exposure Levels

- **Internal** (saved to `process/issue-tree.yaml`): Key questions + hypotheses (H1, H2, H3)
- **User-facing:** ASCII tree with key questions + verbal context (no granular hypotheses)

Users see "key questions to answer", not "hypotheses to test" — less internal methodology exposed.

### Mandatory Checkpoints

- **Scope Checkpoint (Phase 1):** User confirms problem statement and format
- **Preliminary Findings Checkpoint (Phase 2):** Share initial research, get feedback before deep dive
- **Final Checkpoint (Phase 4):** User sign-off on storyline before deliverable

## Quality Standards

### Content Density

- **Documents:** Every H2 section must have framing paragraph + 3+ evidence + comparison + implications
- **Slides:** 60-80% evidence slides (headline + 2-3+ evidence + source)

### Minimum Output by Length

| Length | Slides | Words | Team Size |
|--------|--------|-------|-----------|
| 3min | 5-8 | 800-1200 | 2-3 experts |
| 5min | 10-15 | 2000-2500 | 3-4 experts |
| 10min | 20-25 | 4000-5000 | 4-5 experts |
| 10min+ | 30+ | 6000+ | 5-6 experts |

### BCG Patterns

- Action-oriented headlines (not topic-only)
- "Implications to [client]" after every benchmark
- Specific numbers, not vague language
- Named competitors, not "industry peers"
- "Basis of Perspectives" slide showing sources
- "From... To..." framing for transformation narratives

## Recent Updates

### Update 11 (2026-03-02)
- Transformed Phase 2 and Phase 3 to reflect real BCG consulting workflow
- Added mandatory preliminary findings checkpoint between Phase 2 and 3
- Made both phases internally iterative (not rigid one-shot)
- Issue tree now has two exposure levels (internal vs. user-facing)
- Always produce BOTH slides and .md document when user requests slides
- Contextual file naming (e.g., `Market_Entry_Strategy_EU_Paint_v1.md`)

### Update 10 (2026-03-02)
- Removed `--depth` parameter (consolidated into `--length`)
- Clarified: longer length = more content covered, not more detail on same scope

See [CHANGES.md](CHANGES.md) for complete version history.

## Contributing

This skill is actively developed based on real consulting practice. Contributions welcome!

## License

MIT License - see LICENSE file for details

## Credits

Developed based on BCG consulting methodology and real-world strategy engagement patterns.
