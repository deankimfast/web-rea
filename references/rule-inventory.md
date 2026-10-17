# Fixed inventory, defensible scoring

## Build and verify once

One source-aware scorer inventories distinct HTTP-visible backend rules before round one. Use stable IDs, predeclared broad areas and one meaningful assertion per unit. Keep the complete inventory private. Each unit records:

- ID, area, behavioral assertion and prerequisites/capability tier.
- Source evidence and effective configuration relevant to the assertion.
- A possible distinguishing HTTP observation, including state and timing.
- Whether it is reachable in this fixture; email/provider dependencies.
- What qualifies as correct or partial, and what would falsify it.

Do not equate one route, schema field or code branch with one rule. Merge duplicate statements of the same externally observable behavior; separate genuinely distinct triggers, windows, clear conditions and permission boundaries. Exclude internal-only implementation details. Put provider-dependent or configuration-unreachable rules in a declared excluded set or separately scored cohort. Do not shrink the denominator because a reviewer ran out of time.

An independent source-aware reviewer or owner must cross-check high-impact assumptions using code paths, deployed/local server configuration and authorized controlled HTTP checks. In particular, establish which component reads client-address headers, whether a proxy sanitizes them, what the server trusts, and whether an earlier middleware layer terminates a request. Seeing no header reference in a route is not evidence that the header is ignored. Checks that require state changes still need the agreed local test scope. Keep this verification evidence away from blind reviewers.

Freeze inventory version/digest, ordered rule IDs, area membership, scoring rubric, app revision, fixture configuration and cohort eligibility. Future scorers reuse this exact list. If an assumption is corrected, version the inventory and re-score every retained round under the corrected rubric; publish old scores as superseded. Never silently mix pre-fix and post-fix numbers. If re-scoring cannot be justified from saved evidence, mark that series non-comparable.

## Classification and math

Classify **rules**, not sentences or endpoint counts:

| Label | Meaning |
|---|---|
| Correct (C) | The rule's distinguishing behavior is accurately stated and supported by adequate recorded observations. |
| Partly right (P) | Some defining behavior is supported, but material conditions/boundaries are missing or inaccurate. |
| Wrong (W) | A claim maps to this rule but its central assertion conflicts with verified behavior. |
| Missed (M) | No substantive claim about this rule, or only an explicit unknown/unsupported guess. |

Use the fixed rubric to resolve multiple or contradictory claims; don't award separate credit for duplicate wording. A claimed observation without request evidence cannot receive full credit. Keep a private mapping from every inventory ID to the report claims/evidence and judgment so a reviewer can reproduce the aggregate. Extra false claims that match no inventory rule are counted separately as `unmapped_wrong_claims`; they never inflate the denominator or hide known-rule errors.

`N = C + P + W + M`. Report both discovery coverage `(C + P) / N` and fully correct coverage `C / N`. Do not treat partial as fully known, count wrong twice as missed, or omit wrong from the denominator.

Example: C=9, P=7, W=2, M=12 gives N=30, discovery coverage **53.3%** and fully correct coverage **30.0%**. Using 16/28 would incorrectly remove the two wrong rules. In a legacy score where “wrong” counts claims and “missed” counts all uncovered inventory rules, the old formula may mean something different: reconstruct the per-rule mapping before comparing, rather than adding incompatible counts.

Score the current round report alone by default. A cumulative union is an optional separately labeled metric requiring per-rule adjudication; it is not an independent blind round and cannot be produced by adding round counts. Specify request/time budgets and capability tiers alongside coverage. Report `N=0` as not applicable, never 100%.

## Counts-only output and offline helper

The scorer emits only round/version identifiers, predeclared area labels and numeric counts. No correctness explanations, wrong-claim quotations, source paths, rule IDs/descriptions, thresholds, endpoints, values or “vague” mechanism hints go to the blind reviewer. The orchestrator may withhold per-area feedback for a stricter experiment; even counts guide effort allocation, so log the feedback policy and keep it stable.

The calculator accepts the following aggregate file. Area denominators come from the frozen inventory. The inventory and round identifiers are metadata, not blind hints.

```json
{
  "inventory_version": "v1",
  "scope": "local-http-with-email",
  "areas": {"identity": 30},
  "rounds": [
    {
      "round": 1,
      "inventory_version": "v1",
      "areas": {
        "identity": {"correct": 9, "partly_right": 7, "wrong": 2, "missed": 12}
      },
      "unmapped_wrong_claims": 0
    }
  ]
}
```

Run `python3 scripts/calculate_coverage.py scores.json` from the skill directory. It reads only the supplied JSON and writes Markdown to stdout, rejecting negative counts, changed denominators, missing areas or mixed inventory versions. Use separate files for full/email-free cohorts or different capability scopes; retain the private rule memberships to show those subsets are stable. No arithmetic helper can detect a plausible but incorrect scorer assumption.
