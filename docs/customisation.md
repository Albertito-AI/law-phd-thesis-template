# Customisation guide

## Separate content, layout and evidence

| File or directory | Purpose |
| --- | --- |
| `config/metadata.tex` | Author, title, institution, supervision and document properties |
| `config/settings.tex` | User typography and heading settings |
| `lawthesis.cls` | Document class, layout variants and title-page behaviour |
| `legalcite.sty` | Citation state, tables and secondary bibliography |
| `thesis.tex` | Document order and chapter selection |
| `chapters/` | Research text |
| `frontmatter/` and `backmatter/` | Abstract, declarations, summaries and supporting matter |
| `references/authorities.tex` | Author-curated citation strings and sorting |
| `references/source-register.csv` | Provenance, versions and scope of source checks |
| `examples/` | Editable research records and the public demonstration PDF |

## Layout and chapter order

The generic page is A4 with a generous inner margin and a readable serif body. Print mode uses facing pages and right-hand chapter openings. Review mode uses a double-spaced body and line numbers; footnotes remain single-spaced. These are project defaults, not universal doctoral rules.

Change the order of `\input` commands in `thesis.tex` to match the argument. Rename labels deliberately and run the source checks after doing so. If you remove the comparative chapter, also remove references to it. The article-based example uses its own label so source checks can inspect both variants safely.

Avoid excessive heading depth. Use a section when it helps a reader understand the argument; paragraph length and reasoning should determine the prose rather than the availability of a heading command.

## Optional sections

The Dutch summary is included as a visible multilingual demonstration and can be removed or replaced in the generic profile. Groningen's rules require the appropriate translated title, subtitle and scientific summary. Confirm whether your institution requires a list of figures, tables, publications, declarations or a CV and add only what is needed.

The bibliography prints the secondary sources cited before `\PrintLawBibliography`. Keep all substantive citations before that command; move the command later if you add a citing section after it. Authority tables use the pages of actual citations throughout the compiled document.

## Groningen title page

Place your approved PDF at `frontmatter/approved-title.pdf`. The Groningen entrypoint includes its pages within the selected page dimensions. Confirm the final scaling and printer's requirements against the approved version. The supplied fallback title page is visibly marked as a demonstration. Anonymous mode takes precedence over an imported institutional title page.

Do not use a historical Rector's name or ceremonial wording from another student's thesis. Get the exact approved page for your candidature.

## Languages and fonts

LuaLaTeX is the default. Latin Modern fonts are distributed with common TeX installations. They avoid bundling proprietary font files, but do not include every writing system.

For another script, configure appropriate fonts and language handling, test quotations and bibliography entries, and inspect the final PDF for missing characters. Use the original source alongside a clearly identified translation when that is methodologically appropriate. Complex right-to-left text, CJK typography and script-specific legal sorting need their own tested configuration; they are not advertised as solved by the default Latin-script example.

## Citation style changes

The full, short, table and bibliography fields are intentionally separate. Edit them to the standard required for your work. AGLC, Bluebook, OSCOLA and national conventions differ. Changing a short-form field does not implement all the rules of another manual.

You can replace `legalcite.sty` with an independently tested bibliography system in your own project. Remove its commands and registry input consistently, then test the first, repeated and multi-author citations and all authority tables. The project does not ship a second, untested citation backend.

## New institutional profiles

A useful profile records the applicable rule, its issuer, version, precise location, verification date and implementation. Distinguish requirements from recommendations and unresolved questions. Supply a minimal compiling example. Do not add university logos without an appropriate right to use them or imply institutional endorsement.
