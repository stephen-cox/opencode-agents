#!/usr/bin/env python3
"""
AI Dev Automation Runner

Orchestrates AI-driven development for a Backlog.md milestone using
OpenCode's HTTP API. For each task: implements via a coder agent,
verifies via an independent verifier agent, commits on success or
retries with feedback on failure.

Usage:
    python dev_runner.py --milestone milestone-auth-v1 --project-dir /path/to/project
    python dev_runner.py --milestone milestone-auth-v1 --project-dir . --max-retries 5
    python dev_runner.py --config config.yaml

Requires:
    - OpenCode server running (opencode serve --port 4096)
    - Backlog.md CLI installed and project initialised
    - pip install requests pyyaml (optional: pyyaml only needed for --config)
"""

import argparse
import json
import logging
import re
import subprocess
import sys
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import requests

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------


@dataclass
class Config:
    milestone: str
    project_dir: str
    opencode_url: str = "http://localhost:4096"
    max_retries: int = 3
    model: str = "zai-coding-plan/glm-5"
    coder_model: Optional[str] = None
    verifier_model: Optional[str] = None
    coder_agent: str = "coder"
    verifier_agent: str = "verifier"
    task_timeout: int = 1800  # max seconds to wait for a task to complete
    poll_interval: int = 10  # seconds between polling checks
    stall_timeout: int = 300  # seconds with no activity before declaring a stall
    log_level: str = "INFO"

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> "Config":
        cfg = cls(
            milestone=args.milestone,
            project_dir=str(Path(args.project_dir).resolve()),
            opencode_url=args.opencode_url.rstrip("/"),
            max_retries=args.max_retries,
            model=args.model,
            coder_model=args.coder_model,
            verifier_model=args.verifier_model,
            coder_agent=args.coder_agent,
            verifier_agent=args.verifier_agent,
            task_timeout=args.task_timeout,
            poll_interval=args.poll_interval,
            stall_timeout=args.stall_timeout,
            log_level=args.log_level,
        )
        return cfg

    @classmethod
    def from_yaml(cls, path: str) -> "Config":
        import yaml

        with open(path) as f:
            data = yaml.safe_load(f)
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------


@dataclass
class Task:
    id: str
    slug: str
    title: str
    description: str = ""
    acceptance_criteria: list[str] = field(default_factory=list)
    definition_of_done: list[str] = field(default_factory=list)
    manual_checks: list[str] = field(default_factory=list)
    plan: str = ""  # Task brief for coder (implementation plan)
    do_not_touch: list[str] = field(default_factory=list)  # Files/areas to avoid
    patterns: str = ""  # Coding patterns to follow


@dataclass
class VerifyResult:
    passed: bool
    new_criteria: list[str] = field(default_factory=list)
    feedback: str = ""


@dataclass
class TaskResult:
    task_id: str
    task_title: str
    status: str  # "done" | "blocked"
    attempts: int
    feedback: str = ""


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

log = logging.getLogger("ai-dev-runner")


def setup_logging(level: str = "INFO"):
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S")
    )
    log.addHandler(handler)
    log.setLevel(getattr(logging, level.upper(), logging.INFO))


# ---------------------------------------------------------------------------
# Backlog CLI helpers
# ---------------------------------------------------------------------------


def run_backlog(config: Config, *args: str) -> str:
    """Run a backlog CLI command and return stdout."""
    cmd = ["backlog", *args]
    log.debug(f"Running: {' '.join(cmd)}")
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=30,
        cwd=config.project_dir,
    )
    if result.returncode != 0:
        log.warning(f"backlog command failed: {result.stderr.strip()}")
    return result.stdout.strip()


def _parse_frontmatter(text: str) -> dict:
    """Parse YAML frontmatter from a markdown file's text.

    Returns a dict of the frontmatter fields.  Falls back to a simple
    line-by-line parser so that ``pyyaml`` is not required.
    """
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}
    block = m.group(1)
    try:
        import yaml

        return yaml.safe_load(block) or {}
    except ImportError:
        pass
    # Simple fallback: handles ``key: value`` and ``key: "value"``
    result: dict = {}
    for line in block.splitlines():
        kv = re.match(r"^(\w[\w-]*)\s*:\s*(.*)", line)
        if kv:
            key = kv.group(1)
            val = kv.group(2).strip().strip('"').strip("'")
            result[key] = val
    return result


def get_milestone_tasks(config: Config) -> list[Task]:
    """List To Do tasks for a milestone by reading task files directly.

    The backlog CLI ``task list`` does not support milestone filtering,
    so we read the markdown files in ``backlog/tasks/`` and match the
    ``milestone`` frontmatter field.
    """
    tasks_dir = Path(config.project_dir) / "backlog" / "tasks"
    if not tasks_dir.is_dir():
        log.warning(f"Tasks directory not found: {tasks_dir}")
        return []

    tasks = []
    for md_file in sorted(tasks_dir.glob("task-*.md")):
        try:
            text = md_file.read_text(encoding="utf-8")
        except OSError as e:
            log.debug(f"Could not read {md_file}: {e}")
            continue

        fm = _parse_frontmatter(text)

        # Filter: milestone must match AND status must be "To Do"
        if (fm.get("milestone") or "").lower() != config.milestone.lower():
            continue
        if (fm.get("status") or "").lower() != "to do":
            continue

        task_id_raw = fm.get("id", "")
        title = fm.get("title", md_file.stem)

        # Extract numeric portion from ID (e.g. "TASK-003" -> "003")
        id_match = re.match(r"(?:task-?)?([\d]+(?:\.[\d]+)?)", task_id_raw, re.IGNORECASE)
        if id_match:
            numeric_id = id_match.group(1)
        else:
            numeric_id = task_id_raw

        slug = f"task-{numeric_id}" if numeric_id else md_file.stem
        tasks.append(Task(id=numeric_id, slug=slug, title=title))

    return tasks


def get_task_details(config: Config, task: Task) -> Task:
    """Populate a task with full details from backlog CLI."""
    stdout = run_backlog(config, "task", task.id, "--plain")

    if not stdout:
        log.warning(f"Could not get details for task {task.id}")
        return task

    def extract_section(text: str, header: str) -> list[str]:
        pattern = (
            rf"(?:^|\n)(?:##?\s*)?{header}[:\s]*\n([\s\S]*?)(?=\n(?:##?\s)?[A-Z]|$)"
        )
        match = re.search(pattern, text, re.IGNORECASE)
        if not match:
            return []
        lines = match.group(1).strip().splitlines()
        items = []
        for line in lines:
            cleaned = re.sub(r"^\s*[-*]\s*\[[ x]\]\s*", "", line)
            cleaned = re.sub(r"^\s*[-*]\s*", "", cleaned).strip()
            if cleaned:
                items.append(cleaned)
        return items

    def extract_text(text: str, header: str) -> str:
        pattern = (
            rf"(?:^|\n)(?:##?\s*)?{header}[:\s]*\n([\s\S]*?)(?=\n(?:##?\s)?[A-Z]|$)"
        )
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1).strip() if match else ""

    task.description = extract_text(stdout, "Description")
    task.acceptance_criteria = extract_section(stdout, "Acceptance Criteria")
    task.definition_of_done = extract_section(stdout, "Definition of Done")
    task.manual_checks = extract_section(stdout, "Manual Checks")
    task.plan = extract_text(stdout, "Implementation Plan")
    task.do_not_touch = extract_section(stdout, "Do-Not-Touch")
    task.patterns = extract_text(stdout, "Patterns")

    return task


def set_task_status(config: Config, task_id: str, status: str):
    """Update task status via backlog CLI."""
    try:
        run_backlog(config, "task", "edit", task_id, "-s", status)
        log.info(f"  Task {task_id} → {status}")
    except Exception as e:
        log.warning(f"  Could not set task {task_id} to {status}: {e}")


def add_acceptance_criteria(config: Config, task_id: str, criteria: list[str]):
    """Add new acceptance criteria to a task."""
    for criterion in criteria:
        try:
            run_backlog(config, "task", "edit", task_id, "--ac", criterion)
            log.info(f"  Added AC to {task_id}: {criterion[:60]}...")
        except Exception as e:
            log.warning(f"  Could not add AC to {task_id}: {e}")


def add_task_notes(config: Config, task_id: str, notes: str):
    """Add notes to a task."""
    try:
        run_backlog(config, "task", "edit", task_id, "--notes", notes[:500])
    except Exception as e:
        log.warning(f"  Could not add notes to {task_id}: {e}")


# ---------------------------------------------------------------------------
# OpenCode API helpers
# ---------------------------------------------------------------------------


def opencode_health(config: Config) -> bool:
    """Check if OpenCode server is reachable."""
    try:
        r = requests.get(f"{config.opencode_url}/global/health", timeout=5)
        data = r.json()
        return data.get("healthy", False)
    except Exception:
        return False


def create_session(config: Config, title: str) -> str:
    """Create a new OpenCode session and return its ID."""
    r = requests.post(
        f"{config.opencode_url}/session",
        json={"title": title},
        timeout=15,
    )
    r.raise_for_status()
    session = r.json()
    session_id = session.get("id") or session.get("ID")
    log.debug(f"  Created session: {session_id} ({title})")
    return session_id


def _send_message_async(
    config: Config,
    session_id: str,
    body: dict,
) -> None:
    """Send a message asynchronously (returns immediately, no response body)."""
    r = requests.post(
        f"{config.opencode_url}/session/{session_id}/prompt_async",
        json=body,
        timeout=30,
    )
    if not r.ok:
        raise RuntimeError(
            f"prompt_async failed ({r.status_code}): {r.text[:500]}"
        )


def _abort_session(config: Config, session_id: str) -> None:
    """Abort a running session."""
    try:
        requests.post(
            f"{config.opencode_url}/session/{session_id}/abort",
            timeout=15,
        )
    except Exception:
        pass  # best-effort


def _get_session_status(config: Config, session_id: str) -> Optional[str]:
    """Get the session's current status type ('busy', 'idle', 'retry')."""
    try:
        r = requests.get(
            f"{config.opencode_url}/session/status",
            timeout=15,
        )
        if r.ok:
            statuses = r.json()
            status = statuses.get(session_id, {})
            return status.get("type")
        return None
    except Exception:
        return None


class _SSEActivityMonitor:
    """Monitors an SSE event stream for session activity.

    Connects to the OpenCode /event SSE endpoint and watches for events
    related to a specific session. Any matching event resets the activity
    timer, eliminating false-positive stall detection.
    """

    # Event types that indicate the session is active.  For events whose
    # session ID lives inside ``properties.info.id`` rather than
    # ``properties.sessionID``, we handle both paths in ``_extract_session_id``.
    _ACTIVITY_EVENTS = frozenset({
        "session.updated",
        "session.status",
        "message.updated",
        "message.part.updated",
        "todo.updated",
    })
    # Terminal events — the session has finished (successfully or not).
    _TERMINAL_EVENTS = frozenset({
        "session.idle",
        "session.error",
    })

    def __init__(self, config: Config, session_id: str) -> None:
        self._config = config
        self._session_id = session_id

        self._last_activity = time.time()
        self._terminal_event: Optional[dict] = None  # set on idle/error
        self._connected = False
        self._stopped = False
        self._lock = threading.Lock()

        self._thread = threading.Thread(
            target=self._run, daemon=True, name="sse-monitor"
        )
        self._thread.start()

    # -- public API -----------------------------------------------------------

    def last_activity(self) -> float:
        """Wall-clock time of the most recent activity (``time.time()``)."""
        with self._lock:
            return self._last_activity

    def touch(self) -> None:
        """Manually record activity (e.g. from a polling fallback)."""
        with self._lock:
            self._last_activity = time.time()

    def terminal_event(self) -> Optional[dict]:
        """Return the terminal event if one has been received, else None."""
        with self._lock:
            return self._terminal_event

    def is_connected(self) -> bool:
        with self._lock:
            return self._connected

    def stop(self) -> None:
        self._stopped = True

    # -- internals ------------------------------------------------------------

    @staticmethod
    def _extract_session_id(event: dict) -> Optional[str]:
        props = event.get("properties", {})
        # Most events: properties.sessionID
        sid = props.get("sessionID")
        if sid:
            return sid
        # session.updated / session.created / session.deleted: properties.info.id
        info = props.get("info")
        if isinstance(info, dict):
            return info.get("id")
        # message.part.updated carries part.sessionID in some versions
        part = props.get("part")
        if isinstance(part, dict):
            return part.get("sessionID")
        return None

    def _run(self) -> None:
        """Background thread: connect to SSE and process events."""
        while not self._stopped:
            try:
                self._stream_events()
            except Exception as exc:
                with self._lock:
                    self._connected = False
                if self._stopped:
                    return
                log.debug(f"  SSE stream error: {exc}, reconnecting in 5s")
                time.sleep(5)

    def _stream_events(self) -> None:
        r = requests.get(
            f"{self._config.opencode_url}/event",
            stream=True,
            timeout=(15, None),  # 15s connect, no read timeout
            headers={"Accept": "text/event-stream"},
        )
        r.raise_for_status()

        with self._lock:
            self._connected = True

        data_buf: list[str] = []

        for raw_line in r.iter_lines(decode_unicode=True):
            if self._stopped:
                r.close()
                return

            if raw_line is None:
                continue

            line = raw_line  # already decoded

            if line.startswith("data:"):
                data_buf.append(line[5:].strip())
            elif line == "":
                # End of SSE event frame — process accumulated data lines
                if data_buf:
                    payload_str = "\n".join(data_buf)
                    data_buf.clear()
                    try:
                        event = json.loads(payload_str)
                    except (json.JSONDecodeError, ValueError):
                        continue
                    self._handle_event(event)
            # Ignore other SSE fields (event:, id:, retry:, comments)

    def _handle_event(self, event: dict) -> None:
        etype = event.get("type", "")
        sid = self._extract_session_id(event)

        if sid != self._session_id:
            return

        if etype in self._ACTIVITY_EVENTS:
            with self._lock:
                self._last_activity = time.time()
            log.debug(f"  SSE activity: {etype}")

        if etype in self._TERMINAL_EVENTS:
            with self._lock:
                self._last_activity = time.time()
                self._terminal_event = event
            log.debug(f"  SSE terminal: {etype}")


def _get_last_assistant_message(config: Config, session_id: str) -> Optional[dict]:
    """Fetch messages for a session and return the last assistant message."""
    try:
        r = requests.get(
            f"{config.opencode_url}/session/{session_id}/message",
            timeout=15,
        )
        if not r.ok:
            return None
        messages = r.json()
        if not isinstance(messages, list):
            return None
        # Find the last assistant message
        for msg in reversed(messages):
            if msg.get("info", {}).get("role") == "assistant":
                return msg
        return None
    except Exception:
        return None


def _get_session_updated(config: Config, session_id: str) -> Optional[int]:
    """Get the session's last updated timestamp (ms)."""
    try:
        r = requests.get(
            f"{config.opencode_url}/session/{session_id}",
            timeout=15,
        )
        if r.ok:
            return r.json().get("time", {}).get("updated")
        return None
    except Exception:
        return None


def send_message(
    config: Config,
    session_id: str,
    prompt: str,
    model: Optional[str] = None,
    agent: Optional[str] = None,
) -> dict:
    """Send a message asynchronously and wait for completion.

    Uses the ``prompt_async`` endpoint (returns immediately) combined with
    an SSE event stream listener for real-time activity detection.  Falls
    back to polling ``GET /session/:id`` and ``GET /session/status`` when
    SSE is unavailable.  This eliminates false-positive stall detection
    that occurred with the previous approach of only watching
    ``session.time.updated``.
    """
    body: dict = {
        "parts": [{"type": "text", "text": prompt}],
    }
    if model:
        parts = model.split("/", 1)
        if len(parts) == 2:
            body["model"] = {"providerID": parts[0], "modelID": parts[1]}
        else:
            body["model"] = {"providerID": model, "modelID": model}
    if agent:
        body["agent"] = agent

    log.debug(f"  send_message: session={session_id}, agent={agent}, model={model}")

    # Start SSE activity monitor before sending the message so we don't
    # miss early events.
    sse = _SSEActivityMonitor(config, session_id)

    try:
        # Fire the async prompt (returns 204 immediately).
        _send_message_async(config, session_id, body)
    except Exception:
        sse.stop()
        raise

    # Poll for completion
    start_time = time.time()
    last_log_time = start_time
    last_updated_ts: Optional[int] = None

    try:
        while True:
            elapsed = time.time() - start_time

            # -- Terminal SSE event (session.idle or session.error) ---------
            terminal = sse.terminal_event()
            if terminal:
                etype = terminal.get("type", "")
                if etype == "session.error":
                    props = terminal.get("properties", {})
                    err = props.get("error", {})
                    err_name = err.get("name", "UnknownError")
                    err_msg = err.get("data", {}).get("message", "unknown")
                    raise RuntimeError(
                        f"Session error ({err_name}): {err_msg}"
                    )
                # session.idle — fetch the assistant response
                assistant_msg = _get_last_assistant_message(config, session_id)
                if assistant_msg:
                    finish = assistant_msg.get("info", {}).get("finish", "")
                    parts_count = len(assistant_msg.get("parts", []))
                    log.info(
                        f"  Complete via SSE idle (finish={finish!r}) "
                        f"after {elapsed:.0f}s, {parts_count} parts"
                    )
                    return assistant_msg
                # Idle but no assistant message yet — keep polling briefly
                log.debug("  SSE idle received but no assistant message yet")

            # -- Overall task timeout --------------------------------------
            if elapsed > config.task_timeout:
                log.error(
                    f"  Task timeout ({config.task_timeout}s) exceeded "
                    f"after {elapsed:.0f}s"
                )
                _abort_session(config, session_id)
                raise TimeoutError(
                    f"Task did not complete within {config.task_timeout}s"
                )

            # -- Polling fallbacks for activity ----------------------------
            # 1) Session updated timestamp (catches activity even if SSE
            #    disconnected).
            current_updated = _get_session_updated(config, session_id)
            if current_updated and current_updated != last_updated_ts:
                last_updated_ts = current_updated
                sse.touch()  # reset activity timer

            # 2) Session status — if the server says "busy", the session
            #    is definitely still working.
            status = _get_session_status(config, session_id)
            if status == "busy":
                sse.touch()

            # -- Stall detection -------------------------------------------
            stall_duration = time.time() - sse.last_activity()
            if stall_duration > config.stall_timeout:
                log.error(
                    f"  Session stalled — no activity for {stall_duration:.0f}s "
                    f"(threshold: {config.stall_timeout}s)"
                )
                _abort_session(config, session_id)
                raise TimeoutError(
                    f"Session stalled with no activity for "
                    f"{config.stall_timeout}s"
                )

            # -- Message-level completion check ----------------------------
            assistant_msg = _get_last_assistant_message(config, session_id)
            if assistant_msg:
                finish = assistant_msg.get("info", {}).get("finish", "")
                parts_count = len(assistant_msg.get("parts", []))
                if finish:
                    log.info(
                        f"  Polling: complete (finish={finish!r}) "
                        f"after {elapsed:.0f}s, {parts_count} parts"
                    )
                    return assistant_msg

            # -- Periodic progress log -------------------------------------
            if time.time() - last_log_time >= 30:
                parts_info = ""
                if assistant_msg:
                    parts_count = len(assistant_msg.get("parts", []))
                    parts_info = f", {parts_count} parts so far"
                sse_info = " (SSE)" if sse.is_connected() else " (polling)"
                log.info(
                    f"  Polling: {elapsed:.0f}s elapsed{parts_info}{sse_info}"
                )
                last_log_time = time.time()

            time.sleep(config.poll_interval)
    finally:
        sse.stop()


def get_session_diff(config: Config, session_id: str) -> str:
    """Get the git diff for a session's changes."""
    r = requests.get(
        f"{config.opencode_url}/session/{session_id}/diff",
        timeout=30,
    )
    r.raise_for_status()
    data = r.json()

    if isinstance(data, list):
        parts = []
        for f in data:
            path = f.get("path") or f.get("file") or "unknown"
            content = f.get("diff") or f.get("content") or json.dumps(f)
            parts.append(f"--- {path} ---\n{content}")
        return "\n\n".join(parts)

    return json.dumps(data, indent=2)


def run_shell(config: Config, session_id: str, command: str) -> dict:
    """Run a shell command via OpenCode API."""
    r = requests.post(
        f"{config.opencode_url}/session/{session_id}/shell",
        json={"agent": "coder", "command": command},
        timeout=60,
    )
    r.raise_for_status()
    return r.json()


def extract_response_text(response: dict) -> str:
    """Extract text content from an OpenCode message response."""
    text_parts = []

    # Try parts array
    parts = response.get("parts", [])
    if isinstance(parts, list):
        for part in parts:
            if isinstance(part, dict) and part.get("type") == "text":
                text_parts.append(part.get("text", "") or part.get("content", ""))

    # Fallback: content field
    if not text_parts:
        content = response.get("content")
        if isinstance(content, str):
            text_parts.append(content)
        elif isinstance(content, list):
            for c in content:
                if isinstance(c, dict) and c.get("type") == "text":
                    text_parts.append(c.get("text", ""))

    return "\n".join(text_parts)


# ---------------------------------------------------------------------------
# Prompt builders
# ---------------------------------------------------------------------------


def build_coder_prompt(
    task: Task,
    extra_criteria: list[str],
    feedback: str = "",
    do_not_touch: Optional[list[str]] = None,
    patterns: str = "",
) -> str:
    all_criteria = task.acceptance_criteria + extra_criteria
    do_not_touch_list = do_not_touch or []

    prompt = f"""## Task
{task.title}

## Backlog Task ID
{task.id}

## Description
{task.description or "No additional description provided."}

## Acceptance Criteria
Every one of these must be satisfied by your implementation:
{chr(10).join("- [ ] " + ac for ac in all_criteria)}

## Definition of Done
Your implementation is not complete until all of these are true:
{chr(10).join("- [ ] " + d for d in task.definition_of_done)}
"""

    if do_not_touch_list:
        prompt += f"""
## Do-Not-Touch List
These files/areas must NOT be modified:
{chr(10).join("- " + item for item in do_not_touch_list)}
"""

    if patterns:
        prompt += f"""
## Patterns to Follow
{patterns}
"""

    if task.manual_checks:
        prompt += f"""
## Manual Checks
These checks will be performed to verify your work:
{chr(10).join("- " + c for c in task.manual_checks)}
"""

    if feedback:
        prompt += f"""
## Previous Verification Feedback
A reviewer examined your previous attempt and found these issues.
You MUST address every one:

{feedback}
"""

    if extra_criteria:
        prompt += f"""
## Additional Criteria Added By Reviewer
These were identified as gaps during previous review and are now required:
{chr(10).join("- [ ] " + c for c in extra_criteria)}
"""

    prompt += """
## Working Practices
- Use Backlog MCP tools to claim this task (set status to In Progress) before starting
- Read relevant existing code before making changes
- Run existing tests before modifying anything
- Follow patterns and conventions already in the codebase
- Run tests after your changes to confirm nothing is broken
- If acceptance criteria are ambiguous, implement the most reasonable interpretation
- Record implementation notes in Backlog when done using MCP tools

## When You Are Finished
Run all tests and linting. Provide a summary of what you changed and why.
"""
    return prompt


def build_verifier_prompt(
    task: Task,
    extra_criteria: list[str],
    diff_text: str,
) -> str:
    all_criteria = task.acceptance_criteria + extra_criteria

    # Build numbered lists so the verifier knows which indices to check off
    ac_lines = chr(10).join(f"  {i}. [ ] {ac}" for i, ac in enumerate(all_criteria, 1))
    dod_lines = chr(10).join(
        f"  {i}. [ ] {d}" for i, d in enumerate(task.definition_of_done, 1)
    )

    return f"""You are a senior code reviewer performing a rigorous verification
of a task implementation. You are independent from the developer who wrote
this code. Your job is to verify, not to fix.

## Task
{task.slug} — {task.title}

## Task ID (for backlog commands)
{task.id}

## Description
{task.description or "No additional description."}

## Acceptance Criteria (numbered for backlog --check-ac)
Every one of these must be fully satisfied:
{ac_lines}

## Definition of Done (numbered for backlog --check-dod)
All of these must be true:
{dod_lines}

## Manual Checks
Perform each of these where possible:
{chr(10).join("- " + c for c in task.manual_checks)}

## Changes Made (diff)
```
{diff_text}
```

## Verification Process
Work through this systematically:
1. READ every changed file in full, not just the diff
2. CHECK each acceptance criterion — does the implementation satisfy it?
3. CHECK each definition of done condition
4. PERFORM each manual check where possible (run curl, check files, test endpoints)
5. RUN the test suite and linting
6. LOOK for gaps — requirements that should be acceptance criteria but are not:
   - Error handling for edge cases
   - Input validation
   - Missing test coverage for failure paths
   - Security considerations

## Important Rules
- Do NOT modify the implementation code
- Do NOT give the benefit of the doubt — if you cannot verify it, it fails
- Be specific in feedback: "No test for empty email" not "tests inadequate"

## Updating the Backlog Task
Use Backlog MCP tools to update the task based on verification results:
- On PASS: Check acceptance criteria, check definition of done items, write final summary, set status to Done
- On FAIL: Append failure details to notes, leave status as In Progress

Follow your standard verification workflow (Step 9 in your system prompt).

## Output Format — REQUIRED
You MUST end your response with a JSON code block in EXACTLY this format:

```json
{{
  "passed": false,
  "new_criteria": [
    "Specific new criterion that was missing"
  ],
  "feedback_for_developer": "Detailed, actionable feedback about what failed and why."
}}
```

If ALL criteria pass, set passed to true and leave new_criteria empty.

**IMPORTANT**: This JSON block is required for the automation runner to parse your verdict.
Do not omit it or the runner will fail to process your verification result.
"""


# ---------------------------------------------------------------------------
# Verification result parser
# ---------------------------------------------------------------------------


def parse_verify_result(response_text: str) -> VerifyResult:
    """Extract the structured verification result from the verifier's response."""

    # Try JSON in code block first
    match = re.search(r"```json\s*\n([\s\S]*?)\n\s*```", response_text)
    if match:
        try:
            data = json.loads(match.group(1))
            return VerifyResult(
                passed=data.get("passed", False),
                new_criteria=data.get("new_criteria", []),
                feedback=data.get("feedback_for_developer", ""),
            )
        except json.JSONDecodeError as e:
            log.warning(f"  JSON parsing failed for code block: {e}")

    # Try raw JSON object
    match = re.search(r'\{[\s\S]*"passed"[\s\S]*\}', response_text)
    if match:
        try:
            data = json.loads(match.group(0))
            return VerifyResult(
                passed=data.get("passed", False),
                new_criteria=data.get("new_criteria", []),
                feedback=data.get("feedback_for_developer", ""),
            )
        except json.JSONDecodeError as e:
            log.warning(f"  JSON parsing failed for raw object: {e}")

    # Fallback: try to parse structured report format (Status: PASS/FAIL)
    status_match = re.search(
        r"###?\s*Status:\s*(PASS|FAIL)", response_text, re.IGNORECASE
    )
    if status_match:
        status = status_match.group(1).upper()
        log.info(f"  Parsed status from structured report: {status}")
        return VerifyResult(
            passed=(status == "PASS"),
            new_criteria=[],
            feedback=response_text if status == "FAIL" else "",
        )

    # Final fallback: search for PASS or FAIL keywords
    if re.search(r"\bPASS\b", response_text, re.IGNORECASE):
        log.warning("  Using keyword fallback: found PASS in response")
        return VerifyResult(passed=True, new_criteria=[], feedback="")

    log.warning("  Could not parse verification result JSON or structured format")
    return VerifyResult(
        passed=False,
        new_criteria=[],
        feedback="Could not parse verifier response. Raw output available in logs.",
    )


# ---------------------------------------------------------------------------
# Git helpers
# ---------------------------------------------------------------------------


def git_commit(config: Config, session_id: Optional[str], message: str) -> bool:
    """Commit all changes. Tries OpenCode API first, falls back to CLI."""
    safe_msg = message[:120].replace('"', '\\"')

    # Try via OpenCode shell API
    if session_id:
        try:
            run_shell(config, session_id, f'git add -A && git commit -m "{safe_msg}"')
            return True
        except Exception as e:
            log.debug(f"  OpenCode shell commit failed: {e}, trying CLI")

    # Fallback to direct CLI
    try:
        subprocess.run(
            ["git", "add", "-A"],
            cwd=config.project_dir,
            check=True,
            timeout=15,
        )
        subprocess.run(
            ["git", "commit", "-m", message[:120]],
            cwd=config.project_dir,
            check=True,
            timeout=15,
        )
        return True
    except subprocess.CalledProcessError as e:
        log.error(f"  Git commit failed: {e}")
        return False


def git_revert(config: Config):
    """Revert all uncommitted changes."""
    try:
        subprocess.run(
            ["git", "checkout", "--", "."],
            cwd=config.project_dir,
            check=True,
            timeout=15,
        )
        subprocess.run(
            ["git", "clean", "-fd"],
            cwd=config.project_dir,
            check=True,
            timeout=15,
        )
        log.info("  Reverted uncommitted changes")
    except subprocess.CalledProcessError as e:
        log.warning(f"  Could not revert changes: {e}")


# ---------------------------------------------------------------------------
# Main task loop
# ---------------------------------------------------------------------------


def run_task(config: Config, task: Task) -> TaskResult:
    """Run the implement → verify → retry loop for a single task."""

    log.info(f"{'=' * 60}")
    log.info(f"TASK {task.slug}: {task.title}")
    log.info(f"{'=' * 60}")
    log.info(
        f"  AC: {len(task.acceptance_criteria)} | DoD: {len(task.definition_of_done)} | Checks: {len(task.manual_checks)}"
    )

    # Task status updates delegated to agents via MCP tools:
    # - Coder sets "In Progress" when claiming task
    # - Verifier sets "Done" on PASS
    # - Runner only sets "Blocked" on max retries (agents don't handle this case)

    feedback = ""
    new_criteria: list[str] = []
    coder_session_id: Optional[str] = None

    for attempt in range(config.max_retries):
        log.info(f"\n  --- Attempt {attempt + 1}/{config.max_retries} ---")

        # ---- IMPLEMENT ----
        log.info("  [Coder] Creating session...")
        coder_session_id = create_session(
            config,
            f"Coder: {task.slug} (attempt {attempt + 1})",
        )

        prompt = build_coder_prompt(
            task,
            new_criteria,
            feedback,
            do_not_touch=task.do_not_touch,
            patterns=task.patterns,
        )
        log.info("  [Coder] Sending prompt, waiting for implementation...")
        t0 = time.time()
        try:
            send_message(
                config,
                coder_session_id,
                prompt,
                config.coder_model or config.model,
                config.coder_agent,
            )
        except (TimeoutError, RuntimeError) as e:
            log.warning(f"  [Coder] Failed: {e}")
            feedback = f"Coder session failed: {e}. Please try again."
            git_revert(config)
            continue
        log.info(f"  [Coder] Done in {time.time() - t0:.0f}s")

        # ---- GET DIFF ----
        log.info("  [Verifier] Getting diff...")
        try:
            diff_text = get_session_diff(config, coder_session_id)
        except Exception as e:
            log.warning(f"  Could not get diff from API: {e}, using git diff")
            result = subprocess.run(
                ["git", "diff"],
                cwd=config.project_dir,
                capture_output=True,
                text=True,
            )
            diff_text = result.stdout

        if not diff_text or diff_text.strip() in ("[]", "{}"):
            log.warning("  [Verifier] No changes detected — coder produced no diff")
            feedback = "No code changes were made. The task has not been implemented."
            continue

        # ---- VERIFY ----
        log.info("  [Verifier] Creating session...")
        verifier_session_id = create_session(config, f"Verifier: {task.slug}")

        v_prompt = build_verifier_prompt(task, new_criteria, diff_text)
        log.info("  [Verifier] Sending prompt, waiting for review...")
        t0 = time.time()
        try:
            v_response = send_message(
                config,
                verifier_session_id,
                v_prompt,
                config.verifier_model or config.model,
                config.verifier_agent,
            )
        except (TimeoutError, RuntimeError) as e:
            log.warning(f"  [Verifier] Failed: {e}")
            feedback = f"Verifier session failed: {e}. Implementation may be valid but could not be verified."
            git_revert(config)
            continue
        log.info(f"  [Verifier] Done in {time.time() - t0:.0f}s")

        # ---- PARSE RESULT ----
        response_text = extract_response_text(v_response)
        log.debug(f"  [Verifier] Response text length: {len(response_text)}")
        verify = parse_verify_result(response_text)

        if verify.passed:
            log.info("  ✓ VERIFICATION PASSED")

            # Commit (verifier agent already set status to Done via MCP)
            commit_msg = f"feat({config.milestone}): {task.slug} - {task.title}"
            if git_commit(config, coder_session_id, commit_msg):
                return TaskResult(
                    task_id=task.id,
                    task_title=task.title,
                    status="done",
                    attempts=attempt + 1,
                )
            else:
                log.error("  Git commit failed despite passing verification")
                feedback = "Implementation passed verification but git commit failed."
                continue

        # ---- FAILED: prepare retry ----
        log.info(f"  ✗ VERIFICATION FAILED")
        log.info(f"    Feedback: {verify.feedback[:200]}")
        if verify.new_criteria:
            log.info(f"    New criteria: {verify.new_criteria}")

        feedback = verify.feedback

        # Verifier agent already added new criteria via MCP tools
        if verify.new_criteria:
            new_criteria.extend(verify.new_criteria)

    # ---- MAX RETRIES EXCEEDED ----
    log.warning(f"  ✗ TASK BLOCKED after {config.max_retries} attempts")
    git_revert(config)
    set_task_status(config, task.id, "Blocked")
    add_task_notes(
        config,
        task.id,
        f"Automated implementation failed after {config.max_retries} attempts. "
        f"Last feedback: {feedback[:300]}",
    )

    return TaskResult(
        task_id=task.id,
        task_title=task.title,
        status="blocked",
        attempts=config.max_retries,
        feedback=feedback,
    )


def run_milestone(config: Config) -> list[TaskResult]:
    """Run all tasks for a milestone."""

    log.info(f"Milestone: {config.milestone}")
    log.info(f"Project:   {config.project_dir}")
    log.info(f"OpenCode:  {config.opencode_url}")
    log.info("")

    # Preflight checks
    if not opencode_health(config):
        log.error("OpenCode server is not reachable. Start it with: opencode serve")
        sys.exit(1)
    log.info("OpenCode server: healthy")

    # Get tasks
    tasks = get_milestone_tasks(config)
    if not tasks:
        log.info(f"No To Do tasks found for milestone: {config.milestone}")
        return []

    log.info(f"Found {len(tasks)} tasks to process\n")

    # Get full details for each task
    for i, task in enumerate(tasks):
        tasks[i] = get_task_details(config, task)

    # Process tasks sequentially
    results: list[TaskResult] = []
    for task in tasks:
        result = run_task(config, task)
        results.append(result)

    return results


def print_summary(results: list[TaskResult]):
    """Print a summary table of all task results."""
    if not results:
        return

    done = [r for r in results if r.status == "done"]
    blocked = [r for r in results if r.status == "blocked"]

    print(f"\n{'=' * 60}")
    print("MILESTONE SUMMARY")
    print(f"{'=' * 60}")
    print(f"  Total:    {len(results)}")
    print(f"  Done:     {len(done)}")
    print(f"  Blocked:  {len(blocked)}")
    print()

    for r in results:
        icon = "✓" if r.status == "done" else "✗"
        print(
            f"  {icon} {r.task_id:>8}  {r.task_title[:45]:<45}  {r.status:<8}  {r.attempts} attempt(s)"
        )

    if blocked:
        print(f"\nBlocked tasks need manual attention:")
        for r in blocked:
            print(f"  - {r.task_id}: {r.feedback[:100]}")

    print()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="AI Dev Automation Runner — automate milestone implementation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --milestone milestone-auth-v1 --project-dir /home/user/project
  %(prog)s --milestone milestone-auth-v1 --project-dir . --max-retries 5
  %(prog)s --milestone milestone-auth-v1 --project-dir . --model anthropic/claude-sonnet-4
  %(prog)s --config config.yaml
        """,
    )
    parser.add_argument(
        "--milestone",
        "-m",
        help="Backlog.md label for the milestone (required unless --config)",
    )
    parser.add_argument(
        "--project-dir",
        "-d",
        default=".",
        help="Path to the project directory (default: current dir)",
    )
    parser.add_argument(
        "--opencode-url",
        default="http://localhost:4096",
        help="OpenCode server URL (default: http://localhost:4096)",
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        default=3,
        help="Max implement/verify cycles per task (default: 3)",
    )
    parser.add_argument(
        "--model",
        default="zai-coding-plan/glm-5",
        help="Default model ID for both coder and verifier sessions (default: zai-coding-plan/glm-5)",
    )
    parser.add_argument(
        "--coder-model",
        help="Model ID for coder agent sessions (overrides --model)",
    )
    parser.add_argument(
        "--verifier-model",
        help="Model ID for verifier agent sessions (overrides --model)",
    )
    parser.add_argument(
        "--coder-agent",
        default="coder",
        help="Agent name for coder sessions (default: coder)",
    )
    parser.add_argument(
        "--verifier-agent",
        default="verifier",
        help="Agent name for verifier sessions (default: verifier)",
    )
    parser.add_argument(
        "--task-timeout",
        type=int,
        default=1800,
        help="Max seconds to wait for a task to complete (default: 1800)",
    )
    parser.add_argument(
        "--poll-interval",
        type=int,
        default=10,
        help="Seconds between polling checks (default: 10)",
    )
    parser.add_argument(
        "--stall-timeout",
        type=int,
        default=300,
        help="Seconds with no session activity before declaring a stall (default: 300)",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level (default: INFO)",
    )
    parser.add_argument(
        "--config",
        help="Path to YAML config file (overrides other flags)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List tasks that would be processed without running them",
    )
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    # Build config
    if args.config:
        config = Config.from_yaml(args.config)
    elif args.milestone:
        config = Config.from_args(args)
    else:
        parser.error("--milestone is required (or use --config)")

    setup_logging(config.log_level)

    # Dry run mode
    if args.dry_run:
        log.info(f"DRY RUN — listing tasks for milestone: {config.milestone}\n")
        tasks = get_milestone_tasks(config)
        if not tasks:
            log.info("No To Do tasks found.")
            return
        for task in tasks:
            task = get_task_details(config, task)
            print(f"  {task.slug}: {task.title}")
            print(f"    AC:  {len(task.acceptance_criteria)}")
            print(f"    DoD: {len(task.definition_of_done)}")
            print()
        return

    # Run
    try:
        results = run_milestone(config)
        print_summary(results)

        # Exit code: 0 if all done, 1 if any blocked
        if any(r.status == "blocked" for r in results):
            sys.exit(1)

    except KeyboardInterrupt:
        log.info("\nInterrupted by user")
        sys.exit(130)
    except Exception as e:
        log.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(2)


if __name__ == "__main__":
    main()
