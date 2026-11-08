# Verification record

Release candidate 1.0.0. Verification date: 8 November 2026.

This record describes concrete checks. It does not certify the legal accuracy of a future thesis, compliance with every university or citation manual, or PDF/UA and PDF/A conformance.

## Software and citation checks

- **35 standard-library regression tests pass.** Coverage includes nested citation parsing, missing and duplicate keys, inconsistent provenance records, malformed and credential-bearing URLs, future verification dates, missing cross-references, submission placeholders, build-path boundaries and export safety.
- **10 semantic LaTeX integration checks pass with LuaLaTeX.** The fixture is compiled in an isolated temporary directory. Assertions inspect PDF text and actual auxiliary/index files. They cover first/repeated/forced-full citations, shared notes, numbered/starred/manual contexts, multiple jurisdictions, literal index punctuation, deduplicated thesis pages, only-cited sorted bibliography and expected failures for malformed authorities.
- **The strict submission audit rejects the untouched working example.** Instructional prompts and demonstration metadata are intentionally unfinished. Ordinary template CI treats them as review warnings.
- **The fresh source ZIP compiles with native latexmk.** A clean extracted project automatically reads the root `latexmkrc`, selects LuaLaTeX and produces all three authority tables without Python or an explicit configuration-file argument.
- **The build helper works with a project path containing spaces.**
- **Source ZIP bytes are deterministic for unchanged input.** Entries and timestamps are fixed; the embedded manifest records SHA-256 hashes. This is an archive reproducibility claim, not a claim of bit-identical PDFs across TeX distributions.

## Repeating the checks

```bash
python3 scripts/doctor.py
python3 scripts/check.py
python3 -m unittest discover -s tests -v
python3 tests/run_latex_integration.py
python3 scripts/build.py main
python3 scripts/check.py --log build/main/main.log
python3 scripts/package.py
```

The integration test additionally needs `pdftotext` (Poppler). CI installs it. The seven supported entrypoints are listed in the README and the build workflow.

## Environment and scope

Local verification uses LuaHBTeX 1.18.0, LaTeX 2024-11-01, KOMA-Script 3.43 and latexmk 4.86, with Latin Modern fonts. The supplied execution environment needed scratch-only TeX dependency repair before testing; no such environment-specific paths are shipped in the template. CI independently installs a conventional TeX toolchain on Ubuntu 24.04. Its current run status is visible in the repository's Actions page.

The source checker inspects literal commands in the project's recognised source files. It does not evaluate arbitrary TeX macros or infer which conditional branch an author intends to submit. It can therefore flag an unused draft or alternative chapter. Remove unused demonstration files from the scanned source directories or resolve their warnings deliberately. The compiler and PDF review remain necessary.

The source register records bibliographic identity and the stated inspected passages. The checks do not change a record's verification scope or mark a proposition as legally verified.

## PDF review

All seven supported entrypoints compile successfully. The final logs contain no issues recognised by the log auditor; the 29 source-review warnings in the untouched template are intentional instructional prompts and demonstration metadata.

| Entrypoint | Pages | PDF dimensions | Verified purpose |
| --- | ---: | --- | --- |
| `main` | 23 | A4 | Reading copy and released example PDF |
| `review` | 25 | A4 | Double-spaced body with line numbers |
| `print` | 37 | A4 | Double-sided layout with right-hand chapter openings |
| `anonymous` | 22 | A4 | Configured identity suppression and review layout |
| `groningen` | 37 | 170 × 240 mm | Compact double-sided institutional profile |
| `articles` | 23 | A4 | Article-integration chapter alternative |
| `propositions` | 1 | A4 | Separate editable propositions sheet |

The main, review and Groningen PDFs were rendered page by page and visually inspected for title layout, contents, chapter hierarchy, footnotes, authority tables, bibliography, language rendering and page numbering. Deliberate blank versos in print profiles preserve right-hand chapter openings. The anonymous PDF's author metadata is empty, and its extracted text omits the configured author, university and supervisor placeholders. Authors must still review their entire manuscript and embedded material. Page dimensions and page counts were read from the generated PDF files; these counts describe this working example, not an institutional length requirement.

The default PDF offers selectable text, metadata, bookmarks and links. It is not tagged-PDF certification. See the accessibility guide for the additional work required.

## Export boundaries

The source export excludes designated private folders, Git history and generated build outputs. It preserves `frontmatter/approved-title.pdf` and PDF source figures under `assets/`. Allowed source files can still contain confidential information. Review both the files and the manifest before sharing.
