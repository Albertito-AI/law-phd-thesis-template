"""Shared paths and a deliberately small parser for literal LaTeX arguments.

This is not a TeX interpreter or a sandbox. It reads the documented, literal
source-registry interface; computed macro arguments require human review.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENTRYPOINTS = (
    "main", "print", "review", "anonymous", "groningen", "articles", "propositions"
)
IGNORED_PARTS = {
    ".git", ".venv", "venv", "__pycache__", "build", "dist", "private",
    "confidential", "secrets", "node_modules", ".cache",
}


class SourceSyntaxError(ValueError):
    """An argument in the documented source format is malformed."""


def blank(text: str) -> str:
    """Remove content without changing line numbers."""
    return "".join("\n" if char == "\n" else " " for char in text)


def strip_comments(text: str) -> str:
    """Strip TeX comments, preserving escaped percent signs and line numbers."""
    output = []
    for line in text.splitlines(keepends=True):
        cut = len(line)
        for index, char in enumerate(line):
            if char != "%":
                continue
            backslashes = 0
            previous = index - 1
            while previous >= 0 and line[previous] == "\\":
                backslashes += 1
                previous -= 1
            if backslashes % 2 == 0:
                cut = index
                break
        output.append(line[:cut] + blank(line[cut:]))
    return "".join(output)


def executable_tex(text: str) -> str:
    """Hide literal examples before auditing actual citation commands."""
    # These environments do not interpret citation commands in their bodies.
    environments = r"(verbatim\*?|Verbatim|lstlisting|minted)"
    text = re.sub(
        r"\\begin\{" + environments + r"\}.*?\\end\{\1\}",
        lambda match: blank(match.group()), text, flags=re.DOTALL,
    )
    text = re.sub(
        r"\\verb\*?([^A-Za-z\s])(.*?)\1",
        lambda match: blank(match.group()), text,
    )
    return strip_comments(text)


def read_group(text: str, offset: int, opening: str = "{") -> tuple[str, int]:
    """Read a balanced {...} or [...] argument, retaining its TeX content."""
    while offset < len(text) and text[offset].isspace():
        offset += 1
    if offset >= len(text) or text[offset] != opening:
        raise SourceSyntaxError(f"Expected {opening!r} at character {offset}")
    closing = "}" if opening == "{" else "]"
    start = offset + 1
    depth = 1
    brace_depth = 0
    offset += 1
    while offset < len(text):
        char = text[offset]
        if char == "\\":
            # An escaped delimiter is literal; control-word letters are not
            # delimiters, so skipping one following character is sufficient.
            offset += 2
            continue
        if opening == "[":
            if char == "{":
                brace_depth += 1
            elif char == "}":
                brace_depth -= 1
            if brace_depth:
                offset += 1
                continue
        if char == opening:
            depth += 1
        elif char == closing:
            depth -= 1
            if depth == 0:
                return text[start:offset], offset + 1
        offset += 1
    raise SourceSyntaxError(f"Unclosed {opening!r} argument at character {start - 1}")


def literal_commands(text: str, names: tuple[str, ...], arguments: int = 1,
                     optional: bool = False, exact: bool = False):
    """Yield (command, arguments, line) for documented literal commands."""
    pattern = r"(?<!\\)\\(" + "|".join(re.escape(n) for n in names) + r")(?![A-Za-z@])"
    for match in re.finditer(pattern, text):
        offset = match.end()
        line = text.count("\n", 0, match.start()) + 1
        while offset < len(text) and text[offset].isspace():
            offset += 1
        if optional and offset < len(text) and text[offset] == "[":
            _, offset = read_group(text, offset, "[")
        values = []
        for _ in range(arguments):
            value, offset = read_group(text, offset)
            values.append(value.strip())
        if exact and text[offset:].lstrip().startswith("{"):
            raise SourceSyntaxError(f"Too many arguments for \\{match.group(1)} on line {line}")
        yield match.group(1), tuple(values), line


def source_files(root: Path):
    """Yield visible .tex files without following symlinks or private trees."""
    for path in sorted(root.rglob("*.tex")):
        parts = path.relative_to(root).parts
        if any(part in IGNORED_PARTS or part.startswith(".") for part in parts):
            continue
        if path.is_symlink() or any(parent.is_symlink() for parent in path.parents if parent != root.parent):
            continue
        yield path


def checked_output_dir(root: Path, entrypoint: str) -> Path:
    """Keep build writes in the intended directory, not a symlink target."""
    if entrypoint not in ENTRYPOINTS:
        raise ValueError(f"Unknown entrypoint: {entrypoint!r}")
    output = root / "build" / entrypoint
    for path in (root / "build", output):
        if path.is_symlink():
            raise ValueError(f"Refusing symlinked output directory: {path}")
        if path.exists() and not path.is_dir():
            raise ValueError(f"Output path is not a directory: {path}")
    output.mkdir(parents=True, exist_ok=True)
    return output
