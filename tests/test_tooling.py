"""Regression tests for errors that can silently damage a thesis handoff."""

from __future__ import annotations

import csv
from datetime import date, timedelta
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

from scripts import build, check, package
from scripts._common import SourceSyntaxError, checked_output_dir, executable_tex, literal_commands


DECLARATION = r"\DeclareLawSource{case-one}{case}{United Kingdom}{Example}{\emph{Example} [2020] UKSC 1}{\emph{Example}}{Example [2020] UKSC 1}{}"


class ProjectFixture(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "references").mkdir()
        (self.root / "references" / "authorities.tex").write_text(DECLARATION + "\n", encoding="utf-8")
        (self.root / "main.tex").write_text(
            r"\input{references/authorities}" + "\n" + r"Text.\lawcite[{[32]}]{case-one}" + "\n",
            encoding="utf-8",
        )
        self.rows = [["case-one", "case", "United Kingdom", "https://example.org/judgment",
                      "judgment as handed down", "2020-01-01", "test fixture, not a verified authority"]]
        self.write_register()

    def write_register(self):
        with (self.root / "references" / "source-register.csv").open("w", newline="", encoding="utf-8") as stream:
            writer = csv.writer(stream)
            writer.writerow(check.CSV_FIELDS)
            writer.writerows(self.rows)

    def codes(self, submission=False):
        return {issue.code for issue in check.audit_sources(self.root, submission=submission)}


class SourceAuditTests(ProjectFixture):
    def test_complete_consistent_source_passes(self):
        self.assertEqual(check.audit_sources(self.root), [])

    def test_duplicate_keys_are_rejected(self):
        with (self.root / "references" / "authorities.tex").open("a", encoding="utf-8") as stream:
            stream.write(DECLARATION)
        self.assertIn("duplicate-key", self.codes())

    def test_unknown_citation_is_not_silently_accepted(self):
        (self.root / "main.tex").write_text(r"\lawcite{invented-case}", encoding="utf-8")
        self.assertIn("unknown-source", self.codes())

    def test_literal_code_and_comments_are_not_citations(self):
        (self.root / "main.tex").write_text(
            "% \\lawcite{unknown}\n" + r"\begin{verbatim}\lawcite{unknown}\end{verbatim}" + "\n"
            + r"\verb|\lawcite{unknown}|", encoding="utf-8")
        self.assertNotIn("unknown-source", self.codes())

    def test_source_needs_a_verification_row(self):
        self.rows = []
        self.write_register()
        self.assertIn("missing-verification", self.codes())

    def test_mismatched_jurisdiction_fails(self):
        self.rows[0][2] = "Australia"
        self.write_register()
        self.assertIn("register-mismatch", self.codes())

    def test_duplicate_register_row_fails(self):
        self.rows.append(self.rows[0].copy())
        self.write_register()
        self.assertIn("duplicate-register-key", self.codes())

    def test_non_http_url_and_embedded_credentials_fail(self):
        for url in ("javascript:alert(1)", "file:///tmp/private", "https://user:password@example.org"):
            with self.subTest(url=url):
                self.rows[0][3] = url
                self.write_register()
                self.assertIn("invalid-url", self.codes())

    def test_future_verification_date_fails(self):
        self.rows[0][5] = (date.today() + timedelta(days=2)).isoformat()
        self.write_register()
        self.assertIn("invalid-date", self.codes())

    def test_ragged_csv_row_fails(self):
        self.rows[0].append("unexpected field")
        self.write_register()
        self.assertIn("register-row", self.codes())

    def test_truncated_declaration_fails(self):
        (self.root / "references" / "authorities.tex").write_text(DECLARATION[:-2], encoding="utf-8")
        self.assertIn("registry-syntax", self.codes())

    def test_extra_declaration_argument_fails(self):
        (self.root / "references" / "authorities.tex").write_text(DECLARATION + "{unexpected}", encoding="utf-8")
        self.assertIn("registry-syntax", self.codes())

    def test_placeholder_warns_normally_and_fails_submission(self):
        (self.root / "main.tex").write_text("Your Name\nTODO: verify the quotation.\n", encoding="utf-8")
        normal = check.audit_sources(self.root)
        strict = check.audit_sources(self.root, submission=True)
        self.assertTrue(any(issue.code == "placeholder" and issue.level == "warning" for issue in normal))
        self.assertTrue(any(issue.code == "placeholder" and issue.level == "error" for issue in strict))
        self.assertFalse(any(issue.level == "error" for issue in normal))

    def test_instruction_macros_and_demo_metadata_fail_submission(self):
        (self.root / "main.tex").write_text(r"\LawPrompt{Write your findings.}\LawTODO{Verify this.}", encoding="utf-8")
        (self.root / "metadata.tex").write_text("LEXTHESIS / working EXAMPLE", encoding="utf-8")
        issues = check.audit_sources(self.root, submission=True)
        self.assertTrue(any(issue.code == "placeholder" and issue.level == "error" for issue in issues))
        self.assertTrue(any(issue.code == "demonstration-metadata" and issue.level == "error" for issue in issues))

    def test_rejected_url_does_not_print_credentials(self):
        self.rows[0][3] = "https://researcher:do-not-print-this-password@example.org"
        self.write_register()
        findings = "\n".join(map(str, check.audit_sources(self.root)))
        self.assertIn("invalid-url", findings)
        self.assertNotIn("do-not-print-this-password", findings)
        self.assertNotIn("researcher:", findings)

    def test_audit_never_promotes_or_rewrites_verification(self):
        self.rows[0][6] = "UNVERIFIED: pending verification by the author"
        self.write_register()
        register = self.root / "references" / "source-register.csv"
        before = register.read_bytes()
        findings = check.audit_sources(self.root)
        self.assertTrue(any(issue.code == "pending-verification" and issue.level == "warning" for issue in findings))
        self.assertEqual(before, register.read_bytes())
        strict_findings = check.audit_sources(self.root, submission=True)
        self.assertTrue(any(issue.code == "pending-verification" and issue.level == "error" for issue in strict_findings))
        self.assertEqual(before, register.read_bytes())

    def test_missing_input_and_external_input_fail(self):
        (self.root / "main.tex").write_text(r"\input{missing}" + "\n" + r"\input{../outside}", encoding="utf-8")
        self.assertIn("missing-input", self.codes())
        self.assertIn("external-input", self.codes())

    def test_missing_label_and_duplicate_label_fail(self):
        (self.root / "main.tex").write_text(
            r"\label{same}\label{same}\LawChapterRef{missing}", encoding="utf-8")
        self.assertIn("duplicate-label", self.codes())
        self.assertIn("unknown-label", self.codes())

    def test_private_research_is_not_audited(self):
        (self.root / "private").mkdir()
        (self.root / "private" / "notes.tex").write_text(r"\lawcite{unknown}\input{missing}", encoding="utf-8")
        self.assertEqual(check.audit_sources(self.root), [])


class ParserTests(unittest.TestCase):
    def test_nested_braces_escaped_percent_and_pinpoint_brackets(self):
        text = executable_tex(r"\DeclareLawSource{k}{case}{UK}{A}{\emph{A \{B\}} 50\%}{A}{A}{}")
        parsed = list(literal_commands(text, ("DeclareLawSource",), arguments=8))
        self.assertEqual(parsed[0][1][4], r"\emph{A \{B\}} 50\%")
        cited = list(literal_commands(r"\lawcite[{[32]--[35]}]{k}", ("lawcite",), optional=True))
        self.assertEqual(cited[0][1], ("k",))

    def test_unclosed_optional_argument_fails(self):
        with self.assertRaises(SourceSyntaxError):
            list(literal_commands(r"\lawcite[[32]{k}", ("lawcite",), optional=True))


class LogTests(unittest.TestCase):
    def test_log_checks_real_failure_modes(self):
        with tempfile.TemporaryDirectory() as temporary:
            log = Path(temporary) / "main.log"
            log.write_text(
                "LaTeX Warning: Reference `ch:lost' on page 3 undefined on input line 42.\n"
                "Missing character: There is no 中 in font LatinModernRoman!\n"
                "LaTeX Warning: Label(s) may have changed. Rerun to get cross-references right.\n"
                "Output written on main.pdf (4 pages).\n", encoding="utf-8")
            codes = {issue.code for issue in check.audit_log(log)}
            self.assertTrue({"undefined-reference", "missing-glyph", "rerun-required"} <= codes)

    def test_successful_log_passes_and_incomplete_log_fails(self):
        with tempfile.TemporaryDirectory() as temporary:
            log = Path(temporary) / "main.log"
            log.write_text("Output written on main.pdf (4 pages).\n", encoding="utf-8")
            self.assertEqual(check.audit_log(log), [])
            log.write_text("Starting a build...\n", encoding="utf-8")
            self.assertIn("no-pdf-output", {issue.code for issue in check.audit_log(log)})


class PackageTests(ProjectFixture):
    def test_no_dot_overleaf_config_is_included(self):
        (self.root / "latexmkrc").write_text("$pdf_mode = 4;\n", encoding="utf-8")
        (self.root / ".latexmkrc").write_text("legacy config should not be exported", encoding="utf-8")
        output = self.root / "dist" / "template.zip"
        package.create_package(self.root, output)
        with zipfile.ZipFile(output) as archive:
            self.assertIn("latexmkrc", archive.namelist())
            self.assertNotIn(".latexmkrc", archive.namelist())

    def test_approved_title_and_source_figures_survive_export(self):
        fixture = b"%PDF-1.4\nSynthetic packaging fixture, not a rendered document.\n"
        for relative in ("frontmatter/approved-title.pdf", "assets/figures/diagram.pdf", "examples/generated.pdf",
                         "build/main.pdf", "main.pdf", "assets/private/consent.pdf"):
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(fixture)
        output = self.root / "dist" / "template.zip"
        package.create_package(self.root, output)
        with zipfile.ZipFile(output) as archive:
            for relative in ("frontmatter/approved-title.pdf", "assets/figures/diagram.pdf"):
                self.assertEqual(archive.read(relative), fixture)
            for relative in ("examples/generated.pdf", "build/main.pdf", "main.pdf", "assets/private/consent.pdf"):
                self.assertNotIn(relative, archive.namelist())

    def test_export_is_deterministic_and_manifest_matches_bytes(self):
        first = self.root / "dist" / "one.zip"
        second = self.root / "dist" / "two.zip"
        count, digest = package.create_package(self.root, first)
        second_count, second_digest = package.create_package(self.root, second)
        self.assertEqual((count, digest), (second_count, second_digest))
        self.assertEqual(first.read_bytes(), second.read_bytes())
        with zipfile.ZipFile(first) as archive:
            manifest = json.loads(archive.read("MANIFEST.json"))
            self.assertIn("main.tex", manifest["files"])
            for name, expected in manifest["files"].items():
                self.assertEqual(hashlib.sha256(archive.read(name)).hexdigest(), expected)

    def test_private_files_git_history_and_outputs_are_excluded(self):
        for directory in ("private", ".git", ".github", "build", "references/private"):
            path = self.root / directory
            path.mkdir(parents=True, exist_ok=True)
            (path / "secret.tex").write_text("private", encoding="utf-8")
        (self.root / "private.tex").write_text("private", encoding="utf-8")
        archive_path = self.root / "dist" / "template.zip"
        package.create_package(self.root, archive_path)
        with zipfile.ZipFile(archive_path) as archive:
            self.assertFalse(any("secret" in name or "private" in name or name.startswith(".") for name in archive.namelist()))

    def test_symlink_cannot_smuggle_external_content_into_export(self):
        link = self.root / "references" / "external.tex"
        try:
            link.symlink_to(self.root / "main.tex")
        except OSError:
            self.skipTest("Symlinks are unavailable on this operating system.")
        with self.assertRaisesRegex(ValueError, "symlink"):
            package.create_package(self.root, self.root / "dist" / "template.zip")

    def test_missing_main_file_is_rejected(self):
        (self.root / "main.tex").unlink()
        with self.assertRaisesRegex(ValueError, "main.tex"):
            package.create_package(self.root, self.root / "dist" / "template.zip")

    def test_source_file_cannot_be_overwritten_as_package_output(self):
        source = self.root / "main.tex"
        before = source.read_bytes()
        with self.assertRaisesRegex(ValueError, ".zip"):
            package.create_package(self.root, source)
        self.assertEqual(source.read_bytes(), before)


class BuildBoundaryTests(unittest.TestCase):
    def test_nonempty_authority_index_requires_processed_table(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            for category in ("cases", "legislation", "treaties"):
                (output / f"main-{category}.idx").write_text("", encoding="utf-8")
            index = output / "main-cases.idx"
            index.write_text(r"\indexentry{Test}{1}" + "\n", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "not processed"):
                build.verify_authority_tables(output, "main")
            index.with_suffix(".ind").write_text(r"\begin{theindex}\item Test, 1\end{theindex}", encoding="utf-8")
            build.verify_authority_tables(output, "main")

    def test_propositions_do_not_require_authority_tables(self):
        with tempfile.TemporaryDirectory() as temporary:
            build.verify_authority_tables(Path(temporary), "propositions")

    def test_unknown_entrypoint_cannot_escape_build_directory(self):
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaises(ValueError):
                checked_output_dir(Path(temporary), "../../outside")

    def test_symlinked_build_directory_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "elsewhere").mkdir()
            try:
                (root / "build").symlink_to(root / "elsewhere", target_is_directory=True)
            except OSError:
                self.skipTest("Symlinks are unavailable on this operating system.")
            with self.assertRaisesRegex(ValueError, "symlink"):
                checked_output_dir(root, "main")

    def test_cli_rejects_shell_text_before_running_tex(self):
        root = Path(__file__).resolve().parents[1]
        result = subprocess.run([sys.executable, str(root / "scripts" / "build.py"), "main;touch attack"],
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("invalid choice", result.stderr)


if __name__ == "__main__":
    unittest.main()
