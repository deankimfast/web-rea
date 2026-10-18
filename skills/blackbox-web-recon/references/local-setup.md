# Disposable local setup

Use this pattern only after the target and stateful-test scope are authorized. Adapt configuration names to the owner's app; do not invent settings or modify application logic just to make a probe succeed.

## Fixture contract

Record application revision, dependency/runtime versions, database engine, middleware/proxy topology, effective feature flags, clock/timezone, worker mode and seeded capability tiers. A SQLite substitute, disabled callback signature check or missing background worker can change behavior; list each departure from the deployed configuration. Keep source-derived configuration details private to setup/scoring unless they are an explicitly declared experimental capability.

Start on loopback using a fresh temporary working root, dedicated DB and dedicated caches/queues. Ensure no process reads ambient production `.env` files, credentials, cloud identity, shared Redis or customer data. Use an explicit environment allowlist. Block provider egress; missing credentials alone do not prove external effects are impossible. Prefer existing local/test configuration and provider adapters. If required isolation is unavailable, stop the dependent tests and report the limitation.

A useful layout outside the original repo:

```text
experiment/
  setup-private/       # launch settings, process IDs and disposable data
  scoring-private/     # frozen inventory, source evidence and judgments
  archive-private/     # sanitized completed reports
  blind/round-01/      # only this round's scope, creds and output
```

Do not mount private directories or the original source into the blind runtime. Use a fresh non-root container/user sandbox with access only to the permitted origin and round directory where possible. Verify isolation with a harmless sentinel, not by inviting the blind agent to read source. `cwd`, instructions, and `chmod 000` under the same owning UID are procedural controls, not a security boundary: that UID can often restore permissions. If enforced isolation is unavailable, disclose procedural separation and use fresh contexts without repo auto-loading. Never claim “curl only” if a general shell can read arbitrary files or run other programs.

## Seed capabilities without disclosing rules

Create fictional owner, staff and platform administrator identities as needed. Keep administrative/account access in a separate tier from what an outsider could register or see anonymously. Seed independent tenants, distinct roles, valid MFA enrollment, and disposable accounts for different failure-state tests. Expose only credentials and capability labels, not source-derived thresholds or answers.

Add a fictional inbound phone identifier and active subscription/trial only when needed to reach the authorized area. A tenant near a seat limit can make a boundary test feasible, but explicitly telling the reviewer the exact remaining seats leaks the answer. Label fixtures supplied for reachability as assisted capability assumptions; their seeded values alone do not establish a rule.

For MFA, provide a supported test-only proof mechanism or operator-supplied current codes within the declared scope. Do not quietly allow Python, shell substitutions or a TOTP helper when the reviewer was promised curl-only. Record any deliberate capability exception as a different protocol.

## Local email capture

Invitation and password-reset workflows often require email. Prefer an existing file-capture transport; otherwise run a loopback SMTP sink with no outbound relay, then point only the local app to it. Disable TLS/auth requirements only for that isolated sink. Confirm setup with a fictional message and verify that no external delivery occurred. Never reuse production email credentials.

Give the reviewer narrowly scoped read access to its test messages or a loopback read-only mailbox endpoint. Capture bodies, timestamps and delivery failures; redact tokens from report evidence. Mailbox access is an explicit additional capability, not something every outside attacker has. Run and report an email-enabled cohort separately from rules reachable without email; freeze both subsets up front. If email capture fails, mark affected rules unavailable for testing, not disproven.

## Round reset and cleanup

Archive sanitized evidence before deleting only the previous round's dedicated blind directory. Never expose older findings, scorer feedback files beyond the approved counts, or setup scripts to a new reviewer. Reset database plus rate-limit caches, queues, cookies, tokens, mailbox and process-local counters consistently. Reusing a DB with a fresh server or vice versa can silently change test state.

Use separate fictional accounts for independent stateful tests; this prevents cross-test contamination, not evasion of a limit. Keep a ledger of attempts, responses and elapsed times. Request a narrowly scoped budget change before exceeding an authorized cap; otherwise report an unknown. Do not accelerate clocks or edit backend state during blind tests and then call the result natural HTTP inference.

At the end, identify test processes by recorded PID and command before stopping them. Delete only named disposable databases/volumes, sink contents, credentials, cookie files and setup artifacts. Restore any archive permissions changed for the run. Preserve sanitized reports, score versions and limitations; verify the test listeners stopped. Never apply cleanup commands to shared directories or application data.
