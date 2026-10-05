#!/usr/bin/env python3
"""Render and inspect a CV using the cv-taste design."""
import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys


MM_TO_PT = 72 / 25.4
LEFT_MARGIN_PT = RIGHT_MARGIN_PT = 13.97 * MM_TO_PT
TOP_MARGIN_PT = 9.8 * MM_TO_PT
BOTTOM_MARGIN_PT = 12 * MM_TO_PT
# Font span boxes extend above the TeX top margin; this covers supported MuPDF
# metrics (including the minimum version) and applies only to the top edge.
TOP_SPAN_TOLERANCE_PT = 3.0


def validate_pdf(doc):
    """Check the PDF format; factual and visual review remain separate."""
    import pymupdf

    if len(doc) != 1:
        raise ValueError(f'Expected one page, found {len(doc)}; revise content without shrinking body font')
    page = doc[0]
    if abs(page.rect.width - 595.276) > 1 or abs(page.rect.height - 841.890) > 1:
        raise ValueError('Expected A4 portrait')
    # Normalize font-height boxes across MuPDF versions; preserve caller settings.
    previous = pymupdf.TOOLS.set_small_glyph_heights()
    pymupdf.TOOLS.set_small_glyph_heights(True)
    try:
        blocks = page.get_text('dict')['blocks']
    finally:
        pymupdf.TOOLS.set_small_glyph_heights(previous)
    spans = [s for b in blocks if 'lines' in b
             for line in b['lines'] for s in line['spans'] if s['text'].strip()]
    if not spans:
        raise ValueError('PDF has no extractable text')
    margins = {
        'left': min(s['bbox'][0] for s in spans),
        'right': min(page.rect.width - s['bbox'][2] for s in spans),
        'top': min(s['bbox'][1] for s in spans),
        'bottom': min(page.rect.height - s['bbox'][3] for s in spans),
    }
    limits = {'left': LEFT_MARGIN_PT, 'right': RIGHT_MARGIN_PT,
              'top': TOP_MARGIN_PT - TOP_SPAN_TOLERANCE_PT,
              'bottom': BOTTOM_MARGIN_PT}
    # Round for PDF coordinate noise, without relaxing the design margins.
    if any(round(margins[side], 3) < round(limit, 3) for side, limit in limits.items()):
        raise ValueError('Text is outside the design safe page bounds: ' +
                         ', '.join(f'{side}={value:.3f} pt' for side, value in margins.items()))
    for span in spans:
        if span['font'] in {'LMRoman10-Regular', 'LMRoman10-Italic', 'LMRoman10-Bold'}:
            if abs(span['size'] - 9.963) > 0.05:
                raise ValueError('Body font size does not match the reference')
    allowed = {'LMRoman12-Bold', 'LMRoman10-Regular', 'LMRoman10-Bold',
               'LMRoman10-Italic', 'LMRomanCaps10-Regular', 'LMMathSymbols10-Regular',
               'LMMathSymbols6-Regular'}
    fonts = {re.sub(r'^[A-Z]{6}\+', '', f[3]) for f in page.get_fonts()}
    if not fonts.issubset(allowed):
        raise ValueError('Unexpected font substitution: ' + ', '.join(sorted(fonts - allowed)))
    return {'pages': len(doc), 'text_chars': len(page.get_text(sort=True)),
            'fonts': sorted(fonts), 'minimum_margins_pt': margins}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    source = args.source.resolve()
    output = args.output_dir.resolve()
    if not source.is_file():
        parser.error('Source does not exist')
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*\.tex', source.name):
        parser.error('Source filename must use lowercase kebab-case')
    if not shutil.which('pdflatex'):
        parser.error('pdfLaTeX is missing; install the design dependencies before rendering')
    try:
        import pymupdf
    except ImportError:
        parser.error('PyMuPDF is missing; install it before rendering and inspection')
    output.mkdir(parents=True, exist_ok=True)
    command = ['pdflatex', '-interaction=nonstopmode', '-halt-on-error',
               '-no-shell-escape', f'-output-directory={output}', str(source)]
    for _ in range(2):
        try:
            result = subprocess.run(command, cwd=source.parent, capture_output=True,
                                    text=True, timeout=60)
        except subprocess.TimeoutExpired:
            sys.exit('Compilation exceeded 60 seconds; inspect the TeX source')
        (output / 'build-output.txt').write_text(result.stdout + result.stderr)
        if result.returncode:
            lines = (result.stdout + result.stderr).splitlines()
            first = next((i for i, line in enumerate(lines) if line.startswith('!')), None)
            cause = '\n'.join(lines[first:first + 3] if first is not None else lines[-3:])
            sys.exit(f'Compilation failed (exit {result.returncode}):\n{cause}\nSee build-output.txt')
        log = (output / (source.stem + '.log')).read_text(errors='replace')
        if 'Rerun to get' not in log:
            break
    issues = re.findall(r'^.*(?:Overfull|Missing character|Undefined control sequence).*$',
                        log, re.MULTILINE)
    if issues:
        sys.exit('PDF has a compiler layout/text issue:\n' + '\n'.join(issues[:3]))
    pdf = output / (source.stem + '.pdf')
    doc = pymupdf.open(pdf)
    try:
        report = validate_pdf(doc)
    except ValueError as error:
        sys.exit(str(error))
    page = doc[0]
    text = page.get_text(sort=True)
    (output / (source.stem + '.txt')).write_text(text)
    page.get_pixmap(matrix=pymupdf.Matrix(1.7, 1.7)).save(output / 'cv-preview.png')
    report['pdf_bytes'] = pdf.stat().st_size
    (output / 'validation.json').write_text(json.dumps(report, indent=2))
    print(json.dumps({'pdf': str(pdf), 'preview': str(output / 'cv-preview.png'),
                      'validation': str(output / 'validation.json'),
                      'reminder': 'Visual and factual review is required'}, indent=2))


if __name__ == '__main__':
    main()
