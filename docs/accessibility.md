# Accessibility and durable PDF output

The baseline template aims to produce readable text, useful PDF bookmarks and document-language metadata. These features help readers navigate a thesis, but the release does **not** claim validated PDF/UA conformance, PDF/A conformance or complete screen-reader accessibility. A successfully compiled PDF does not establish any of those properties.

## Write an accessible source document

Use the normal chapter, section and subsection commands to express the document's structure. Keep the hierarchy meaningful. A large bold sentence is not a substitute for a heading. Give headings descriptive names and check that the PDF bookmarks reflect the intended order.

Keep substantive text as text. Avoid converting paragraphs, legal quotations or tables into images. Supply text equivalents for scans and check optical character recognition against the original, particularly for case names, section numbers and footnote markers. Searchability does not prove that an OCR transcription is accurate.

Use descriptive link text and explain unfamiliar abbreviations. Make the meaning of a chart or table understandable without relying on colour alone. Use a clear caption and discuss the relevant result in the prose. For a figure whose interpretation depends on spatial arrangement, prepare a longer description when a short alternative is insufficient.

Prefer simple data tables with explicit headings. Avoid unnecessary merged cells and layout tables. If the thesis includes material in another language, choose fonts that contain the necessary characters and declare language changes using the language facilities of your chosen LaTeX setup. Test actual examples: a successful English build is not evidence of Arabic shaping, Thai line breaking, Chinese font coverage or correct screen-reader pronunciation.

## Review the PDF that readers will receive

Perform these checks after the final build and again after any conversion or printer processing:

- Check the document title, author and primary language in the PDF properties. For an anonymised copy, inspect those properties and the visible pages separately.
- Search for a distinctive sentence, a case name, a footnote and any non-Latin text. Copy them into a plain-text editor and check the result.
- Navigate through the bookmarks. Test links from the contents and several footnote cross-references.
- Zoom in and inspect small footnotes, quotations, dense tables and long URLs. Confirm that no text is clipped or hidden.
- Test keyboard navigation and reading order with the tools available to the intended readers. Inspect notes, tables, lists and multilingual passages, not only the title page.
- Confirm that figures have meaningful text descriptions and that any confidential or identifying metadata has been handled according to the intended release.

Automated text extraction can reveal omissions, but correct extracted text alone does not demonstrate a usable structure for assistive technology. Invite accessibility feedback from readers and the university's specialist service where possible.

## Tagged PDF is a separate, testable workflow

The [LaTeX Tagged PDF Project](https://tagging-project.latex-project.org/) documents current support and package compatibility. Its [usage instructions](https://tagging-project.latex-project.org/documentation/usage-instructions) recommend a current LaTeX release and favour LuaLaTeX for new documents. They also explain author-supplied image alternatives and table-header information. The instructions were reviewed on 8 November 2026; the available features depend on the engine, LaTeX release, document class and packages actually installed.

For a tagged version, work on a separate branch or copy. Follow the instructions matching your installed release, review the compatibility of every additional package, and rebuild the whole thesis. Inspect the tag structure and reading order, including the title pages, footnotes, legal authority tables and bibliography. Test with assistive technology and a validator appropriate to the standard required by your institution. Record the validator version, configuration, date and remaining manual checks.

Do not add a `pdfstandard` declaration and assume that it validates the result. A metadata claim is not a conformance report. The standard baseline build intentionally makes no such claim, and this document does not supply an untested tagged-PDF configuration.

Citation and indexing packages also require attention. For example, [CTAN's `oscola` entry](https://ctan.org/pkg/oscola) labels that package partially compatible with tagged PDF. This template's author-curated citation layer is different, and its complete output still requires its own tagging assessment.

## Archival and repository versions

Check your repository's actual submission requirements. **PDF/A** concerns archival preservation; **PDF/UA** concerns accessibility. Treat them as distinct requirements and verify the version of each standard requested. A printer-ready file, a repository deposit and an accessible reading copy may require different production steps.

Preserve the editable source, referenced assets, build instructions and the final submitted PDF. Keep a record of the document version and the tools used to build it. If a service converts the PDF or changes its fonts, links, encryption or metadata, inspect the resulting file again. Do not claim archival or accessibility certification without an applicable validation result and the necessary human review.

This approach follows the emphasis on explicit metadata, package compatibility and author-supplied structure in the LaTeX Project's primary documentation. It leaves the final institutional and reader-specific requirements visible instead of treating a visual inspection as sufficient.
