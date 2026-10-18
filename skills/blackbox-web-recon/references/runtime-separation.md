# Claude Code and ChatGPT runtime separation

The shared artifact is `SKILL.md` plus its relative references and offline script. `agents/openai.yaml` is optional UI metadata for hosts that understand it; other hosts can ignore it. Do not assume that loading a skill creates a sandbox or grants any tool permission.

## Claude Code or another local coding-agent host

Use the host's skill-loading mechanism to load this folder. Before spawning reviewers, check whether a fresh worker inherits the current conversation, repo working directory, automatic project instructions, memories, attachments, plugins or filesystem permissions. Launch the blind worker in its dedicated round directory with source and archive mounts absent. Restrict execution to the approved curl request surface and report writing; restrict file reads to the provided credentials/scope and test mailbox where authorized.

“Bash (curl only)” means the effective policy permits only approved curl invocations. General Bash access permits commands, substitution and file reads beyond curl; simply asking an agent not to use them is procedural separation. Curl itself can read/upload files or use non-HTTP schemes, redirects and proxies: constrain destinations, schemes and accessible files as well. Set these controls in the host/sandbox, not by relying on tool names in a prompt. Request artifacts should exclude authorization headers/cookies and redact token-bearing bodies.

The scorer uses a different context with the owner's source and private inventory, and writes aggregates to a controlled exchange location. Never attach private inventory files to the blind conversation. The orchestrator reviews outbound feedback for forbidden detail before starting another fresh reviewer.

## ChatGPT environments

Provide this folder as files or use the host's supported skill mechanism. Verify that the session actually has an authorized HTTP runner, report-file output and separately scoped agent contexts. A generic web-browsing tool is not equivalent to curl: it may not reach loopback, preserve cookies, expose headers or submit the required methods. Do not claim to have performed HTTP tests when those capabilities are absent.

If isolated agents are unavailable, use human-mediated handoffs: one fresh blind conversation with only scope/credentials and sanitized HTTP results from the owner's local runner; a separate source-aware conversation for inventory/scoring; an orchestrator conversation receiving only numeric feedback. Label this a manually mediated variant. Never place both source and blind work into one conversation and ask it to “forget” source details. Do not copy real secrets into chat to compensate for missing tools; the owner keeps fixture secrets in the local runner and shares redacted evidence.

If neither isolated workers nor manual separation is practical, produce the setup/report templates and explain the missing capability. Do not assign a black-box score or pretend the three roles were independently executed.

## Publishing the skill

Publish only generic instructions, references and helper code. Exclude audit reports, inventories, target URLs, credentials, source excerpts, captured customer data, private emails and machine-specific paths. This package is distributed under the [MIT License](../LICENSE); preserve its copyright and permission notice when redistributing. Inspect the final tracked files before public distribution. No publication or remote repository creation is implied by writing the skill locally.
