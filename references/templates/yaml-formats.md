# YAML Templates for Process Files

All agents must write structured YAML files to `process/`. Use these exact formats.

---

## Workstream Findings (Business Experts)

File: `process/<workstream-name>.yaml`

```yaml
workstream: "<name of this workstream>"
agent: "<agent identifier>"
problem_scope: "<the question this agent is answering>"
timestamp: "<ISO 8601>"
status: "complete"
key_findings:
  - finding: "<one-sentence conclusion>"
    confidence: high|medium|low
    source: "<where this came from>"
    implications: "<what this means for the client's specific decision>"
    data_points:
      - metric: "<what was measured>"
        value: "<number or range>"
        year: <year>
        source_type: verified|model_estimate|derived
        source_url: "<url if verified, empty if model_estimate>"
data_gaps:
  - "<what we couldn't find>"
sources:
  - name: "<source name>"
    type: "<source type>"
    url: "<url if available>"
```

### Implications Field (MANDATORY)

Every agent must include an `implications` field in their key findings — what does this finding mean for the client's specific decision? This forces the thinking to happen during research, not just during synthesis.

```yaml
key_findings:
  - finding: "EU decorative paint market is €12B, growing 3.2% CAGR"
    confidence: high
    source: "Euromonitor 2025"
    implications: "Market is large enough to support a niche entrant — even 0.1% share = €12M revenue"
```

### `source_type` Rules (MANDATORY)

- `verified` — number comes from a specific, citable source. MUST have `source_url`.
- `model_estimate` — from model knowledge, not verified. Must be explicitly labeled. Treated as hypothesis, not evidence.
- `derived` — calculated from other data points. Show the formula.

**Data sourcing workflow:**
1. Search for the number using web/MCP/API
2. If found → cite as `verified` with URL
3. If not found after genuine search → label `model_estimate` and note in `data_gaps`

**Quality gate:** Agent with >10% `model_estimate` ratio has not done enough research. Re-dispatch with more specific search instructions.

### Case Study Standards in YAML

A one-line mention ("Clare raised $7.5M") is NOT a case study. For each comparable, collect at minimum:

**Case study depth:** For the 1-2 most relevant case studies, collect all 4 dimensions below. For supporting comparables, a brief mention with source is acceptable.

```yaml
case_studies:
  - company: "Clare Paint"
    strategy: "DTC-only eco paint via Shopify + Instagram"
    outcomes:
      - metric: "Revenue"
        value: "$7.5M Series A (2020)"
        source_type: verified
        source_url: "https://..."
      - metric: "Market position"
        value: "Top 5 DTC paint brand in US"
        source_type: model_estimate
    what_worked: "Strong brand identity, Instagram-first marketing, simplified SKU count"
    what_didnt: "Struggled with B2B/contractor channel, high CAC"
    lesson_for_client: "DTC paint can work but requires strong brand investment; contractor channel is a separate problem"
```

Each case study must have all 4 dimensions:
1. What they did (strategy/approach)
2. Key outcomes (quantitative metrics where available, qualitative results where not — both are valid)
3. What worked and what didn't
4. The specific lesson for this client's situation

---

## Issue Tree

File: `process/issue-tree.yaml`

```yaml
core_question: "Should we launch B2C paint in EU/US?"
version: 1
last_updated: "<ISO 8601>"
branches:
  - id: "market-viability"
    label: "Market viability"
    hypotheses:
      - id: H1
        statement: "Decorative segment growing >3% CAGR"
        status: pending|supported|refuted|revised
        evidence_summary: ""
      - id: H2
        statement: "Specialty niches have room for new entrants"
        status: pending
        evidence_summary: ""
  - id: "cost-advantage"
    label: "Cost advantage survivability"
    hypotheses:
      - id: H3
        statement: "Margins positive after tariffs + shipping"
        status: pending
        evidence_summary: ""
changelog:
  - version: 1
    timestamp: "<ISO 8601>"
    change: "Initial tree created from Phase 2 research"
```

**Living document:** When validation adds, removes, or restructures branches:
1. Increment version
2. Update hypothesis statuses
3. Log the change in changelog
4. User sees current tree at each checkpoint, not the original

---

## Partner Review

File: `process/partner-review-<checkpoint>.yaml`

```yaml
reviewer: "Partner"
checkpoint: "phase2" | "validation" | "final"
timestamp: "<ISO 8601>"
status: "approved" | "needs-revision"
assessment:
  storyline_coherence: "<are the hypotheses well-framed?>"
  evidence_gaps:
    - "<what's missing>"
  logic_issues:
    - "<what doesn't hold up>"
  skeptic_challenges:
    - "<what would a critic say>"
directives:
  - agent: "<which agent>"
    action: "<specific instruction>"
overall_verdict: "Ready for user checkpoint" | "Needs more work on [X]"
```

### Partner Restructure Directive

When the framing itself is wrong (not just weak evidence):

```yaml
directives:
  - agent: "lead"
    action: "restructure"
    reason: "The issue tree treats channel and positioning as independent, but validation shows they're deeply coupled — DTC pricing forces premium positioning, Amazon pricing enables value positioning."
    suggested_framing: "Restructure around positioning-channel combinations"
```

This sends the engagement back to Phase 2 for fundamental revision.

---

## Fact-Check Results

File: `process/fact-check-phase{N}.yaml`

```yaml
fact_check:
  phase: 2|3
  timestamp: "<ISO 8601>"
  checked_data_points: 8
  results:
    - metric: "EU decorative paint market size"
      claimed_value: "€12B"
      claimed_source: "Euromonitor 2025"
      source_url: "https://..."
      verification: verified|downgraded|upgraded|discrepancy
      actual_value: "€11.8B"
      notes: "Close enough — rounding difference"
    - metric: "Specialty segment CAGR"
      claimed_value: "6.2%"
      claimed_source: "model knowledge"
      source_url: ""
      verification: "upgraded"
      actual_value: "5.8%"
      notes: "Found in Grand View Research 2025 report"
  summary:
    verified_count: 5
    downgraded_count: 1
    upgraded_count: 1
    discrepancy_count: 1
    risk_flags:
      - "Shipping cost estimate ($8.50/unit) is model_estimate and critical to margin calculation"
```

---

## Engagement State (Resumability)

File: `process/engagement-state.yaml`

```yaml
engagement:
  topic: "<user's original question>"
  project_folder: "<path>"
  created: "<ISO 8601>"
  last_updated: "<ISO 8601>"

current_phase: 3
phase_status:
  phase_0: complete
  phase_1: complete
  phase_2: complete
  phase_3: in_progress
  phase_4: pending
  phase_5: pending
  phase_6: pending

parameters:
  format: slides
  length: 10min
  level: analyst
  depth: standard
  sources: balanced
  lang: en

hypotheses:
  supported:
    - H1: "Market growing >3% CAGR"
    - H3: "Margins positive after tariffs"
  refuted:
    - H6: "Retail partnership viable under $500K"
  pending:
    - H2: "Specialty niches accessible"

data_gaps:
  - "Partner B financials — private company"
  - "Real freight quotes for Vietnam→UK route"

loop_back_count: 1
loop_back_history:
  - from_phase: 3
    to_phase: 2
    reason: "Positioning analysis revealed channel-positioning coupling"
    timestamp: "<ISO 8601>"
```

---

## Next Steps Proposal

File: `process/next-steps-proposal.yaml`

```yaml
next_steps:
  category_a_researchable:
    - action: "Get real container rates from Freightos"
      url: "https://fbx.freightos.com"
      route: "Vietnam→UK"
      priority: high
    - action: "Pull Amazon UK PPC benchmarks"
      tool: "Jungle Scout or Helium 10"
      keywords: "eco paint"
      priority: medium

  category_b_human_action:
    - action: "Interview 3 potential retail partners"
      materials_generated: "next-steps/interview-guide-retail-partners.md"
      priority: high
    - action: "Customer survey on eco-paint preferences"
      materials_generated: "next-steps/survey-eco-preferences.md"
      priority: medium
```
