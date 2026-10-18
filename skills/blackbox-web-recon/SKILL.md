---
name: blackbox-web-recon
description: Measure what a patient outsider could infer about an owned or explicitly authorized web app through HTTP alone, using fresh blind reviewers, a source-aware scorer, a fixed rule inventory, and repeated rounds with counts-only feedback. Use for authorized self-audits of observable backend behavior and coverage gaps; never for unauthorized third-party reconnaissance or exploit development.
---

# Black-box web recon

**Only ever target a system the user owns or is explicitly authorized to test. Refuse to adapt this skill to target an unauthorized third-party site.** Authorization must cover the target, test environment and proposed actions; access to a website or its source is not authorization. This is an owner-facing coverage and gap assessment, never an exploit or attack guide.

## When to use it

Use when a developer asks what a patient outside attacker could learn about their deployed web app through HTTP alone: public pages, served JavaScript, published source maps, visitor login flow, and observable backend rules. Authenticated test-account observations are a separate capability tier from anonymous access; label them accordingly.

Prefer a disposable local instance matching the deployment configuration. Stateful checks of login lockouts, rate limits, MFA, tokens and spam controls belong there, using fictional accounts. Local findings are evidence about that fixture, not proof of production behavior. A deployed-target pass defaults to explicitly scoped read-only observation; it does not authorize lockout testing, real-user actions, provider calls or billing changes. This skill does not deploy anything.

In the originating five-round exercise, coverage plateaued around 50–60% after round three. **About 50–65% coverage of HTTP-visible backend rules is a reasonable planning ceiling, not a failure of the method.** This is an experience-based expectation, not a validated universal benchmark or target to force. Extra hints can increase scores without improving blind inference. Recovering a route or schema is not recovering its rules; partial coverage is not complete understanding.

Login lockout and spam auto-block were the hardest areas to infer in that exercise. Email-dependent rules needed a local SMTP sink; absent email capture was a reachability limit, not evidence that those rules did not exist.

## Establish the experiment

Use existing explicit authorization; ask only for missing scope. Record the permitted origin(s), environment, identities/roles, allowed state changes, request and failed-authentication budgets, timing budget, round cap and cleanup obligations. Never follow redirects or callbacks out of scope. No password guessing, credential stuffing, fuzzing, exploit chaining or attempts against real accounts.

Read [runtime separation](references/runtime-separation.md) before selecting tools. Read [local setup](references/local-setup.md) for a throwaway instance. Do not claim enforced isolation when the runtime only supports instructions and separate conversations.

Three roles:

- **Orchestrator:** owns scope, local setup, round scheduling, evidence custody and cleanup. May read source only for setup, but never forwards source-derived clues to the blind reviewer.
- **Blind reviewer:** a fresh agent/context each round. HTTP requests through `curl` only, narrowly allowed fixture reads, and report writing; no source, database, logs, prior reports, scorer files or inherited repo context.
- **Scorer:** source access plus the frozen inventory and current report. Maintains private rule-to-evidence judgments. Returns only numeric classifications per predeclared area and totals, never corrections, examples, source paths, code, rule descriptions or mechanisms.

## The loop

1. **Freeze the baseline before probing.** One source-aware scorer builds a single versioned inventory of HTTP-visible backend rules. Independently check its assumptions, especially middleware, proxy/header trust and effective configuration, before freezing it. Read [rule inventory and scoring](references/rule-inventory.md). Do not derive a new denominator each round.
2. **Prepare a comparable fixture.** Use the same declared capabilities and reset state each round, including cooldown stores, SMTP capture and sessions. Keep fixture identity, application revision and configuration recorded privately. If capabilities change, mark a new series or re-score all archived rounds against the same revised baseline.
3. **Run a fresh blind reviewer.** Supply only the approved scope/budgets, base URL, dedicated credentials file, stable high-level areas and reporting instructions. From round two, add only sanitized numeric feedback. It may choose a different approach using public observations or generic methodology; do not pass source-informed approaches. Read [role prompts](references/role-prompts.md).
4. **Require evidence, not confident guesses.** Each numbered claim must state one inferred rule, sanitized request/response evidence IDs, relevant state/timing, confidence and remaining alternatives. Distinguish observed, inferred and unknown. End the Markdown report with what could not be inferred, budget constraints and untested capabilities. Never put passwords, session cookies, API secrets, live tokens or real customer data in reports.
5. **Score the current report alone.** The scorer maps claims to the fixed inventory, applying the same rubric every round. Do not silently combine earlier reports into a cumulative score. Reject narrative feedback before it reaches the next reviewer. Preserve private evidence mappings for audit and re-scoring.
6. **Evaluate stopping.** Predeclare a round cap (default five) and plateau criterion (default: less than two percentage points of coverage gain in each of two consecutive comparable transitions, with no increase in fully correct rules). Stop at either condition; also stop on scope uncertainty, exhausted safety budgets or unexpected external effects. A single high score is not a stopping proof. Pause comparison if the inventory or fixture is invalid; repair and re-score consistently. Do not add hints to escape a plateau.
7. **Report and clean up.** Show per-round and per-area correct/partly right/wrong/missed counts, denominator, coverage, fully correct percentage, fixture scope, evidence links and stop reason. Separate anonymous and authenticated visibility, independent reconstruction and assisted runs, and missing coverage from security defects. State gaps the owner can investigate without publishing exploitation steps. Stop only test processes you started; delete disposable state, credentials and captured mail; preserve sanitized reports and restore archive permissions. Never delete the application's actual data or unrelated work.

## Coverage and interpretation

Each inventory rule has exactly one label per round: correct (`C`), partly right (`P`), wrong (`W`) or missed (`M`). Thus `N = C + P + W + M`, coverage is `(C + P) / N`, and fully correct coverage is `C / N`. Wrong rules stay in the denominator; they are not also counted as missed. Extra false claims outside the inventory are reported separately and do not change `N`. See the worked example and offline calculator format in [rule inventory](references/rule-inventory.md).

Use `python3 scripts/calculate_coverage.py scores.json` to validate counts and print comparable tables. This helper performs no network requests. It checks arithmetic and version consistency, not scorer correctness.

Read [known pitfalls](references/pitfalls.md) before interpreting gains or publishing results. Explicitly flag any source-derived hint contamination. A reproducible server rule may be normal product behavior; a low reconstruction score is not a security assurance, and a high one is not evidence of an exploit.

## Boundaries and portable use

The deliverable is a coverage/gap report for the authorized owner to improve their system. Do not turn findings into an attack playbook, publish reusable credentials or payload chains, expand targets, or infer permission to clone, deploy or exploit the app. Authorization for a local test does not authorize production or provider actions.

The Markdown workflow is shared between Claude Code and ChatGPT-capable environments. Tool permissions, isolated subagents and source access must be supplied by the host or a human operator; a skill file cannot grant or enforce them. Where those capabilities are absent, use the manual handoffs in [runtime separation](references/runtime-separation.md), or produce a setup plan and state that no experiment was run. Never simulate a blind agent, invent HTTP evidence or manufacture a score.
