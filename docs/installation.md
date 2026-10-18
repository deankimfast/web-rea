# Install the standalone skill or plugin

All variants contain the same skill instructions. They provide workflow guidance and an offline calculator; the host supplies curl, report writing, source-aware scoring and isolated reviewer contexts. Installing does not start a test or grant target access. No MCP server, hooks, credentials or automatic probing are included.

## Claude Code plugin

Register this GitHub repository as a marketplace, then install its plugin:

```sh
claude plugin marketplace add deankimfast/web-rea
claude plugin install blackbox-web-recon@web-rea
```

In a new Claude Code session, invoke:

```text
/blackbox-web-recon:blackbox-web-recon
```

For local development, use `claude --plugin-dir /path/to/web-rea`. Validate the manifest/catalog with `claude plugin validate /path/to/web-rea`. Loading the plugin does not enforce blind-agent filesystem isolation; follow the skill's runtime-separation guidance.

Format and installation references: [Claude plugin manifest](https://code.claude.com/docs/en/plugins-reference), [marketplace installation](https://code.claude.com/docs/en/plugin-marketplaces).

## ChatGPT / Codex plugin

The root `plugin.json` is an Agent Plugins manifest with OpenAI presentation metadata. Its skill is under `skills/blackbox-web-recon/`. The `.agents/plugins/marketplace.json` catalog exposes the repository root as a local plugin.

For a supported ChatGPT desktop local environment, clone this repository, open it as a project, then restart the app to refresh local marketplace discovery. Select the `web-rea` source in the Plugins Directory and install Black-box Web Recon. Availability depends on the client and workspace policies. This local catalog does not make the plugin appear in the universal public directory.

For ZIP distribution, run the offline builder below and use `dist/blackbox-web-recon-openai.zip`. It has `plugin.json` at the archive root. Public directory distribution requires uploading the package to OpenAI's plugin submission portal, completing its checks/review and publishing an approved version. This repository is packaged for that workflow; it has not been submitted, approved or listed. No account/client installation was performed by the package build.

The repo catalog and package do not supply localhost connectivity, a curl runner, source access or isolated workers to a chat-only environment. Use the manual handoff procedure in the skill when those capabilities are absent; do not claim an automated audit ran.

Official references: [OpenAI plugin packaging and local marketplaces](https://developers.openai.com/plugins/build/plugins), [submission and publication](https://developers.openai.com/plugins/deploy/submission).

## Standalone skill

The root `SKILL.md`, `agents/`, `references/` and `scripts/calculate_coverage.py` remain the canonical standalone skill. Use the skill-loading location supported by your host. For Claude Code project discovery, the extracted skill folder belongs at `.claude/skills/blackbox-web-recon/` in the project where you want it available; take care not to start a blind reviewer inside a source-aware project context.

Alternatively build the skill ZIP and extract its `blackbox-web-recon/` directory into your host's skill directory. A host without native skill loading can use `SKILL.md` and the relative references as manual role instructions. Do not install both standalone and plugin copies unless you intend to expose duplicate workflows.

## Build packages offline

From the repository root, using Python 3.9+:

```sh
python3 scripts/build_packages.py
python3 scripts/build_packages.py --check
```

Outputs:

| File | Contents |
|---|---|
| `dist/blackbox-web-recon-skill.zip` | Standalone skill folder, license and documentation |
| `dist/blackbox-web-recon-claude-code.zip` | Claude manifest and bundled skill |
| `dist/blackbox-web-recon-openai.zip` | Portable/OpenAI manifest and bundled skill |

The builder copies only the nine named canonical skill/license files into `skills/blackbox-web-recon/`, checks manifest/catalog identities, and creates ZIPs from explicit file lists. It excludes Git metadata, local state and arbitrary working-directory files. Generated ZIPs are ignored by Git; the generated skill copy is committed for direct GitHub plugin installation. Edit canonical files first, rerun the builder, review and commit the resulting bundle updates.

`--check` detects drift without modifying files. It is a consistency check, not an official platform validator or a guarantee of directory approval. Check manifests with the host's validator and test installation on your intended client before announcing runtime support.

## Packaging verification

The Claude plugin and marketplace passed `claude plugin validate`. Local marketplace registration and plugin installation were also exercised in a disposable `CLAUDE_CONFIG_DIR`; the CLI reported the plugin enabled and its installed skill matched the canonical file. That temporary configuration was removed. No model session or target probe ran.

The portable manifest passed the Agent Plugins 1.0.0 JSON schema. Both skill copies passed skill validation. Offline checks covered deterministic ZIPs, private-file exclusion, stale bundle detection, unexpected bundled-file rejection, symlink rejection, version mismatches and relative documentation links. ChatGPT/Codex client installation and OpenAI directory submission have not been tested or performed.
