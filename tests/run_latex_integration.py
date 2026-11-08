#!/usr/bin/env python3
"""Exercise legal citation semantics in isolated, synthetic LaTeX documents.

This is an explicit integration check, not part of unittest discovery. It needs
latexmk, the selected TeX engine, makeindex and pdftotext on PATH. The fixture's
source names and citations are invented test markers, never research examples.
No network access, shell escape, thesis edits or third-party Python modules are
used. All generated files are removed with their temporary directories.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata


ROOT = Path(__file__).resolve().parents[1]
SUPPORT_FILES = ("lawthesis.cls", "legalcite.sty", "latexmkrc")

# Every entry below is synthetic and exists solely to make output observable.
# Deliberately reverse declaration/citation order for the secondary sources.
DECLARATIONS = r'''
\DeclareLawSource{alpha-case}{case}{North! @ | "Test"}{alpha!@|"sort}
  {ALPHA FULL CITATION}{ALPHA SHORT}{ALPHA TABLE ! @ | "LITERAL"}{}
\DeclareLawSource{beta-case}{case}{South Test Jurisdiction}{beta}
  {BETA FULL CITATION}{BETA SHORT}{BETA TABLE ENTRY}{}
\DeclareLawSource{uncited-case}{case}{South Test Jurisdiction}{uncited}
  {UNCITED CASE FULL}{UNCITED CASE SHORT}{UNCITED CASE TABLE}{}
\DeclareLawSource{z-secondary}{secondary}{Test}{zeta}
  {ZETA FULL SECONDARY}{ZETA SHORT}{ZETA TABLE UNUSED}
  {ZETA BIBLIOGRAPHY ENTRY}
\DeclareLawSource{a-secondary}{secondary}{Test}{alpha}
  {ALPHA FULL SECONDARY}{SECONDARY ALPHA SHORT}{ALPHA TABLE UNUSED}
  {ALPHA BIBLIOGRAPHY ENTRY}
\DeclareLawSource{uncited-secondary}{secondary}{Test}{uncited}
  {UNCITED SECONDARY FULL}{UNCITED SECONDARY SHORT}{UNCITED SECONDARY TABLE}
  {UNCITED SECONDARY BIBLIOGRAPHY}
\DeclareLawSource{test-statute}{legislation}{Test Statute Jurisdiction}{statute}
  {TEST STATUTE FULL}{TEST STATUTE SHORT}{TEST STATUTE TABLE}{}
\DeclareLawSource{test-treaty}{treaty}{Test Treaty Jurisdiction}{treaty}
  {TEST TREATY FULL}{TEST TREATY SHORT}{TEST TREATY TABLE}{}
'''

POSITIVE_BODY = r'''
\begin{document}
\frontmatter
\PrintLawTables
\mainmatter
\chapter{CONTEXT ONE}
\typeout{LAWTEST_CONTEXT_ONE=\arabic{lawcitationcontext}}
This document contains synthetic test markers only.

First citation.\lawcite[101]{alpha-case}

Ordinary repeat.\lawcite[102]{alpha-case}

Forced full citation.\lawfullcite[103]{alpha-case}

Repeat after forced full.\lawcite[104]{alpha-case}

Two sources first used in one note.\footnote{JOINT NOTE START:
  \lawref[201]{beta-case}; \lawref[301]{z-secondary}. JOINT NOTE END.}

Repeat the first joint-note source.\lawcite[202]{beta-case}

Repeat the second joint-note source.\lawcite[302]{z-secondary}

Alphabetically earlier secondary source, cited later.\lawcite[401]{a-secondary}

\newpage
A separate thesis page must enter the authority table.\lawcite[105]{alpha-case}

\chapter{CONTEXT TWO}
\typeout{LAWTEST_CONTEXT_TWO=\arabic{lawcitationcontext}}
Numbered chapters restart the citation context and footnote counter.
\lawcite[106]{alpha-case}

Its repeat refers to this chapter's first note.\lawcite[107]{alpha-case}

\chapter*{STARRED CONTEXT}
\typeout{LAWTEST_CONTEXT_STAR=\arabic{lawcitationcontext}}
An unnumbered chapter resets the citation context without resetting notes.
\lawcite[108]{alpha-case}

This repeat points to the first note in the starred context.
\lawcite[109]{alpha-case}

\LawNewCitationContext
\typeout{LAWTEST_CONTEXT_MANUAL=\arabic{lawcitationcontext}}
An explicit context reset again requires a full citation.
\lawcite[110]{alpha-case}

Its repeat points to the new first note.\lawcite[111]{alpha-case}

The other primary-source indices also receive content.
\lawcite[section 7]{test-statute}
\lawcite[article 2]{test-treaty}

\PrintLawBibliography
\end{document}
'''


class IntegrationFailure(RuntimeError):
    """An executable failed or the rendered document violated a contract."""


def normalise(text: str) -> str:
    """Ignore extraction whitespace and typographic double-quote glyphs."""
    text = unicodedata.normalize("NFKC", text)
    text = text.translate(str.maketrans({"“": '"', "”": '"', "„": '"', "‟": '"'}))
    return re.sub(r"\s+", " ", text).strip()


def run(command: list[str], directory: Path, *, failure_expected: bool = False) -> subprocess.CompletedProcess:
    try:
        result = subprocess.run(
            command, cwd=directory, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, text=True, encoding="utf-8",
            errors="replace", timeout=300, check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise IntegrationFailure(f"Could not run {command[0]}: {exc}") from exc
    if result.returncode and not failure_expected:
        tail = "\n".join(result.stdout.splitlines()[-45:])
        raise IntegrationFailure(
            f"Command failed ({result.returncode}): {command!r}\n{tail}"
        )
    return result


def prepare(directory: Path, source: str) -> None:
    directory.mkdir()
    for name in SUPPORT_FILES:
        shutil.copyfile(ROOT / name, directory / name)
    (directory / "fixture.tex").write_text(source, encoding="utf-8")


def latexmk_command(engine: str) -> list[str]:
    return [
        "latexmk", "-norc", "-r", "latexmkrc",
        "-lualatex" if engine == "lualatex" else "-pdf",
        "-interaction=nonstopmode", "-halt-on-error", "-file-line-error",
        "-no-shell-escape", "fixture.tex",
    ]


def require(condition: bool, description: str, detail: str = "") -> None:
    if not condition:
        raise IntegrationFailure(description + ("\n" + detail if detail else ""))


def read_text(directory: Path, name: str) -> str:
    path = directory / name
    require(path.is_file(), f"Expected build output is missing: {name}")
    return path.read_text(encoding="utf-8", errors="replace")


def index_page_set(index_text: str) -> set[int]:
    pages: set[int] = set()
    for group in re.findall(r"\\hyperpage\{([^{}]+)\}", index_text):
        for part in group.split(","):
            match = re.fullmatch(r"\s*(\d+)(?:--(\d+))?\s*", part)
            require(match is not None, "Unexpected index page syntax", repr(part))
            start = int(match.group(1))
            finish = int(match.group(2) or start)
            require(start <= finish, "Reversed index page range", part)
            for page in range(start, finish + 1):
                require(page not in pages, "Duplicate thesis page in one authority-table entry", str(page))
                pages.add(page)
    return pages


def positive_checks(directory: Path, engine: str) -> list[str]:
    command = latexmk_command(engine)
    run(command, directory)

    # Current latexmk natively discovers imakeidx's named indices. Keep this
    # fallback for installations that leave a non-empty index unprocessed.
    generated_index = False
    for path in sorted(directory.glob("fixture-*.idx")):
        if path.stat().st_size and not path.with_suffix(".ind").is_file():
            run(["makeindex", "-o", path.with_suffix(".ind").name, path.name], directory)
            generated_index = True
    if generated_index:
        run(command[:-1] + ["-g", "fixture.tex"], directory)

    pdf = directory / "fixture.pdf"
    require(pdf.is_file(), "No PDF was produced for the positive fixture")
    text = normalise(run(["pdftotext", "-layout", str(pdf), "-"], directory).stdout)
    log = read_text(directory, "fixture.log")
    aux = read_text(directory, "fixture.aux")
    cases = read_text(directory, "fixture-cases.ind")
    case_input = read_text(directory, "fixture-cases.idx")
    checks: list[str] = []

    require("??" not in text, "Unresolved references remain in the rendered PDF")
    require("There were undefined references" not in log, "The final LaTeX log has undefined references")
    for first in (101, 103, 106, 108, 110):
        expected = f"ALPHA FULL CITATION, {first}."
        require(expected in text, "A required full citation was not rendered", expected + "\n" + text[-6500:])
    require(text.count("ALPHA FULL CITATION") == 5, "Unexpected number of full alpha citations")
    checks.append("full first citations and forced full citations")

    for pinpoint, note in ((102, 1), (104, 1), (105, 1), (107, 1), (109, 3), (111, 5)):
        expected = f"ALPHA SHORT (n {note}) {pinpoint}."
        require(expected in text, "A repeat citation points to the wrong note or has wrong punctuation", expected)
    require(text.count("ALPHA SHORT") == 6, "Unexpected number of short alpha citations")
    checks.append("short references retain original note after a forced full citation")

    require("BETA SHORT (n 5) 202." in text, "First joint-note source did not retain note 5")
    require("ZETA SHORT (n 5) 302." in text, "Second joint-note source did not retain note 5")
    checks.append("two sources first cited inside the same manually written footnote")

    contexts = {}
    for name in ("ONE", "TWO", "STAR", "MANUAL"):
        found = re.search(rf"LAWTEST_CONTEXT_{name}=(\d+)", log)
        require(found is not None, "Citation context marker missing from log", name)
        contexts[name] = found.group(1)
    require(len(set(contexts.values())) == 4, "Numbered, starred or explicit context reset failed", repr(contexts))
    for context_name, key, expected_note in (
        ("ONE", "alpha-case", 1), ("ONE", "beta-case", 5),
        ("ONE", "z-secondary", 5), ("TWO", "alpha-case", 1),
        ("STAR", "alpha-case", 3), ("MANUAL", "alpha-case", 5),
    ):
        label = f"law:{contexts[context_name]}:{key}"
        pattern = r"\\newlabel\{" + re.escape(label) + r"\}\{\{" + str(expected_note) + r"\}"
        require(re.search(pattern, aux) is not None, "Auxiliary first-note label is incorrect", label)
    checks.append("numbered chapter, starred chapter and explicit reset contexts")

    require("Table of cases" in text and "Table of legislation" in text, "Primary authority tables missing")
    case_table = text.split("Table of cases", 1)[1].split("Table of legislation", 1)[0]
    expected_jurisdiction = 'North! @ | "Test"'
    expected_entry = 'ALPHA TABLE ! @ | "LITERAL"'
    index_evidence = case_table + "\nProcessed index:\n" + cases + "\nRaw index:\n" + case_input
    require(expected_jurisdiction in case_table, "Jurisdiction MakeIndex punctuation did not survive", index_evidence)
    require(expected_entry in case_table, "Displayed MakeIndex punctuation did not survive", index_evidence)
    require("South Test Jurisdiction" in case_table and "BETA TABLE ENTRY" in case_table,
            "Second case jurisdiction or entry is missing", case_table)
    require(case_table.index(expected_jurisdiction) < case_table.index(expected_entry)
            < case_table.index("South Test Jurisdiction") < case_table.index("BETA TABLE ENTRY"),
            "Case entries are not grouped under their jurisdictions", case_table)
    require("\\subsubitem" not in cases, "Literal exclamation mark created an unintended index level", cases)
    require("TEST STATUTE TABLE" in text and "TEST TREATY TABLE" in text, "Statute or treaty entry missing")
    checks.append("separate authority tables, jurisdiction grouping and literal index metacharacters")

    cited_pages = {int(page) for page in re.findall(r"\\indexentry\{[^\n]*ALPHA TABLE[^\n]*\}\{(\d+)\}", case_input)}
    require(len(cited_pages) >= 3, "The fixture did not exercise citations on multiple thesis pages", case_input)
    entry_start = cases.find("ALPHA TABLE")
    require(entry_start >= 0, "Alpha entry missing from processed case index", cases)
    entry = re.split(r"\\(?:subitem|item|end)\b", cases[entry_start:], maxsplit=1)[0]
    printed_pages = index_page_set(entry)
    require(printed_pages == cited_pages, "Printed thesis page references differ from the citation pages",
            f"Citation pages: {sorted(cited_pages)}; printed pages: {sorted(printed_pages)}\n{entry}")
    require(text.count(expected_entry) == 1, "One authority was printed as multiple table entries")
    require(not any(token in cases for token in ("\\prop_item", "\\exp_args", "\\l__law")),
            "Unevaluated citation implementation leaked into the index", cases)
    checks.append("deduplicated thesis page references and fully expanded index entries")

    for absent in ("UNCITED CASE", "UNCITED SECONDARY", "TABLE UNUSED"):
        require(absent not in text, "Uncited or inappropriate source material appeared in the PDF", absent)
    require("Bibliography" in text, "Bibliography heading missing")
    bibliography = text.split("Bibliography", 1)[1]
    first = "ALPHA BIBLIOGRAPHY ENTRY"
    second = "ZETA BIBLIOGRAPHY ENTRY"
    require(bibliography.count(first) == bibliography.count(second) == 1,
            "Cited secondary sources were missing or duplicated", bibliography)
    require(bibliography.index(first) < bibliography.index(second), "Secondary bibliography is not sorted")
    require("TABLE ENTRY" not in bibliography and "TEST STATUTE" not in bibliography
            and "TEST TREATY" not in bibliography, "A primary authority leaked into the secondary bibliography")
    checks.append("only cited secondary sources in sorted bibliography; uncited sources absent")
    return checks


def negative_check(directory: Path, engine: str, name: str, source: str, error: str) -> str:
    prepare(directory, source)
    result = run(latexmk_command(engine), directory, failure_expected=True)
    log_path = directory / "fixture.log"
    evidence = normalise(result.stdout + "\n" + (log_path.read_text(errors="replace") if log_path.is_file() else ""))
    require(result.returncode != 0, f"Malformed {name} fixture incorrectly succeeded")
    # TeX can wrap a log line in the middle of a key or immediately before its
    # closing quote. Ignore that physical wrapping when matching the diagnostic.
    compact_error = re.sub(r"\s+", "", error)
    compact_evidence = re.sub(r"\s+", "", evidence)
    require(compact_error in compact_evidence,
            f"Malformed {name} fixture failed for an unrelated reason", evidence[-5000:])
    return f"{name} produces an explicit build failure"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine", choices=("lualatex", "pdflatex"), default="lualatex",
                        help="LuaLaTeX by default; pdflatex is an explicit compatibility check.")
    args = parser.parse_args(argv)
    missing = [name for name in ("latexmk", args.engine, "makeindex", "pdftotext") if not shutil.which(name)]
    if missing:
        print("Integration check requires these executables on PATH: " + ", ".join(missing), file=sys.stderr)
        return 2
    for name in SUPPORT_FILES:
        if not (ROOT / name).is_file():
            print(f"Integration support file is missing: {name}", file=sys.stderr)
            return 2

    try:
        with tempfile.TemporaryDirectory(prefix="lexthesis-latex-") as temporary:
            workspace = Path(temporary)
            positive = workspace / "positive"
            prepare(positive, "\\documentclass{lawthesis}\n" + DECLARATIONS + POSITIVE_BODY)
            checks = positive_checks(positive, args.engine)
            checks.append(negative_check(
                workspace / "unknown", args.engine, "unknown citation key",
                r"\documentclass{lawthesis}\begin{document}\chapter{Test}\lawcite{missing-source}\end{document}",
                "Unknown authority key 'missing-source'",
            ))
            repeated = r"\DeclareLawSource{duplicate-key}{case}{Test}{duplicate}{TEST FULL}{TEST SHORT}{TEST TABLE}{}"
            checks.append(negative_check(
                workspace / "duplicate", args.engine, "duplicate source key",
                "\\documentclass{lawthesis}\n" + repeated + "\n" + repeated
                + "\n\\begin{document}Test.\\end{document}\n",
                "Duplicate authority key 'duplicate-key'",
            ))
            checks.append(negative_check(
                workspace / "invalid-kind", args.engine, "unsupported authority kind",
                r"\documentclass{lawthesis}\DeclareLawSource{bad-kind}{unsupported}{Test}{test}{FULL}{SHORT}{TABLE}{}"
                r"\begin{document}Test.\end{document}",
                "Unknown authority kind 'unsupported'",
            ))
    except (IntegrationFailure, OSError) as exc:
        print(f"FAIL ({args.engine}): {exc}", file=sys.stderr)
        return 1

    for check in checks:
        print("PASS: " + check)
    print(f"Passed {len(checks)} LaTeX integration checks with {args.engine}; temporary files removed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
