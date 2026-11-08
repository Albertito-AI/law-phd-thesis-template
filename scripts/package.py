#!/usr/bin/env python3
"""Create a deterministic, allowlisted source ZIP suitable for Overleaf.

The ZIP is a deliberate source export, not a backup of the repository.
Designated private folders, build products and Git history are excluded.
Included source paths can still contain restricted or personal material.
Review the manifest and file contents before uploading an adapted project.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import zipfile

try:
    from ._common import ENTRYPOINTS, ROOT
except ImportError:
    from _common import ENTRYPOINTS, ROOT


ROOT_FILES = {
    *(entry + ".tex" for entry in ENTRYPOINTS), "thesis.tex", "metadata.tex", "settings.tex",
    "lawthesis.cls", "legalcite.sty", "latexmkrc", ".gitignore", "Makefile",
    "README.md", "LICENSE", "LICENSE.md", "CHANGELOG.md", "CITATION.cff",
    "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "SECURITY.md", "NOTICE.md",
}
SOURCE_TREES = {
    "chapters", "frontmatter", "backmatter", "appendices", "config", "profiles",
    "references", "examples", "docs", "assets", "scripts", "tests",
}
SOURCE_SUFFIXES = {".tex", ".sty", ".cls", ".bib", ".ist", ".csv", ".json", ".md", ".txt", ".py", ".svg", ".png", ".jpg", ".jpeg"}
PRIVATE_PARTS = {"private", "confidential", "secrets", "raw-data", "data", "notes", "__pycache__", "build", "dist"}
FIXED_TIMESTAMP = (2020, 1, 1, 0, 0, 0)


def selected_files(root: Path) -> list[Path]:
    files = []
    for name in sorted(ROOT_FILES):
        path = root / name
        if path.is_symlink():
            raise ValueError(f"Refusing source symlink: {name}")
        if path.is_file():
            files.append(path)
    for directory in sorted(SOURCE_TREES):
        start = root / directory
        if start.is_symlink():
            raise ValueError(f"Refusing source symlink: {directory}")
        if not start.is_dir():
            continue
        for current, directories, names in os.walk(start, followlinks=False):
            current_path = Path(current)
            for child in directories + names:
                if (current_path / child).is_symlink():
                    raise ValueError(f"Refusing source symlink: {(current_path / child).relative_to(root)}")
            directories[:] = sorted(name for name in directories
                                     if name not in PRIVATE_PARTS and not name.startswith("."))
            for name in sorted(names):
                path = current_path / name
                relative = path.relative_to(root).as_posix()
                allowed_pdf = (path.suffix.lower() == ".pdf" and
                               (relative == "frontmatter/approved-title.pdf" or directory == "assets"))
                if not name.startswith(".") and (path.suffix.lower() in SOURCE_SUFFIXES or allowed_pdf):
                    files.append(path)
    return sorted(files, key=lambda path: path.relative_to(root).as_posix())


def create_package(root: Path, output: Path) -> tuple[int, str]:
    if output.suffix.lower() != ".zip":
        raise ValueError("The output must have a .zip extension; source files are never package targets.")
    files = selected_files(root)
    names = {path.relative_to(root).as_posix() for path in files}
    if "main.tex" not in names:
        raise ValueError("A package must include main.tex at its top level.")
    if output.is_symlink() or any(parent.is_symlink() for parent in output.parents):
        raise ValueError("Refusing a symlinked package output path.")
    output.parent.mkdir(parents=True, exist_ok=True)
    payloads = {path.relative_to(root).as_posix(): path.read_bytes() for path in files}
    manifest = {
        "format": 1,
        "description": "Law thesis source export; Git history, designated private folders and build outputs excluded.",
        "files": {name: hashlib.sha256(data).hexdigest() for name, data in payloads.items()},
    }
    payloads["MANIFEST.json"] = (json.dumps(manifest, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(payloads.items()):
            info = zipfile.ZipInfo(name, FIXED_TIMESTAMP)
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    return len(payloads), digest


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist" / "law-phd-thesis-template.zip")
    args = parser.parse_args(argv)
    try:
        count, digest = create_package(ROOT, args.output.absolute())
    except (OSError, ValueError) as exc:
        print(f"Packaging failed: {exc}", file=sys.stderr)
        return 1
    print(f"Packaged {count} entries: {args.output}")
    print(f"SHA256 {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
