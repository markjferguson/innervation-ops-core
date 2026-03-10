# DIRECTIVE_009
DATE: 2026-03-08
FROM: Genspark
TO: OpenClaw
PRIORITY: HIGH
COMMIT_POLICY: COMMIT_TO_BRANCH
BRANCH: directive/DIRECTIVE_009-live-validation

## OBJECTIVE
End-to-end live validation of the Phase 1 directive bridge.
Confirm full lifecycle: pending detected processed response written log updated status updated committed to branch.

## CONTEXT
DIRECTIVE_008 delivered the bridge scaffold. This is the first live run
to confirm the bridge is functional before any merge to main.
Scope is strictly the ops/ directory. No production changes of any kind.

## FILES_IN_SCOPE
- ops/directives/pending/DIRECTIVE_009.md
- ops/directives/processed/DIRECTIVE_009.md
- ops/responses/OC_RESPONSE_DIRECTIVE_009.md
- ops/status/STATUS.md
- ops/logs/DIRECTIVE_LOG.md

## AUTHORIZED_ACTIONS
Lane 1: Read DIRECTIVE_009.md, write response/log/status files, stage changes
Lane 2: Create branch directive/DIRECTIVE_009-live-validation, commit staged files
Lane 3 BLOCKED: No push to main, no secrets, no production changes

## COMMANDS_ALLOWED
git checkout -b directive/DIRECTIVE_009-live-validation
git add ops/
git commit -m "[TEST] DIRECTIVE_009 live validation pass"
openclaw system event --mode now

## COMMANDS_FORBIDDEN
git push origin main
Any credential or secret modification
Any file writes outside ops/ or scripts/

## DELIVERABLES
1. ops/responses/OC_RESPONSE_DIRECTIVE_009.md
   Sections: SUMMARY, ACTIONS TAKEN, FILES MODIFIED, COMMANDS RUN, ASSUMPTIONS, BLOCKERS, COMMIT STATUS
2. ops/status/STATUS.md updated with Phase, Last Directive, Bridge State, Timestamp
3. ops/logs/DIRECTIVE_LOG.md new entry: [TIMESTAMP] DIRECTIVE_009 Live validation COMPLETED or PARTIAL or BLOCKED
4. DIRECTIVE_009.md moved from pending/ to processed/

## SUCCESS_CRITERIA
- OC_RESPONSE_DIRECTIVE_009.md exists with all sections populated
- STATUS.md shows Last Directive: DIRECTIVE_009
- DIRECTIVE_LOG.md has new timestamped entry
- DIRECTIVE_009.md is in processed/ not pending/
- All changes committed to directive/DIRECTIVE_009-live-validation

## BLOCKERS
None anticipated. If openclaw system event --mode now fails document exact error
and fall back to openclaw agent then HTTP hook.
PARTIAL completion with full documentation is acceptable for Phase 1.

## NOTES_FOR_OC
Validation run only. No bot service changes. No Teams changes. No ngrok changes.
Scope is strictly ops/ directory. If any step is blocked document it and continue.
