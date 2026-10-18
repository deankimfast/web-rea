# web-rea

A reusable skill for measuring how much of an authorized web app's behavior can be reconstructed through HTTP alone.

**Use only on systems you own or are explicitly authorized to test.** The output is an owner-facing coverage and gap report. Stateful tests use a disposable local instance with fictional accounts and isolated providers.

## The method

1. An orchestrator prepares the authorized fixture and keeps private setup/source information away from the blind reviewer.
2. A fresh blind reviewer uses curl, public assets and approved test identities to infer rules, recording requests, observations, confidence and unknowns.
3. A source-aware scorer compares that report with one frozen, independently checked rule inventory and returns counts only: correct, partly right, wrong and missed.
4. The next fresh reviewer receives numeric feedback. Stop at a predeclared coverage plateau or round cap, rather than chasing one high score.

The originating five-round exercise plateaued around 50–60% after round three. Later gains depended heavily on hints leaking answers. The skill treats 50–65% as a practical planning expectation from that experience, not a general benchmark. Login lockout and spam auto-block were especially difficult; email-dependent rules required a local SMTP sink.

## Use with Claude Code or ChatGPT

Start with [SKILL.md](SKILL.md). The same Markdown instructions and relative references support either host. Load this folder through your host's supported skill mechanism, or provide the instructions and referenced files to the conversations performing the roles.

The host or human operator must provide an authorized curl runner, report writing, source access for scoring, and isolated contexts. In a chat-only setup, use the manual handoffs in [runtime separation](references/runtime-separation.md): a fresh blind conversation, a separate source-aware scoring conversation, and an orchestrator exchanging sanitized numeric results. Do not put the source into the blind conversation. A skill file cannot enforce tool or filesystem restrictions.

An example starting request:

> Use blackbox-web-recon to assess my own app through a disposable local instance. Establish scope and budgets, freeze and independently check the scoring inventory, and run fresh blind rounds until coverage plateaus or five rounds finish.

Loading the skill is not permission to start testing. Confirm the target and proposed actions against the owner's existing authorization first.

## Contents

```text
blackbox-web-recon/
├── LICENSE
├── README.md
├── SKILL.md
├── .gitignore
├── agents/
│   └── openai.yaml
├── references/
│   ├── local-setup.md
│   ├── pitfalls.md
│   ├── role-prompts.md
│   ├── rule-inventory.md
│   └── runtime-separation.md
└── scripts/
    └── calculate_coverage.py
```

The references cover disposable databases and SMTP capture, blind isolation, stable rule inventories, scorer cross-checks, feedback contamination and role prompts. `agents/openai.yaml` is optional UI metadata for hosts that understand it.

## Offline coverage calculator

The helper uses Python 3.8+ and the standard library only. Save aggregate counts in the format documented in [rule-inventory.md](references/rule-inventory.md), then run:

```sh
python3 scripts/calculate_coverage.py /path/to/scores.json
```

It prints per-round/per-area Markdown tables and rejects inconsistent counts or inventory versions. Each fixed rule has exactly one classification:

```text
N = correct + partly_right + wrong + missed
coverage = (correct + partly_right) / N
fully_correct = correct / N
```

Wrong rules remain in the denominator and are not also counted as missed. The calculator validates arithmetic, not the scorer's assumptions. It sends no network requests.

## Contributing and publishing

Keep contributions generic and reproducible. Document changes to rule granularity, scoring or feedback policy, since these affect comparisons across rounds. Use synthetic offline examples to check the calculator and inspect relative links after editing the skill.

This repository contains only reusable instructions and helper code. Keep target-specific source, private inventories, reports, captured assets, credentials and mailbox contents outside it. The ignore file reduces accidental additions; review the tracked file list and every change before publishing.

Licensed under the [MIT License](LICENSE).
