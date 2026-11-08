# Source review and design decisions

Sources checked on **8 November 2026**. This record distinguishes observed rules from project design decisions. Live documents can change; recheck the requirements applicable to your candidature.

| Primary source | Verified detail | Design response |
| --- | --- | --- |
| [Groningen formatting instructions](https://www.rug.nl/education/phd-programmes/promotieregeling/thesis-instructions-for-phd-candidates.pdf), version 4.0, October 2026 | The stated standard booklet is 170 × 240 mm; the size is not fixed. The final version, approved title page, consistent referencing and tool-use disclosure receive specific treatment. | Explicit dimensions, separate profile, approved-PDF slot and finalisation guidance. Do not substitute ISO B5 dimensions. |
| [Groningen PhD Regulations](https://www.rug.nl/about-ug/organization/rules-and-regulations/onderzoek/phd-regulations-ug-2026.pdf), March 2026, arts 4.2–4.5 | Propositions; translated title/summary; thesis contents; publication-based coherence and attribution. | Separate propositions sheet, translated-summary appendix, article-integration example and contribution prompts. |
| [Groningen title-page and ceremony guidance](https://www.rug.nl/education/phd-programmes/promotieregeling/?lang=en) | Candidate-specific title-page approval through Hora Finita before printing. | No hardcoded ceremonial names or asserted institutional approval. |
| [Groningen final-phase timeline](https://www.rug.nl/education/phd-programmes/promotieregeling/bijlage5?lang=en) | Separate approval, publicity, printing and deposit milestones. | Linked institutional checklist; no automatically calculated universal submission deadline. |
| [Oxford OSCOLA page](https://www.law.ox.ac.uk/oscola) and [fifth edition](https://www.law.ox.ac.uk/sites/default/files/2026-03/OSCOLA%205.pdf), sections 1.2, 1.6–1.7 | Fifth edition; chapter-local repeated citations; authority tables; reference-manager styles still labelled fourth edition pending updates. | Explicit author-curated mechanics and no automatic claim of full fifth-edition compliance. |
| [CTAN oscola](https://ctan.org/tex-archive/macros/latex/contrib/biblatex-contrib/oscola?lang=en), v1.7, March 2020 | Package README targets OSCOLA fourth edition. | No dependency on a package falsely described as current-edition support. |
| [Oxford Law PGR handbook 2025–26](https://www.law.ox.ac.uk/sites/default/files/2025-12/pgr_handbook_2025.pdf), printed pp 40–41 | Specific abstract, authority-table, spacing, margin and word-count rules. | Demonstrates why local rules must be separately checked. No claim to a verified Oxford 2026–27 profile. |
| [Melbourne AGLC](https://law.unimelb.edu.au/mulr/aglc/about) and [AGLC5 project](https://law.unimelb.edu.au/mulr/aglc/aglc-5) | AGLC4 and a subsequent edition project have distinct status. | No unverified AGLC5 implementation claim. |
| [Van Hoecke, university repository](https://biblio.ugent.be/publication/7145504) | Comparative-method scholarship and verifiable metadata/full text. | Question-led method prompts, case-selection and translation records. |
| [ALLEA, European Code of Conduct](https://allea.org/wp-content/uploads/2023/06/European-Code-of-Conduct-Revised-Edition-2023.pdf), revised 2023 | Research records, methods, tools and responsible reporting. | Editable evidence and tool-use records; no automatic declarations of approval or authorship. |
| [LaTeX tagging guidance](https://tagging-project.latex-project.org/documentation/usage-instructions) | Tagged output depends on current engine/package support and author-supplied structure. | Accessible-document checklist and explicit absence of PDF/UA certification for the baseline. |
| [GitHub Actions security guidance](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions) | Least privilege, action pinning and risks of untrusted code. | Read-only CI token, pinned Actions, ephemeral runners and no privileged PR triggers. |
| [Overleaf compiler guidance](https://docs.overleaf.com/getting-started/compiling-your-project/choosing-a-latex-compiler) | Per-project compiler selection. | LuaLaTeX setup instructions and source ZIP. |

## What was learned from the reference project

The [reference Groningen template](https://github.com/vcaldas/Groningen-thesis-template/tree/33bf34609b480d39faeb42890b6c119b92c8f797) illustrates modular chapters and supporting matter. Its inspected README and Makefile use different compiler instructions; its class identifies a 2013 TU Delft origin and uses numbered scientific citations. A repository-level licence was not found in the inspected tree. See [provenance](provenance.md) for the resulting independent-implementation decision.

## Evidence boundaries

The source register identifies exactly what was checked in each demonstration authority. Identity, bibliographic accuracy and an inspected paragraph do not establish current legal validity, subsequent treatment or support for a new thesis claim. No public claim of university approval, comprehensive legal verification or universal citation compliance follows from a successful build.
