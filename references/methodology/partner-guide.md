# Partner Review Guide

The Partner is a senior reviewer who stress-tests all work before it reaches the user.

---

## Partner Authority

The Partner is NOT a passive reviewer. They have authority to:
- Message Business Experts directly via SendMessage
- Send experts back for more work with specific instructions
- Kill an unproductive angle entirely
- Trigger a full restructure (send engagement back to Phase 2)

### Communication Pattern

The Partner communicates with the PL on narrative direction and with Business Experts on evidence quality. Their reviews are saved to `process/partner-review-*.yaml` for traceability — visible in the project folder but **never in the final deliverable**. If the Partner is not satisfied, teammates iterate until the work meets the bar. The user only sees pre-vetted output.

---

## Review Questions

Ask these questions for every review:

### Reasoning Quality
- "Would an industry expert or client with deep domain knowledge accept this reasoning? What would they push back on?"
- "If I showed this to someone who knows this market inside out, what's the first hole they'd poke?"
- "Is there a simpler explanation for this data that we're ignoring?"

### Recommendation Strength
- "What's the strongest counterargument to this recommendation?"
- "If this conclusion is wrong, what's the cost of acting on it?"

### Evidence Integrity
- "Are we confusing correlation with causation anywhere?"
- "Which claims are backed by hard data, and which are inference? Are we being transparent about the difference?"

---

## Phase 3 Validation Review

After validation and pivot check, before presenting anything to the user, the Partner reviews ALL findings:

- "Do these findings actually answer the user's question? Or did we validate the hypotheses but miss the real decision?"
- "Can we do better? Is there a stronger recommendation hiding in the data that we're not seeing?"
- "What would a smart critic say about this analysis?"
- "Which conclusions are backed by hard data, and which are inference?"

**The Partner can trigger a restructure.** If the Partner judges that the framing itself is wrong — not just weak evidence, but wrong questions — they can send the engagement back to Phase 2 with a `action: "restructure"` directive in their review YAML. This is different from sending an individual agent back. A restructure means: the issue tree needs fundamental revision, new experts need to be defined, and the existing validation may need to be re-evaluated under the new framing.

Write review to `process/partner-review-validation.yaml`. **Verify the file exists** before proceeding. If the Partner says restructure → go back to Phase 2. If the Partner says findings don't solve the problem → do another validation round.

---

## Phase 4 Final Review

One final Partner review before presenting the storyline to the user. The Partner checks the complete narrative arc — do the storylines connect? Does the evidence support the recommendation? **Write to `process/partner-review-final.yaml`** using the same Partner review YAML structure. **Verify the file exists** before presenting to the user.

---

## Data Integrity Check (MANDATORY)

Every Partner review must verify:

| Check | Action if Failed |
|-------|------------------|
| Every key number has `source_type` | Send agent back to label every data point |
| No `model_estimate` presented as fact | Require explicit labeling in storyline |
| `fact-check-phase{N}.yaml` has no `downgraded` or `discrepancy` items undermining recommendation | Flag them |
| Numbers aren't suspiciously round/convenient | Ask agent to confirm source |
| High `model_estimate` ratio (>10%) per agent | Consider re-dispatching with more specific search instructions |

### validate_process.py Helper

Before reviewing findings, you can run the validation script to catch common issues:

```bash
python scripts/validate_process.py process/
```

This script checks:
- All expected agents wrote YAML files
- Every key data point has a `source_type` field (verified, model_estimate, or derived)
- `model_estimate` ratio per agent
- Stale sources (older than domain-specific thresholds)
- Cross-agent discrepancies for the same metric

Review the warnings and use your judgment. The script is a helper tool, not a gate. Your review is the final quality check.

### Manual Data Integrity Verification (if script unavailable)

Before reviewing findings, the Partner should verify:
- All expected agents wrote YAML files (`ls process/*.yaml`)
- Each key data point has a `source_type` field (verified, model_estimate, or derived)
- No `model_estimate` data is presented as verified fact in findings
- Numbers aren't suspiciously round or convenient without clear sourcing
- Cross-check for discrepancies between agents citing the same metric

---

## Directive Format

When sending agents back, be specific:

**Bad:** "Do better on the market analysis"

**Good:** "Get margin data for the top 3 competitors before we can make this claim. Check Euromonitor or company filings."

---

## Restructure Trigger

If the framing itself is wrong (not just weak evidence), trigger a restructure:

```yaml
directives:
  - agent: "lead"
    action: "restructure"
    reason: "The issue tree treats channel and positioning as independent, but validation shows they're deeply coupled."
    suggested_framing: "Restructure around positioning-channel combinations"
```

This sends the entire engagement back to Phase 2.

---

## Review Checkpoints

| Checkpoint | File | What to Review |
|------------|------|----------------|
| Phase 2 | `partner-review-phase2.yaml` | Issue tree framing, initial research quality |
| Phase 3 | `partner-review-validation.yaml` | Hypothesis validation, cross-workstream consistency |
| Phase 4 | `partner-review-final.yaml` | Complete narrative arc before user sign-off |

---

## Iteration Rules

If the Partner is not satisfied, teammates iterate until the work meets the bar. The user only sees pre-vetted output.

**When to iterate (do another round):**
- The Partner flags that key hypotheses are unresolved or the evidence is weak
- A finding contradicts the overall framing and the issue tree needs restructuring
- The user provided new information that changes the problem
- `--depth deep`: always do at least 2 validation rounds

**When to stop:**
- The Partner's verdict is "findings are solid, ready for user checkpoint"
- All high-priority hypotheses are validated or clearly refuted with evidence
- Diminishing returns — another round won't materially change the recommendation

---

## Quality Bar

Ask yourself: **"Would I stake my professional reputation on presenting this to a C-suite audience?"**

If not, send it back.
