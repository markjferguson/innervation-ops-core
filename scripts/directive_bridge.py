#!/usr/bin/env python3
"""
Innervation OS Directive Bridge — v3
State machine: PENDING -> AWAITING_RESPONSE -> COMPLETED | ESCALATED
Option C telemetry: reports all key events to OC dashboard via system event.
v3 changes: in-session dedup (FIRED_THIS_SESSION), mandate explicitly forbids
writing back to pending/, execution mandate strengthened.
"""
import os, time, shutil, subprocess
from pathlib import Path
from datetime import datetime

REPO            = Path(__file__).resolve().parent.parent
PENDING         = REPO / "ops" / "directives" / "pending"
AWAITING        = REPO / "ops" / "directives" / "awaiting_response"
PROCESSED       = REPO / "ops" / "directives" / "processed"
ESCALATED_DIR   = REPO / "ops" / "directives" / "escalated"
RESPONSES       = REPO / "ops" / "responses"
LOG_FILE        = REPO / "ops" / "logs" / "DIRECTIVE_LOG.md"
STATUS          = REPO / "ops" / "status" / "STATUS.md"
OC              = os.environ.get("OPENCLAW_BIN", "/opt/homebrew/bin/openclaw")
POLL            = int(os.environ.get("DIRECTIVE_POLL_SECONDS", "15"))
DEFAULT_TIMEOUT = int(os.environ.get("RESPONSE_WAIT_SECONDS", "300"))

for d in [PENDING, AWAITING, PROCESSED, ESCALATED_DIR, RESPONSES]:
    d.mkdir(parents=True, exist_ok=True)

# v3: in-session dedup — prevents re-firing if OC writes back to pending/
FIRED_THIS_SESSION = set()

def log(msg):
    line = f"[{datetime.utcnow().isoformat()}] {msg}"
    print(line, flush=True)
    return line

def oc_event(text, expect_final=False):
    """Fire telemetry event to OC dashboard (Option C). Best-effort, never blocks."""
    cmd = [OC, "system", "event", "--mode", "now", "--text", text, "--timeout", "15000"]
    if expect_final:
        cmd.append("--expect-final")
    try:
        subprocess.run(cmd, cwd=str(REPO), capture_output=True, text=True, timeout=20)
    except Exception:
        pass

def parse_timeout(directive_path: Path) -> int:
    """Read RESPONSE_TIMEOUT_MINUTES from directive header if present."""
    try:
        for line in directive_path.read_text().splitlines():
            if line.startswith("RESPONSE_TIMEOUT_MINUTES:"):
                return int(line.split(":")[1].strip()) * 60
    except Exception:
        pass
    return DEFAULT_TIMEOUT

def build_mandate(directive_path: Path) -> str:
    name = directive_path.stem
    response_path = RESPONSES / f"OC_RESPONSE_{name}.md"
    return (
        f"DIRECTIVE_ID: {name} | "
        f"FILE: {directive_path.as_posix()} | "
        f"MANDATE: Read the directive file. EXECUTE the stated objective completely. "
        f"Do not acknowledge, validate, or summarize — perform the actual work. "
        f"HARD PROHIBITION: Do NOT write any file to {PENDING.as_posix()}/ — "
        f"writing back to pending is a Lane 3 violation and will cause a re-fire loop. "
        f"AFTER completing the work: "
        f"(1) Write your complete response to {response_path.as_posix()} "
        f"with sections: SUMMARY, ACTIONS TAKEN, FILES MODIFIED, COMMANDS RUN, "
        f"ASSUMPTIONS, BLOCKERS, COMMIT STATUS. "
        f"(2) Run: git -C {REPO.as_posix()} add ops/responses/ && "
        f"git -C {REPO.as_posix()} commit -m '[RESPONSE] OC_RESPONSE_{name} written'. "
        f"(3) Write '## RESPONSE_COMPLETE' as the FINAL line of the response file — "
        f"this is the only signal the bridge accepts as completion. "
        f"Generic acknowledgments without execution are not acceptable."
    )

def trigger(directive_path: Path):
    mandate = build_mandate(directive_path)
    cmd = [OC, "system", "event", "--mode", "now",
           "--text", mandate, "--timeout", "60000"]
    log(f"Firing mandate: {directive_path.name}")
    return subprocess.run(cmd, cwd=str(REPO), capture_output=True, text=True, timeout=65)

def append_log(name, status):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.utcnow().isoformat()}] {name} — {status}\n")

def update_status(name, state):
    STATUS.write_text(
        f"Phase: Phase 1 — Active\nBridge: ACTIVE\n"
        f"Last Directive: {name}\nState: {state}\n"
        f"Timestamp: {datetime.utcnow().isoformat()}Z\n"
    )

def process_new(directive_path: Path):
    """Pick up a directive from pending/, fire mandate, move to awaiting_response/."""
    name = directive_path.stem
    # v3 dedup: never re-fire a directive already fired in this bridge session
    if name in FIRED_THIS_SESSION:
        log(f"DEDUP: {directive_path.name} already fired this session — skipping.")
        return
    log(f"Detected: {directive_path.name}")
    oc_event(f"BRIDGE_DETECTED: {directive_path.name}")
    timeout_s = parse_timeout(directive_path)
    try:
        r = trigger(directive_path)
        if r.returncode == 0:
            dest = AWAITING / directive_path.name
            shutil.move(str(directive_path), str(dest))
            (AWAITING / f".{directive_path.stem}.deadline").write_text(
                str(time.time() + timeout_s)
            )
            FIRED_THIS_SESSION.add(name)  # lock it in-session
            log(f"Mandate fired. Moved to awaiting_response/. Timeout={timeout_s}s")
            oc_event(f"BRIDGE_MANDATE_FIRED: {directive_path.name} timeout={timeout_s}s")
            append_log(directive_path.name, "TRIGGERED_AWAITING_RESPONSE")
            update_status(directive_path.name, "TRIGGERED_AWAITING_RESPONSE")
        else:
            log(f"Mandate FAILED exit={r.returncode} stderr={r.stderr.strip()}")
            oc_event(f"BRIDGE_ERROR: {directive_path.name} mandate failed exit={r.returncode}")
            append_log(directive_path.name, "MANDATE_FAILED")
    except Exception as e:
        log(f"Exception on {directive_path.name}: {e}")
        oc_event(f"BRIDGE_ERROR: {directive_path.name} exception={e}")

def reconcile_awaiting():
    """Check awaiting_response/ for completed responses or expired timeouts."""
    for directive_path in sorted(AWAITING.glob("*.md")):
        name = directive_path.stem
        response_path = RESPONSES / f"OC_RESPONSE_{name}.md"
        deadline_file = AWAITING / f".{name}.deadline"
        if response_path.exists() and "## RESPONSE_COMPLETE" in response_path.read_text():
            shutil.move(str(directive_path), str(PROCESSED / directive_path.name))
            if deadline_file.exists():
                deadline_file.unlink()
            log(f"RECONCILED: {name} sentinel found — COMPLETED")
            oc_event(f"BRIDGE_COMPLETED: {name} sentinel confirmed")
            append_log(name, "COMPLETED")
            update_status(name, "COMPLETED")
            continue
        if deadline_file.exists():
            try:
                deadline = float(deadline_file.read_text().strip())
                if time.time() > deadline:
                    shutil.move(str(directive_path), str(ESCALATED_DIR / directive_path.name))
                    deadline_file.unlink()
                    log(f"ESCALATED: {name} no response after timeout")
                    oc_event(
                        f"BRIDGE_ESCALATION: {name} timed out — moved to escalated/. Mark review required."
                    )
                    append_log(name, "ESCALATED_NO_RESPONSE")
                    update_status(name, f"ESCALATED: {name}")
            except Exception as e:
                log(f"Deadline check error for {name}: {e}")

log(f"Bridge v3 started. Poll={POLL}s  DefaultTimeout={DEFAULT_TIMEOUT}s")
oc_event(f"BRIDGE_STARTED: poll={POLL}s default_timeout={DEFAULT_TIMEOUT}s")

while True:
    for d in sorted(PENDING.glob("*.md")):
        process_new(d)
        break  # one at a time
    reconcile_awaiting()
    time.sleep(POLL)
