#!/usr/bin/env python3
"""Audit literal thesis sources and final build logs without network access.

The checks detect mechanical problems. They do not establish that a source
supports an argument, a pinpoint is correct, or a thesis meets local rules.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import date
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

try:
    from ._common import ROOT, SourceSyntaxError, executable_tex, literal_commands, source_files
except ImportError:
    from _common import ROOT, SourceSyntaxError, executable_tex, literal_commands, source_files


KINDS = {"case", "legislation", "treaty", "secondary"}
CSV_FIELDS = ["key", "kind", "jurisdiction", "url", "version", "verified_on", "verification_scope"]
KEY_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9:_.-]*\Z")
PLACEHOLDER = re.compile(
    r"\b(?:TODO|FIXME|TBD|PLACEHOLDER)\b|\\(?:todo|lawtodo|lawprompt|lawexamplenote)\b|"
    r"\b(?:Your Name|Your Full Name|Your University|Example Candidate|"
    r"Candidate Name|Name Surname|REPLACE ME|DEMONSTRATION ONLY)\b",
    re.IGNORECASE,
)
DEMO_METADATA = re.compile(
    r"\b(?:working example|working template|demonstration date|demonstration title page|"
    r"Supervisor names and approved titles|Law, authority and accountable institutions|"
    r"Recht, gezag en verantwoordelijke instituties|"
    r"Een werkmodel voor rechtswetenschappelijk promotieonderzoek)\b", re.IGNORECASE,
)
PENDING_VERIFICATION = re.compile(
    r"\b(?:unverified|pending verification|not yet verified|to be checked)\b", re.IGNORECASE,
)


@dataclass(frozen=True)
class Issue:
    level: str
    code: str
    path: str
    line: int
    message: str

    def __str__(self):
        return f"{self.level.upper()} {self.path}:{self.line} [{self.code}] {self.message}"


def audit_sources(root: Path, submission: bool = False) -> list[Issue]:
    issues: list[Issue] = []

    def add(level, code, path, line, message):
        issues.append(Issue(level, code, str(path), line, message))

    registry = root / "references" / "authorities.tex"
    sources: dict[str, tuple[str, ...]] = {}
    if not registry.is_file() or registry.is_symlink():
        add("error", "missing-registry", "references/authorities.tex", 1,
            "A regular source-registry file is required.")
    else:
        try:
            text = executable_tex(registry.read_text(encoding="utf-8"))
            for _, fields, line in literal_commands(text, ("DeclareLawSource",), 8, exact=True):
                key, kind, jurisdiction, sort_key, full, short, table, bibliography = fields
                if not KEY_PATTERN.fullmatch(key):
                    add("error", "invalid-key", "references/authorities.tex", line,
                        f"Source key {key!r} must be a literal identifier.")
                if key in sources:
                    add("error", "duplicate-key", "references/authorities.tex", line,
                        f"Duplicate source key {key!r}.")
                sources[key] = fields
                if kind not in KINDS:
                    add("error", "invalid-kind", "references/authorities.tex", line,
                        f"Unknown source kind {kind!r}.")
                for name, value in zip(("jurisdiction", "sort key", "full citation", "short citation", "table citation"),
                                       (jurisdiction, sort_key, full, short, table)):
                    if not value:
                        add("error", "empty-field", "references/authorities.tex", line,
                            f"Source {key!r} has no {name}.")
                if kind == "secondary" and not bibliography:
                    add("error", "empty-bibliography", "references/authorities.tex", line,
                        f"Secondary source {key!r} needs its bibliography form.")
        except (UnicodeError, SourceSyntaxError, OSError) as exc:
            add("error", "registry-syntax", "references/authorities.tex", 1, str(exc))
        if not sources:
            add("error", "empty-registry", "references/authorities.tex", 1,
                "No valid source declarations were found.")

    register = root / "references" / "source-register.csv"
    seen_rows: set[str] = set()
    if not register.is_file() or register.is_symlink():
        add("error", "missing-register", "references/source-register.csv", 1,
            "The source-verification register is required.")
    else:
        try:
            with register.open(encoding="utf-8-sig", newline="") as stream:
                reader = csv.DictReader(stream)
                if reader.fieldnames != CSV_FIELDS:
                    add("error", "register-schema", "references/source-register.csv", 1,
                        "Expected columns: " + ",".join(CSV_FIELDS))
                else:
                    for row in reader:
                        line = reader.line_num
                        if None in row or any(value is None for value in row.values()):
                            add("error", "register-row", "references/source-register.csv", line,
                                "Row has the wrong number of fields.")
                            continue
                        row = {name: value.strip() for name, value in row.items()}
                        key = row["key"]
                        if key in seen_rows:
                            add("error", "duplicate-register-key", "references/source-register.csv", line,
                                f"Duplicate register key {key!r}.")
                        seen_rows.add(key)
                        if key not in sources:
                            add("error", "unregistered-source", "references/source-register.csv", line,
                                f"{key!r} has no source declaration.")
                        elif (row["kind"], row["jurisdiction"]) != (sources[key][1], sources[key][2]):
                            add("error", "register-mismatch", "references/source-register.csv", line,
                                f"Kind or jurisdiction differs from the declaration for {key!r}.")
                        try:
                            url = urlsplit(row["url"])
                            good_url = (url.scheme in {"http", "https"} and bool(url.hostname)
                                        and not url.username and not url.password
                                        and not any(char.isspace() for char in row["url"]))
                            if not good_url:
                                raise ValueError("Use an absolute HTTP(S) URL without credentials.")
                        except ValueError:
                            # Do not echo a rejected URL: it might contain credentials.
                            add("error", "invalid-url", "references/source-register.csv", line,
                                "Use an absolute HTTP(S) URL without credentials or whitespace.")
                        try:
                            verified = date.fromisoformat(row["verified_on"])
                            if verified.isoformat() != row["verified_on"] or verified > date.today():
                                raise ValueError("The verification date must be ISO YYYY-MM-DD and not in the future.")
                        except ValueError:
                            add("error", "invalid-date", "references/source-register.csv", line,
                                "Use a real, non-future verification date in YYYY-MM-DD form.")
                        for name in ("version", "verification_scope"):
                            if not row[name]:
                                add("error", "empty-register-field", "references/source-register.csv", line,
                                    f"{key!r} needs an explicit {name}.")
                        if PENDING_VERIFICATION.search(row["verification_scope"]):
                            add("error" if submission else "warning", "pending-verification",
                                "references/source-register.csv", line,
                                f"Source {key!r} is marked as requiring verification; the audit does not change that status.")
        except (UnicodeError, csv.Error, OSError) as exc:
            add("error", "register-syntax", "references/source-register.csv", 1, str(exc))
    for key in sorted(set(sources) - seen_rows):
        add("error", "missing-verification", "references/source-register.csv", 1,
            f"Source {key!r} has no verification-register row.")

    labels: dict[str, tuple[str, int]] = {}
    references: list[tuple[str, str, int]] = []
    for path in source_files(root):
        relative = str(path.relative_to(root))
        try:
            text = executable_tex(path.read_text(encoding="utf-8"))
            for command, fields, line in literal_commands(
                    text, ("lawcite", "lawref", "lawfullcite"), optional=True):
                key = fields[0]
                if key not in sources:
                    add("error", "unknown-source", relative, line,
                        f"\\{command} refers to unknown source {key!r}.")
            for _, fields, line in literal_commands(text, ("label",)):
                label = fields[0]
                if "\\" in label or "#" in label:
                    continue
                if label in labels:
                    previous = labels[label]
                    add("error", "duplicate-label", relative, line,
                        f"Label {label!r} was already declared at {previous[0]}:{previous[1]}.")
                labels[label] = (relative, line)
            for _, fields, line in literal_commands(text, ("ref", "pageref", "autoref", "eqref", "nameref", "cref", "Cref", "LawChapterRef", "LawSectionRef")):
                for label in fields[0].split(","):
                    if "\\" not in label and "#" not in label:
                        references.append((label.strip(), relative, line))
            for _, fields, line in literal_commands(text, ("input", "include")):
                target_name = fields[0]
                if "\\" in target_name or "#" in target_name:
                    continue
                target = root / target_name
                if not target.suffix:
                    target = target.with_suffix(".tex")
                try:
                    target.resolve().relative_to(root.resolve())
                except ValueError:
                    add("error", "external-input", relative, line,
                        f"Input {target_name!r} resolves outside the project.")
                    continue
                if not target.is_file() or target.is_symlink():
                    add("error", "missing-input", relative, line,
                        f"Input {target_name!r} is not a regular project file.")
            for match in PLACEHOLDER.finditer(text):
                add("error" if submission else "warning", "placeholder", relative,
                    text.count("\n", 0, match.start()) + 1,
                    f"Review placeholder marker {match.group()!r} before submission.")
            if path.name == "metadata.tex":
                for match in DEMO_METADATA.finditer(text):
                    add("error" if submission else "warning", "demonstration-metadata", relative,
                        text.count("\n", 0, match.start()) + 1,
                        "Replace the template's demonstration metadata before submission.")
        except (UnicodeError, SourceSyntaxError, OSError) as exc:
            add("error", "source-syntax", relative, 1, str(exc))
    for label, relative, line in references:
        if label not in labels:
            add("error", "unknown-label", relative, line,
                f"Reference to undeclared literal label {label!r}.")
    return issues


LOG_ERRORS = (
    ("tex-error", re.compile(r"^!|LaTeX Error:|Package .* Error:|Undefined control sequence|Emergency stop|Fatal error", re.I)),
    ("undefined-reference", re.compile(r"(?:Citation|Reference).*undefined|There were undefined (?:references|citations)", re.I)),
    ("missing-glyph", re.compile(r"Missing character:", re.I)),
    ("rerun-required", re.compile(r"Label\(s\) may have changed|Rerun to get|Please \(re\)run (?:Biber|BibTeX)", re.I)),
    ("duplicate-destination", re.compile(r"duplicate (?:destination|identifier)|destination with the same identifier", re.I)),
)


def audit_log(path: Path) -> list[Issue]:
    issues = []
    if not path.is_file():
        return [Issue("error", "missing-log", str(path), 1, "Build log does not exist.")]
    text = path.read_text(encoding="utf-8", errors="replace")
    for line_number, line in enumerate(text.splitlines(), 1):
        for code, pattern in LOG_ERRORS:
            if pattern.search(line):
                issues.append(Issue("error", code, str(path), line_number, line.strip()))
                break
        if re.search(r"Overfull \\[hv]box", line):
            issues.append(Issue("warning", "overfull-box", str(path), line_number, line.strip()))
    if "Output written on " not in text:
        issues.append(Issue("error", "no-pdf-output", str(path), 1,
                            "The log does not report a completed PDF."))
    return issues


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--submission", action="store_true",
                        help="Fail on placeholder markers as well as mechanical errors.")
    parser.add_argument("--log", type=Path, action="append", default=[],
                        help="Also inspect a final LaTeX log; may be repeated.")
    args = parser.parse_args(argv)
    issues = audit_sources(ROOT, submission=args.submission)
    for log in args.log:
        issues.extend(audit_log(log))
    for issue in issues[:60]:
        print(issue)
    if len(issues) > 60:
        print(f"... {len(issues) - 60} further findings omitted.")
    errors = sum(issue.level == "error" for issue in issues)
    warnings = len(issues) - errors
    print(f"Audit: {errors} error(s), {warnings} review warning(s).")
    print("Mechanical checks do not verify legal propositions, pinpoints or institutional approval.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
