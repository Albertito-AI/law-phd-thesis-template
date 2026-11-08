# Security and thesis confidentiality

## Supported version and reporting

Security fixes apply to the current release on `main`. Report a reproducible
tooling vulnerability through the repository's **Security → Report a
vulnerability** facility when available. If private reporting is unavailable,
open a minimal issue asking for a private contact route. Do not disclose an
exploit, private thesis text or credentials in that issue.

## What the template does

The local Python tools use the Python standard library, do not contact the
network and invoke build tools with argument lists. Builds use
`-no-shell-escape`. The source exporter includes only documented source paths,
rejects symlinks, and excludes Git history, designated private folders and build
outputs. It includes PDF figures under `assets/` and the optional
`frontmatter/approved-title.pdf`. Files in approved source paths can still
contain personal or restricted material; review their contents before sharing.
The Actions workflow grants read-only repository access, does not persist
checkout credentials, and has no need for repository secrets. External Actions
are pinned to verified full commit identifiers and receive Dependabot updates.

These measures reduce exposure. They do not make arbitrary TeX, Lua, Perl or
Python safe to execute. A `.tex`, `.sty`, `.cls` or `latexmkrc` file is executable
input. Inspect unfamiliar templates and pull requests before building them.
Use an isolated, disposable environment for untrusted sources; do not expose
credentials or private research to it. Disabling shell escape is not a sandbox.

## Working on an actual thesis

Create a **private** repository or an institution-approved private workspace
before adding unpublished chapters, interview data, consent records or
restricted documents. Git ignore rules do not remove files already committed
and do not grant permission to share research data. Review the selected files
and the ZIP manifest before uploading an adapted project to Overleaf or another
service. Removing author metadata is not a guarantee of anonymity: inspect the
PDF, acknowledgements, self-citations and filenames.

CI in this public template builds demonstration material. It uploads sample
PDFs only on a trusted push to this repository or a manual run, never on a pull
request. Users who copy the workflow into a thesis project should review
repository visibility, Actions log access and artifact access first. No
workflow automatically deploys or publishes a thesis.

## Owner settings

Repository owners may enable private vulnerability reporting, branch rules,
required review and available secret-scanning protections in GitHub settings.
Their presence cannot be established by a file in this template. Inspect the
actual settings rather than treating this document as proof they are enabled.

## Boundaries of the audit

`scripts/check.py` checks literal source keys, register consistency, references,
placeholder markers and selected LaTeX log problems. It does not check a
source's legal force, subsequent treatment, quoted wording, exact pinpoint,
research consent, confidentiality or academic approval. A working URL is not
evidence that an authority supports a proposition.

## Maintainer references

- [GitHub: secure use of Actions](https://docs.github.com/en/actions/reference/security/secure-use)
- [GitHub: workflow token permissions](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#permissions)
- [GitHub: workflow dependency lockfiles](https://docs.github.com/en/actions/concepts/security/workflow-dependency-lockfiles)
- [Overleaf: TeX engine options](https://www.overleaf.com/learn/latex/TeX_engine_command_line_options_for_pdfTeX%2C_XeTeX_and_LuaTeX)

SHA pins are the present dependency mechanism. A generated GitHub Actions
lockfile can additionally lock transitive action dependencies when maintainers
adopt that feature. No such lockfile is claimed by this release.
