import re
from typing import List, Dict

# Patterns that indicate the real error, not noise
ERROR_PATTERNS = [
    r"ERROR",
    r"FAILED",
    r"error:",
    r"fatal:",
    r"Error:",
    r"Exception:",
    r"Traceback",
    r"npm ERR!",
    r"FAIL ",
    r"AssertionError",
    r"ModuleNotFoundError",
    r"ImportError",
    r"SyntaxError",
    r"TypeError",
    r"AttributeError",
    r"ConnectionRefusedError",
    r"TimeoutError",
    r"exit code [1-9]",
    r"Process completed with exit code",
    r"##\[error\]",
]

NOISE_PATTERNS = [
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}",   # timestamps
    r"^Downloading",
    r"^Extracting",
    r"^Pulling",
    r"^Already exists",
    r"^Pull complete",
    r"^\s*$",                                       # blank lines
    r"^remote: Counting",
    r"^remote: Compressing",
    r"^Receiving objects",
    r"^Resolving deltas",
]

ANSI_ESCAPE = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


def strip_ansi(text: str) -> str:
    return ANSI_ESCAPE.sub("", text)


def is_noise(line: str) -> bool:
    for pattern in NOISE_PATTERNS:
        if re.search(pattern, line):
            return True
    return False


def is_error_line(line: str) -> bool:
    for pattern in ERROR_PATTERNS:
        if re.search(pattern, line, re.IGNORECASE):
            return True
    return False


def parse_log(raw_log: str, max_chars: int = 8000) -> Dict:
    """
    Clean a raw CI log and extract the most relevant lines.
    Returns a dict with cleaned text and metadata.
    """
    lines = raw_log.splitlines()
    cleaned_lines = []
    error_lines   = []
    step_lines    = []

    for line in lines:
        line = strip_ansi(line).strip()
        if not line:
            continue
        if is_noise(line):
            continue

        # Capture GitHub Actions step markers
        if line.startswith("##[group]") or line.startswith("Run "):
            step_lines.append(line)

        if is_error_line(line):
            error_lines.append(line)

        cleaned_lines.append(line)

    # Build the focused log: steps + errors + surrounding context
    focused = []

    # Add last 10 step markers for context
    focused.extend(step_lines[-10:])

    # Add all error lines
    focused.extend(error_lines)

    # Deduplicate while preserving order
    seen = set()
    deduped = []
    for line in focused:
        if line not in seen:
            seen.add(line)
            deduped.append(line)

    focused_text = "\n".join(deduped)

    # Fallback: if focused is too short, take last N lines of cleaned log
    if len(focused_text) < 200:
        focused_text = "\n".join(cleaned_lines[-100:])

    # Truncate to max_chars from the END (most recent = most relevant)
    if len(focused_text) > max_chars:
        focused_text = focused_text[-max_chars:]

    return {
        "focused_log":    focused_text,
        "total_lines":    len(lines),
        "cleaned_lines":  len(cleaned_lines),
        "error_count":    len(error_lines),
        "has_errors":     len(error_lines) > 0,
        "step_count":     len(step_lines),
    }


def chunk_log(text: str, chunk_size: int = 3000) -> List[str]:
    """Split a long log into overlapping chunks for model input."""
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    overlap = 200
    start   = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap

    return chunks
