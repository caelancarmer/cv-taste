"""Exercise real PDF failure cases and the bundled rendering contract."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import pymupdf


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('cv_render', ROOT / 'scripts/render.py')
RENDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RENDER)

if not shutil.which('pdflatex'):
    TEX_SKIP_REASON = 'pdfLaTeX (pdflatex) is missing'
elif not shutil.which('kpsewhich'):
    TEX_SKIP_REASON = 'kpsewhich is missing; cannot locate lmodern.sty'
else:
    located = subprocess.run(['kpsewhich', 'lmodern.sty'], capture_output=True,
                             text=True, timeout=10)
    TEX_SKIP_REASON = '' if located.returncode == 0 and located.stdout.strip() else 'lmodern.sty is missing'


def run_cli(source, output):
    return subprocess.run(
        [sys.executable, str(ROOT / 'scripts/render.py'), str(source), '--output-dir', str(output)],
        capture_output=True, text=True, timeout=90)


class PDFValidationTests(unittest.TestCase):
    def test_reference_passes(self):
        with pymupdf.open(ROOT / 'assets/reference.pdf') as doc:
            self.assertIn('LMRoman10-Regular', RENDER.validate_pdf(doc)['fonts'])
            self.assertIn('fictional', doc[0].get_text().lower())

    def test_extra_page_is_rejected(self):
        with pymupdf.open(ROOT / 'assets/reference.pdf') as doc:
            doc.new_page(width=595.276, height=841.890)
            with self.assertRaisesRegex(ValueError, 'Expected one page'):
                RENDER.validate_pdf(doc)

    def test_non_a4_is_rejected(self):
        with pymupdf.open() as doc:
            doc.new_page(width=612, height=792)
            with self.assertRaisesRegex(ValueError, 'Expected A4'):
                RENDER.validate_pdf(doc)

    def test_pdf_without_text_is_rejected(self):
        with pymupdf.open() as doc:
            doc.new_page(width=595.276, height=841.890)
            with self.assertRaisesRegex(ValueError, 'no extractable text'):
                RENDER.validate_pdf(doc)

    def test_substitute_font_is_rejected(self):
        with pymupdf.open() as doc:
            page = doc.new_page(width=595.276, height=841.890)
            page.insert_text((60, 100), 'Fictional sample text', fontname='helv')
            with self.assertRaisesRegex(ValueError, 'font substitution'):
                RENDER.validate_pdf(doc)

    def test_text_outside_safe_margin_is_rejected(self):
        with pymupdf.open(ROOT / 'assets/reference.pdf') as doc:
            doc[0].insert_text((20, 100), 'Outside margin')
            with self.assertRaisesRegex(ValueError, 'safe page bounds'):
                RENDER.validate_pdf(doc)

    def test_text_at_37_pt_is_rejected(self):
        with pymupdf.open(ROOT / 'assets/reference.pdf') as doc:
            doc[0].insert_text((37, 100), 'Outside left margin')
            with self.assertRaisesRegex(ValueError, 'safe page bounds'):
                RENDER.validate_pdf(doc)

    def test_text_within_25_pt_of_bottom_is_rejected(self):
        with pymupdf.open(ROOT / 'assets/reference.pdf') as doc:
            doc[0].insert_text((60, doc[0].rect.height - 25), 'Near bottom edge')
            with self.assertRaisesRegex(ValueError, 'safe page bounds'):
                RENDER.validate_pdf(doc)

    def test_altered_body_font_size_is_rejected(self):
        with pymupdf.open(ROOT / 'assets/reference.pdf') as reference:
            font = next(f for f in reference[0].get_fonts() if f[3].endswith('LMRoman10-Regular'))
            buffer = reference.extract_font(font[0])[3]
        for size in (8, 12):
            with self.subTest(fontsize=size), pymupdf.open() as doc:
                page = doc.new_page(width=595.276, height=841.890)
                page.insert_font(fontname='Body', fontbuffer=buffer)
                page.insert_text((60, 100), 'Fictional sample text', fontname='Body', fontsize=size)
                with self.assertRaisesRegex(ValueError, 'Body font size'):
                    RENDER.validate_pdf(doc)

    def test_non_kebab_source_name_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'Bad_source.tex'
            source.write_text('Not reached')
            result = run_cli(source, directory)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('lowercase kebab-case', result.stderr)

    def test_nonexistent_source_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            result = run_cli(Path(directory) / 'missing-source.tex', directory)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('Source does not exist', result.stderr)

    @unittest.skipUnless(not TEX_SKIP_REASON, TEX_SKIP_REASON)
    def test_compile_error_includes_cause(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'bad-source.tex'
            source.write_text(r'\documentclass{article}\begin{document}\undefinedcmd\end{document}')
            result = run_cli(source, directory)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('Undefined control sequence', result.stderr)
            self.assertIn('Undefined control sequence', (Path(directory) / 'build-output.txt').read_text())

    @unittest.skipUnless(not TEX_SKIP_REASON, TEX_SKIP_REASON)
    def test_reference_renders_through_cli(self):
        with tempfile.TemporaryDirectory() as output:
            result = run_cli(ROOT / 'assets/reference.tex', output)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            report = json.loads((Path(output) / 'validation.json').read_text())
            self.assertEqual(report['pages'], 1)
            self.assertGreater(report['text_chars'], 0)
            self.assertEqual(set(report), {'pages', 'text_chars', 'fonts',
                                           'minimum_margins_pt', 'pdf_bytes'})
            self.assertTrue((Path(output) / 'cv-preview.png').is_file())

    @unittest.skipUnless(not TEX_SKIP_REASON, TEX_SKIP_REASON)
    def test_committed_reference_text_is_current(self):
        with tempfile.TemporaryDirectory() as output:
            result = run_cli(ROOT / 'assets/reference.tex', output)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            with pymupdf.open(Path(output) / 'reference.pdf') as rendered, \
                    pymupdf.open(ROOT / 'assets/reference.pdf') as committed:
                self.assertEqual(rendered[0].get_text(sort=True), committed[0].get_text(sort=True))


if __name__ == '__main__':
    unittest.main()
