# Contributing to LexThesis

Thank you for helping make legal research easier to write and verify.

Good contributions are concrete: a reproducible layout defect, a verified institutional requirement, a citation edge case, a clearer instruction or an accessibility improvement. Explain who benefits and provide the smallest example that demonstrates the issue.

## Before a pull request

- Use a branch and keep changes focused.
- Run `python3 scripts/check.py` and `python3 -m unittest discover -s tests -v`.
- For typesetting changes, compile the affected variants and inspect the PDF.
- Update the relevant documentation and changelog.
- Confirm that all contributed content may be redistributed under the project licence.

## Institutional and citation changes

Link to the issuing institution or citation manual. Give the exact edition, date, section or page, and distinguish a requirement from advice. Explain what the implementation supports and what still needs author review. A new style claim needs regression examples for the source types it covers.

## Research integrity and privacy

Use public or clearly synthetic demonstration data. Do not attach confidential thesis chapters, participant data, unpublished co-author material or credentials. A public bug report is visible to others. Report a vulnerability through the route in SECURITY.md.

## Collaboration

Discuss the argument or implementation respectfully. Correct errors openly and preserve the evidence behind corrections. Contributions by doctoral researchers, librarians, academics and technical users are welcome.
