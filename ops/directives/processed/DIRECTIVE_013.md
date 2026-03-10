# DIRECTIVE_013 — Re-issue: innervation-ops-core Repository Migration

DIRECTIVE_ID: DIRECTIVE_013
PRIORITY: HIGH
RESPONSE_TIMEOUT_MINUTES: 20
ISSUED: 2026-03-10
SUPERSEDES: DIRECTIVE_011

## Objective

Create the innervation-ops-core repository and migrate the operational core files from
T-E-Branch-clean into it. This is a prerequisite for all future repo-separation work.

## Required Actions

1. Create a new GitHub repository named innervation-ops-core under the markjferguson
   account (matching the T-E-Branch remote at https://github.com/markjferguson).

2. Initialize the repo with the following directory structure:
   ops/directives/pending/
   ops/directives/awaiting_response/
   ops/directives/processed/
   ops/directives/escalated/
   ops/responses/
   ops/logs/
   ops/status/
   scripts/directive_bridge.py (copy from T-E-Branch-clean)
   README.md

3. Push an initial commit to the main branch.

4. Confirm the remote URL is reachable via git ls-remote <url>.

## HARD PROHIBITION

DO NOT write this response file to ops/directives/pending/.
DO NOT return a generic validation message.
DO NOT mark this directive complete without providing the GitHub repo URL
and the git ls-remote output as proof of execution.

## Required Response Format

Your response file (ops/responses/OC_RESPONSE_DIRECTIVE_013.md) MUST contain:
- The GitHub repository URL (https://github.com/markjferguson/innervation-ops-core)
- Output of: git ls-remote <repo-url>
- Exact commands executed
- Any errors encountered

Final line MUST be exactly:

## RESPONSE_COMPLETE
