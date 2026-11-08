#!/usr/bin/env python3
"""Report local prerequisites; do not install packages or contact a network."""

from __future__ import annotations

import shutil
import subprocess
import sys


REQUIRED_TOOLS = ("latexmk", "lualatex", "makeindex", "kpsewhich")
REQUIRED_TEX = (
    "scrbook.cls", "iftex.sty", "fontspec.sty", "geometry.sty", "microtype.sty", "hyperref.sty",
    "imakeidx.sty", "setspace.sty", "xcolor.sty", "booktabs.sty", "babel.sty", "dutch.ldf",
    "graphicx.sty", "pdfpages.sty", "longtable.sty", "tabularx.sty", "enumitem.sty",
    "csquotes.sty", "scrlayer-scrpage.sty", "bookmark.sty", "lineno.sty",
)
FONT_FILES = ("lmroman10-regular.otf", "lmsans10-regular.otf", "lmmono10-regular.otf")


def main() -> int:
    missing = []
    print("Law thesis build prerequisites\n")
    print(f"OK      Python {sys.version.split()[0]}: {sys.executable}")
    for name in REQUIRED_TOOLS:
        executable = shutil.which(name)
        print(f"{'OK     ' if executable else 'MISSING'} {name}: {executable or 'not installed'}")
        if not executable:
            missing.append(name)
    if shutil.which("kpsewhich"):
        for name in REQUIRED_TEX + FONT_FILES:
            result = subprocess.run(["kpsewhich", name], text=True, capture_output=True, timeout=30)
            found = result.returncode == 0 and bool(result.stdout.strip())
            print(f"{'OK     ' if found else 'MISSING'} {name}")
            if not found:
                missing.append(name)
    for name in ("latexmk", "lualatex"):
        if shutil.which(name):
            result = subprocess.run([name, "--version"], text=True, capture_output=True, timeout=30)
            lines = result.stdout.splitlines()
            print(f"\n{name}: {lines[0] if lines else 'version unavailable'}")
    print("\nDebian/Ubuntu packages: latexmk texlive-luatex texlive-latex-extra "
          "texlive-fonts-recommended texlive-lang-european.")
    print("macOS: a current MacTeX installation. Windows: current TeX Live or MiKTeX, "
          "with Perl available for latexmk.")
    print("If files exist but kpsewhich cannot find them, consult your TeX distribution's "
          "filename-database repair instructions.")
    print("Overleaf: choose LuaLaTeX, main.tex and a recent stable TeX Live version.")
    print("This template's core legal citations do not require Biber.")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
