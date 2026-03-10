# DIRECTIVE_012

## OBJECTIVE
Execute a directive by performing specified actions and generating a response file.

## MANDATE
- Read the directive file.
- Execute the stated objective completely.
- Do not acknowledge, validate, or summarize — perform the actual work.
- HARD PROHIBITION: Do NOT write any file to `/Users/markjferguson/T-E-Branch-clean/ops/directives/pending/`. Writing back to pending is a Lane 3 violation and will cause a re-fire loop.

## AFTER COMPLETING WORK
1. Write response to `/Users/markjferguson/T-E-Branch-clean/ops/responses/OC_RESPONSE_DIRECTIVE_012.md` with sections:
   - SUMMARY
   - ACTIONS TAKEN
   - FILES_MODIFIED
   - COMMANDS_RUN
   - ASSUMPTIONS
   - BLOCKERS
   - COMMIT STATUS
2. Run: `git -C /Users/markjferguson/T-E-Branch-clean add ops/responses/ && git -C /Users/markjferguson/T-E-Branch-clean commit -m '[RESPONSE] OC_RESPONSE_DIRECTIVE_012 written'`
3. Write '## RESPONSE_COMPLETE' as the FINAL line of the response file.

## FILES_IN_SCOPE
- `/Users/markjferguson/T-E-Branch-clean/ops/directives/pending/DIRECTIVE_012.md` (input)
- `/Users/markjferguson/T-E-Branch-clean/ops/responses/OC_RESPONSE_DIRECTIVE_012.md` (output)

## CONTEXT
This is a routine test for directive processing.

## COMMANDS_ALLOWED
- git add <path>
- git commit -m "<message>"
- Writing to `/Users/markjferguson/T-E-Branch-clean/ops/responses/`

## COMMANDS_FORBIDDEN
- Writing to `/Users/markjferguson/T-E-Branch-clean/ops/directives/pending/`
- Generic acknowledgments without execution.

## SUCCESS_CRITERIA
- Response file exists and is correctly formatted with '## RESPONSE_COMPLETE' as the last line.
- The response file is committed to the repository.
