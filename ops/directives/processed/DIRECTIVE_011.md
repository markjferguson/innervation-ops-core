# DIRECTIVE_011
DATE: 2026-03-10
FROM: Genspark
TO: OpenClaw (Alexa)
PRIORITY: HIGH
RESPONSE_TIMEOUT_MINUTES: 15
COMMIT_POLICY: COMMIT_TO_BRANCH
BRANCH: directive/DIRECTIVE_011-repo-migration

## OBJECTIVE
Create new GitHub repo innervation-ops-core under markjferguson.
Migrate ops/ and scripts/ directory structure from T-E-Branch-clean into it.
Update directive_bridge.py REPO path. Write README.md. Commit and push.

## CONFIRMATION REQUIRED — DO THIS FIRST
Before writing a single file, restate these instructions in your own words
in OC_RESPONSE_DIRECTIVE_011.md under CONFIRMATION. Do not proceed past
CONFIRMATION until that section is written. If you drift outside
AUTHORIZED_ACTIONS, stop and write DRIFT_ALERT immediately.

## AUTHORIZED_ACTIONS
- Create github.com/markjferguson/innervation-ops-core (public repo, no template)
- Clone to ~/innervation-ops-core
- Copy ops/ and scripts/directive_bridge.py from ~/T-E-Branch-clean
- Update REPO path in directive_bridge.py to ~/innervation-ops-core
- Write README.md (repo purpose, owner, structure, migration note)
- Initial commit and push to innervation-ops-core main

## COMMANDS_FORBIDDEN
- Do NOT modify T-E-Branch in any way
- Do NOT touch bot_service.py or Teams files
- Do NOT push to T-E-Branch main

## DELIVERABLES
1. github.com/markjferguson/innervation-ops-core live and accessible
2. ops/ structure replicated
3. directive_bridge.py REPO path updated
4. README.md written
5. OC_RESPONSE_DIRECTIVE_011.md in ops/responses/ with CONFIRMATION section

## SUCCESS_CRITERIA
- Repo exists on GitHub
- ops/ matches T-E-Branch-clean/ops/ exactly
- T-E-Branch unchanged
