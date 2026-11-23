# Dependencies

Moved verbatim from `README.md` during the README trim to 100 lines or fewer; the README now links here.

## Dependencies

Use Python 3.10 or later and pdfLaTeX. The layout requires `lmodern`, `fontenc`, `inputenc`, `geometry`, `enumitem`, `microtype`, and `hyperref`. PyMuPDF provides PDF inspection and preview generation.

This release was validated on Linux. The following installation commands target Debian or Ubuntu:

```bash
sudo apt-get install texlive-latex-base texlive-latex-recommended lmodern
```

Install the Python dependency in your chosen environment:

```bash
python -m pip install -r requirements.txt
```

No web framework, database, JavaScript runtime, or Python HTTP package is required.
