#!/usr/bin/env python3
"""Build a known thesis entrypoint locally, without shell escape or network use."""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import subprocess
import sys

try:
    from ._common import ENTRYPOINTS, ROOT, checked_output_dir
    from .check import audit_log
except ImportError:
    from _common import ENTRYPOINTS, ROOT, checked_output_dir
    from check import audit_log


def verify_authority_tables(output: Path, entrypoint: str) -> None:
    """Require processed output for every non-empty thesis authority index."""
    if entrypoint == "propositions":
        return
    for category in ("cases", "legislation", "treaties"):
        index = output / f"{entrypoint}-{category}.idx"
        processed = index.with_suffix(".ind")
        if index.is_symlink() or processed.is_symlink():
            raise ValueError(f"Refusing a symlinked authority index: {index.name}")
        if not index.is_file():
            raise RuntimeError(f"Expected authority index was not generated: {index.name}")
        # An adapted thesis may legitimately cite no sources of one kind.
        # MakeIndex need not produce a table for a completely empty index.
        if index.stat().st_size and (not processed.is_file() or not processed.stat().st_size):
            raise RuntimeError(f"Authority table was not processed: {processed.name}")


def build(entrypoint: str, engine: str = "lualatex", root: Path = ROOT) -> Path:
    if engine not in {"lualatex", "pdflatex"}:
        raise ValueError("Only lualatex and the explicit pdflatex fallback are supported.")
    output = checked_output_dir(root, entrypoint)
    source = root / f"{entrypoint}.tex"
    if not source.is_file() or source.is_symlink():
        raise ValueError(f"Missing regular entrypoint: {source.name}")
    for executable in ("latexmk", engine, "makeindex"):
        if shutil.which(executable) is None:
            raise RuntimeError(f"Missing {executable}; run python3 scripts/doctor.py for help.")
    console_path = output / "build-console.log"
    if console_path.is_symlink():
        raise ValueError("Refusing a symlinked build log.")
    latexmk = [
        "latexmk", "-norc", "-r", str(root / "latexmkrc"),
        "-lualatex" if engine == "lualatex" else "-pdf",
        "-interaction=nonstopmode", "-halt-on-error", "-file-line-error",
        "-no-shell-escape", "-outdir=" + str(output), source.name,
    ]
    with console_path.open("w", encoding="utf-8") as console:
        def run(command):
            console.write("COMMAND: " + repr(command) + "\n")
            console.flush()
            try:
                subprocess.run(command, cwd=root, stdout=console, stderr=subprocess.STDOUT,
                               check=True, timeout=300)
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
                raise RuntimeError(f"Build command failed; see {console_path}") from exc

        run(latexmk)
        # latexmk discovers and processes all named indexes through the
        # list-form callback in latexmkrc, then converges cross-references.
        # Running makeindex again here would be redundant and could violate
        # TeX's openout_any restrictions when given absolute output paths.
    verify_authority_tables(output, entrypoint)
    pdf = output / f"{entrypoint}.pdf"
    if not pdf.is_file() or pdf.is_symlink():
        raise RuntimeError(f"No regular PDF was produced at {pdf}")
    errors = [issue for issue in audit_log(output / f"{entrypoint}.log") if issue.level == "error"]
    if errors:
        raise RuntimeError("Final PDF has unresolved build problems:\n" + "\n".join(map(str, errors)))
    return pdf


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("entrypoint", nargs="?", default="main", choices=ENTRYPOINTS)
    parser.add_argument("--engine", choices=("lualatex", "pdflatex"), default="lualatex",
                        help="Use pdflatex only when the selected content and fonts support it.")
    args = parser.parse_args(argv)
    try:
        pdf = build(args.entrypoint, args.engine)
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"Build failed: {exc}", file=sys.stderr)
        return 1
    print(f"Built {pdf.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
