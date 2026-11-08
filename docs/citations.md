# Legal citations and source verification

The template provides an **author-curated legal footnote system**. You supply the correct full citation, short form and table entry. The software connects them to footnotes, chapter-local cross-references, authority tables and the secondary bibliography. It does not determine what the law is or format arbitrary bibliographic data into a national citation standard.

This release is **not a complete OSCOLA 5, AGLC or Bluebook renderer**. Confirm the citation style and edition required by your faculty, then review the supplied strings and repeat-reference conventions against that requirement. A citation can compile successfully and still identify the wrong source, version or proposition.

## Cite a source

The demonstration sources live in [authorities.tex](../references/authorities.tex). Their supporting records are in [source-register.csv](../references/source-register.csv).

```latex
% Create a footnote containing the source and a specific pinpoint.
The discussion refers to the specified paragraph.\lawcite[{[16]}]{vellama2013}

% A statutory subsection and a treaty provision.
The statutory example uses the as-enacted text.\lawcite[s 3(1)]{hra1998}
The treaty example identifies a provision.\lawcite[art 31(1)]{vclt1969}

% Cite within a footnote that you write yourself.
\footnote{Compare \lawref[{[8]}]{marleasing1990} with
  \lawref[art 31(1)]{vclt1969}. The examples concern different legal settings.}

% Explicitly request a full citation in its own footnote.
\lawfullcite[1]{vanhoecke2015}
```

Use braces inside the optional argument when a pinpoint itself contains square brackets: `[{[16]}]`. For ordinary page numbers or provisions, use `[1]`, `[s 3(1)]` or `[art 31(1)]`. A pinpoint is the location **in the cited source**. The numbers in an authority table instead identify the **pages of your thesis** on which that source is cited.

The first citation to a source in a chapter prints the full citation. Later citations in that chapter use the supplied short form with a reference to the first note, such as `Vellama (n 3) [16]`. A new chapter starts a new first-citation context. The system does not generate `ibid`. Use `\lawref` inside an existing footnote; nesting `\lawcite` inside a footnote would create a second footnote.

Supply the pinpoint on every citation that needs one. A repeat reference does not inherit the preceding pinpoint. Do not put a citation command in a chapter title, section title, running header, caption, table of contents entry or PDF bookmark. Place the citation in adjacent prose or a suitable note instead. These moving elements may be processed more than once and can produce misleading citation state.

## Add or edit an authority

Each `\DeclareLawSource` has exactly eight brace-delimited arguments. For example:

```latex
\DeclareLawSource{hra1998}{legislation}{United Kingdom}{human-rights-act-1998}
  {Human Rights Act 1998}
  {Human Rights Act 1998}
  {Human Rights Act 1998}
  {}
```

| Argument | Purpose | Author's responsibility |
| --- | --- | --- |
| `key` | Stable identifier used in citation commands | Use a unique combination of lowercase ASCII letters, digits and hyphens. |
| `kind` | Selects the relevant table or bibliography | Choose `case`, `legislation`, `treaty` or `secondary`. |
| `jurisdiction` | Groups primary authorities | Use a consistent, meaningful label, such as `Singapore` or `European Union`. For cross-jurisdictional scholarship, the examples use `International`. |
| `sort-key` | Controls ordering within a group or bibliography | Supply a stable, plain-text key consistent with the required ordering. |
| Full citation | Appears on first use in a chapter | Check name, court, report or identifier, date, edition and typography. |
| Short citation | Appears on subsequent use | Make it unambiguous; distinguish works by the same author. |
| Roman table entry | Appears in a primary-authority table | Supply a complete identifying entry without case-name italics. |
| Bibliography entry | Appears for cited secondary records | Supply the required bibliography form for `secondary`; leave `{}` for other kinds. |

Keep citation strings free of a terminal full stop and keep use-specific pinpoints out of the stored citation. LaTeX special characters need escaping, for example `\&`, `\%` and `\_`. A record may contain ordinary formatting such as `\textit{...}`. Treat source files as code: do not paste unfamiliar commands from an untrusted citation export.

The reference file is the typesetting input. The CSV is an accompanying provenance record; editing it alone does not change a printed citation. Keep both in step. Add a new source row with its version, review date and the precise scope of the checks you actually performed. Do not reuse the sample verification date for newly added material.

## Tables and bibliography

The template collects citations into separate tables of cases, legislation and treaties, with jurisdiction headings and references to thesis pages. The bibliography includes **cited secondary records only**, ordered by their sort keys. Defining a source does not by itself justify including it among works cited.

An authority mentioned only as ordinary text is not automatically indexed. Make an intentional citation through the supplied commands when you want it recorded. Review the final tables against the manuscript, including notes, appendices and discussions of contrary authority. Complete the normal multi-pass build so that page and note references settle after edits.

Sorting requires editorial judgement. A table may need a case beginning with `Re` filed under its significant word; a criminal-law work may treat `R v ...` differently from a public-law work; some institutions ask for chronological or numerical ordering of European cases. Choose the sort key accordingly. The core system does not infer these rules or create case-name aliases. Its tables are at source level: provision-level subentries, such as individual sections beneath a statute, require additional work if your rules demand them.

## Citation standards: scope and edition

Oxford published the fifth edition of OSCOLA on **25 March 2026**. Its official support page states that the listed reference-manager styles still relate to the fourth edition pending updates. The CTAN `oscola` package describes version 1.7 as targeting the fourth edition. This template does not load that package or claim to modernise its output automatically.

The fifth edition changes repeat references, including removing `ibid`, and contains revised international-law guidance. Its instructions for longer works include chapter-local citation contexts and tables of primary authorities. Following those selected conventions here does not establish complete compliance with the guide.

Sources:

- [Oxford: OSCOLA and current support materials](https://www.law.ox.ac.uk/oscola).
- [Oxford: announcement of the fifth edition](https://www.law.ox.ac.uk/content/news/fifth-edition-oxford-university-standard-citation-legal-authorities-published).
- [OSCOLA fifth edition](https://www.law.ox.ac.uk/sites/default/files/2026-03/OSCOLA%205.pdf), particularly sections 1.2 and 1.6–1.7.
- [Oxford's summary of changes](https://www.law.ox.ac.uk/sites/default/files/2026-04/OSCOLA%20key%20changes.pdf).
- [CTAN: `oscola` package documentation and version history](https://ctan.org/tex-archive/macros/latex/contrib/biblatex-contrib/oscola?lang=en).

Melbourne identifies **AGLC4 (2018)** as its published fourth edition. Its separate AGLC5 page describes work towards a prospective edition following consultation. AGLC conventions require their own review, as do the Bluebook and civil-law citation traditions. The ordinary short-form rule in this template may need adaptation even when the stored full citation is correct.

- [Melbourne: AGLC and fourth-edition details](https://law.unimelb.edu.au/mulr/aglc/about).
- [Melbourne: AGLC5 consultation status](https://law.unimelb.edu.au/mulr/aglc/aglc-5).

These edition observations were checked on **8 November 2026**. Recheck the official sources before submission.

## Using Zotero or BibLaTeX

You may continue to manage research in Zotero, another reference manager or a `.bib` database. This release does not provide a Zotero connector, `.bib` importer or automatic citation-style conversion. Transfer the needed records into `authorities.tex` and check each field against the actual source. Retain your original library as a separate research resource.

An advanced user can replace the citation layer with an appropriate BibLaTeX/Biber setup. That is a migration requiring changes to citation commands, bibliography generation and legal tables, followed by a clean rebuild and output review. Loading two citation engines together does not make their citation tracking or tables interoperable. Check the package's supported style edition and installed versions before choosing this route.

## What the sample verification means

The six examples are real sources. The register records checks of identifying details and selected pinpoints. It does **not** establish exhaustive subsequent judicial treatment, a consolidated statute's current application, treaty participation or reservations, or the correctness of a proposition in your thesis.

| Example | Demonstration pinpoint | Version or qualification |
| --- | --- | --- |
| `vellama2013` | `[16]` | Singapore Court of Appeal judgment of 5 July 2013. The parallel SLR citation is corroborated in a later official judgment. |
| `hra1998` | `s 3(1)` | The registered source is the **as-enacted** provision, not a claim about the current consolidated version. |
| `vclt1969` | `art 31(1)` | Opened for signature on 23 May 1969. The adoption date was 22 May, a different event. |
| `marleasing1990` | `[8]` | Official English EUR-Lex text; the authentic language is Spanish. |
| `vanhoecke2015` | `1` | Author-university repository supplies metadata and the article text. |
| `allea2023` | `section 2.3` | Research-integrity guidance, not legislation or evidence that a university has formally adopted it. |

Use the primary links and detailed scope in [the register](../references/source-register.csv) to inspect those checks. For the treaty dates, the [UN Treaty Collection](https://treaties.un.org/Pages/ViewDetailsIII.aspx?chapter=23&clang=_en&mtdsg_no=XXIII-1&src=TREATY) distinguishes adoption from opening for signature. For the case's report citation, see [the official Singapore judgment [2015] SGHC 48](https://www.elitigation.sg/gdviewer/s/2015_SGHC_48), paragraph 33.

For your own research, read the material at the exact pinpoint, record the relevant version and distinguish quotations, paraphrases and your own inferences. Check adverse authority and later treatment where relevant. A working link and a plausible citation are starting points for that assessment. Neither proves the legal proposition.

### Citation contexts and index punctuation

A new numbered or starred `\chapter` starts a citation context. For a custom heading that does not call `\chapter`, use `\LawNewCitationContext` before its first citation. First and forced-full citations separate the pinpoint with a comma; repeat references use a space after the note cross-reference. The formatter escapes MakeIndex metacharacters in jurisdiction, sort and table fields. These mechanics do not resolve a style manual's source-specific rules.
