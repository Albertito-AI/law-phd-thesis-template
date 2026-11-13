# Getting started

## Choose your working environment

**Overleaf** is the shortest route for a newcomer: upload the ZIP linked from the README, choose LuaLaTeX, select `main.tex` and recompile. The package includes the source needed for typesetting. No Python execution or external bibliography program is required.

**Local work** gives you the source checks, deterministic packaging and ordinary Git version control. Keep the thesis project private until you deliberately prepare material for publication.

### Linux

On Debian or Ubuntu, a typical package set is:

```bash
sudo apt-get update
sudo apt-get install python3 latexmk texlive-luatex texlive-latex-extra texlive-fonts-recommended texlive-lang-european poppler-utils
```

Package versions vary by distribution. `python3 scripts/doctor.py` diagnoses what the current project needs; it does not install anything.

### Windows

Install [MiKTeX](https://miktex.org/download) or [TeX Live](https://tug.org/texlive/), together with Python 3.10 or later. MiKTeX's `latexmk` requires a working Perl installation. Use MiKTeX Console to install missing packages or select a sufficiently complete distribution. Restart the terminal after changing PATH. Use `py` in place of `python3` where appropriate.

### macOS

Install [MacTeX](https://tug.org/mactex/) and Python 3.10 or later. Confirm that `lualatex`, `latexmk` and `makeindex` are available in your terminal, then run the doctor command.

## Personalise in this order

1. Edit `config/metadata.tex`: title, author, institution, degree, supervision, date and legal cut-off.
2. Confirm margins, spacing and section requirements, then edit `config/settings.tex`.
3. Choose the entrypoint from the README. Change the included chapters in `thesis.tex` as your argument requires.
4. Replace the example abstract, declarations, chapters, appendices, acknowledgements and CV. The Dutch summary is an optional demonstration outside institutions requiring it.
5. Replace the authorities and source register with sources you have read. Retain verification scope and version information.
6. Build, inspect and revise the PDF.

## Everyday commands

```bash
python3 scripts/build.py main
python3 scripts/build.py review
python3 scripts/check.py
python3 scripts/check.py --log build/main/main.log
```

Each variant has its own directory, such as `build/review/`. The build helper runs LaTeX and MakeIndex as needed. It refuses arbitrary entrypoint names and uses subprocess argument lists.

Open `build/main/main.pdf` for the reading copy or `build/review/review.pdf` for the review copy. Other variants follow the same pattern: `build/<entrypoint>/<entrypoint>.pdf`.

If a LaTeX build command fails, inspect `build/<entrypoint>/build-console.log` for the command and its output. If LaTeX produced a log, it is in the same directory as `<entrypoint>.log`; for example, `build/review/review.log`. Missing-dependency errors can occur before these logs are created; follow the terminal message and run `python3 scripts/doctor.py`.

On a conventional TeX installation, the direct Overleaf-style build is:

```bash
latexmk -lualatex -no-shell-escape main.tex
```

The Python helper provides isolated output directories and an additional final-log check. A pdfLaTeX fallback is available with `--engine pdflatex`; verify that your languages and fonts are supported before choosing it.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| `lualatex`, `latexmk` or `makeindex` missing | Install or repair the TeX distribution and restart the terminal. |
| A package or font is missing | Run `python3 scripts/doctor.py`; install the package through your distribution's manager. |
| `Unknown authority key` | Match the key in the citation to a declaration in `references/authorities.tex`. |
| A `?` appears in a reference | Run the full build; then inspect missing labels and the final log. |
| An authority table is empty | Confirm the authority is actually cited and MakeIndex has run. Declared but uncited sources are omitted. |
| `Runaway argument` around a pinpoint | Use braces around square-bracket pinpoints: `\lawcite[{[16]}]{key}`. |
| Build succeeds but layout is wrong | Review the PDF at normal size. Inspect long case names, footnotes, tables and page breaks. |
| Strict submission check fails on the supplied example | Replace demonstration metadata and author prompts. The failure is intentional. |
| A non-Latin character is missing | Use LuaLaTeX, a font containing the required glyphs and suitable language configuration. Latin Modern does not cover every script. |
| Changes after assessment are needed | Follow your institution's approval process and keep a change record. |

## Source export

`python3 scripts/package.py` creates the source ZIP in `dist/` and embeds a SHA-256 manifest. It uses an allowlist of project paths, rejects symlinks and excludes private folders, Git history and build products. It is a source package, not a public release of your thesis PDF.

Review the manifest and archive contents before sharing. An allowlist cannot determine whether prose inside an allowed chapter contains confidential information.

The exporter preserves an approved title page at `frontmatter/approved-title.pdf` and PDF source figures under `assets/`. Review those inputs before sharing. Generated example PDFs and other PDF output paths are excluded; place a required source figure in the supported assets directory deliberately.
