# Provenance and reuse

## What inspired this project

This project was commissioned to create a reusable law PhD thesis template after studying [Victor Caldas's Groningen thesis template](https://github.com/vcaldas/Groningen-thesis-template/tree/master). The original demonstrates modular chapters, separate front matter and a propositions document. Its README attributes substantial influence to a TU Delft dissertation template.

The upstream repository was inspected on **8 November 2026** at commit **`33bf34609b480d39faeb42890b6c119b92c8f797`**. The inspection covered its README, Makefile, main document, document class, title source and complete repository tree. The GitHub metadata returned no repository-level licence, and the tree contained no licence-named file.

The new implementation and documentation are independently authored. No upstream class, bundled font, university logo, personal title page, thesis text or example publication was copied into this project. The historical template is acknowledged as an inspiration, not presented as an endorsement of this project.

## Design choices and evidence

| Design choice | Source or reason |
| --- | --- |
| Separate institutional profiles | Institutions prescribe different front matter, formats and counting rules. The generic profile remains adaptable. |
| Explicit Groningen print dimensions | October 2026 guidance specifies 170 × 240 mm as a standard while permitting alternatives. |
| Approved-title-PDF slot | Groningen requires approval of the student's actual title page. |
| Publication-based thesis example | Groningen's March 2026 Regulations recognise a coherent collection of academic publications. |
| Research-question and method prompts | Informed by LSE's public law research-proposal guidance and developed into original planning questions. |
| Claim, comparison and assistance logs | Original workflow aids for traceable research decisions. They do not certify the accuracy of entries. |

Source details and limitations are recorded in [the Groningen guide](groningen.md) and [the research-design guide](research-design.md).

## Template rights and thesis rights

The **MIT licence** in the repository governs the original software, templates and documentation distributed under that licence. Retain its notice when redistributing substantial portions of those materials.

**Your thesis remains your work.** Using this template does not require you to publish your thesis under MIT or to release your research data. Choose the copyright notice, publication terms and deposit licence that apply to your work and institutional obligations. Rights in co-authored articles, publisher material, images, datasets and other third-party content must be considered separately.

TeX packages, fonts and other external dependencies retain their own licences. Their availability in a TeX distribution does not transfer their authorship or rights to this project. University names identify the scope of a profile; they do not imply sponsorship, certification or permission to use institutional marks.

## Demonstration content

The CSV files in `examples/` contain explicitly labelled workflow demonstrations. They do not assert completed fieldwork, ethics approval, individual university approval or verified findings. Replace them in your own project. The thesis examples are teaching material, not a submission on behalf of a real candidate.

The repository licence does not automatically apply to third-party legal authorities identified by citation or link. Users should consult the source and any applicable reuse terms.

## Research record

All sources below were consulted on **8 November 2026**:

- [Upstream README](https://github.com/vcaldas/Groningen-thesis-template/blob/33bf34609b480d39faeb42890b6c119b92c8f797/README.txt) and [upstream class](https://github.com/vcaldas/Groningen-thesis-template/blob/33bf34609b480d39faeb42890b6c119b92c8f797/dissertation.cls).
- [University of Groningen PhD Regulations](https://www.rug.nl/about-ug/organization/rules-and-regulations/onderzoek/phd-regulations-ug-2026.pdf), **Version March 2026**.
- [University of Groningen thesis instructions](https://www.rug.nl/education/phd-programmes/promotieregeling/thesis-instructions-for-phd-candidates.pdf), **Version 4.0, October 2026**.
- [University of Groningen title-page guidance](https://www.rug.nl/education/phd-programmes/promotieregeling/?lang=en).
- [University of Groningen Library publishing guidance](https://www.rug.nl/library/publish/theses-dissertations/faq?lang=en).
- [LSE Law PhD FAQ](https://www.lse.ac.uk/law/study/phd/faqs), research-proposal guidance.
- [Oxford Research Degrees in Law](https://examregs.admin.ox.ac.uk/Regulation?code=rdegrinlaw), page displaying **2025/26**, section 5.

A source's inclusion records what informed a design decision. It does not mean that every requirement in that source has been implemented or automatically checked. Consult the current primary source before submission.
