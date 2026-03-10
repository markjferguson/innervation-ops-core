# Directive Bridge Runbook (Phase 1)

## Purpose
Eliminate manual copy/paste by using a thin, auditable local bridge.

## Paths
- Pending directives: ops/directives/pending/
- Processed directives: ops/directives/processed/
- Responses: ops/responses/
- Log: ops/logs/DIRECTIVE_LOG.md
- Status: ops/status/STATUS.md
- Bridge: scripts/directive_bridge.py

## How it works
1. Bridge monitors ops/directives/pending/ for new directive files.
2. For each unprocessed directive, it triggers OpenClaw via:
   - `openclaw system event --mode now ...`
3. OpenClaw processes the directive and writes:
   - ops/responses/OC_RESPONSE_<DIRECTIVE_ID>.md
   - updates ops/status/STATUS.md
   - appends to ops/logs/DIRECTIVE_LOG.md
4. Bridge moves the directive into ops/directives/processed/.

## Safety boundaries
- Bridge does not execute arbitrary shell commands.
- All heavy execution occurs inside OpenClaw, bounded by directive policy.
- Default commit policy: COMMIT_TO_BRANCH (never push to main).

## Testing
1. Drop a test directive file into ops/directives/pending/.
2. Start the bridge.
3. Verify OC_RESPONSE, STATUS, and DIRECTIVE_LOG update.
