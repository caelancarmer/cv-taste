# Render the reference

Moved verbatim from `README.md` during the README trim to 100 lines or fewer; the README now links here.

## Render the reference

Run from the repository root:

```bash
python scripts/render.py assets/reference.tex --output-dir /tmp/cv-taste-preview
```

The current renderer enforces the bundled one-page A4 Latin Modern design. Additional pages or different designs require corresponding renderer changes. Use trusted TeX sources; see the security note in `SKILL.md`.

The output directory receives the PDF, extracted text, preview PNG, validation JSON, and compiler files. Validation checks A4 page size, one page, allowed fonts, reference body font size, and text bounds. The report contains measured page count, text character count, fonts, minimum margins in points, and PDF byte size. Margins use font-height-normalized span boxes for consistent measurement across supported PyMuPDF versions; the top edge has the documented tolerance in `scripts/render.py`. See `SKILL.md` for review steps.

Run the renderer tests with:

```bash
python -m unittest discover -s tests -v
```
