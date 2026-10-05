---
name: cv-taste
description: Create or tailor a CV or resume using a minimal Latin Modern Roman design, role-specific evidence, concise writing, lowercase kebab-case filenames, and the requested delivery channel.
---

# CV Taste

## Activation and scope

Apply this skill when asked to create or tailor a CV or resume using cv-taste. Read the current request, job description, and supplied candidate facts. Preserve established preferences available in the conversation; do not infer a real biography from the bundled reference.

Current instructions take precedence. If the user requests a discussion first, keep the draft in chat until file creation is authorized. Continue work already authorized without redundant confirmation. Submitting an application or contacting a recruiter requires explicit instruction.

This package defines presentation and workflow. It contains no candidate profile, account identifiers, private workspace locations, or delivery credentials. The reference candidate and all example achievements are fictional.

## Reference and layout

- Visual reference: `assets/reference.pdf` and `assets/reference-preview.png`.
- Fictional source: `assets/reference.tex`.
- Shared preamble and macros: `assets/style.tex`.
- Renderer: `scripts/render.py`.

Inspect the reference before the first render in a new environment. Use it for typography, spacing, and hierarchy. Replace all sample facts, contact details, dates, results, and PDF metadata in a real candidate document.

## Fixed visual design

Use the actual Latin Modern Roman faces rather than a substitute serif.

- Name: `LMRoman12-Bold`, TeX `\Huge`, approximately 24.787 PDF pt.
- Body and contacts: `LMRoman10-Regular`, TeX 10 pt, approximately 9.963 PDF pt.
- Emphasis: `LMRoman10-Bold`; supporting metadata: `LMRoman10-Italic`.
- Section headings: `LMRomanCaps10-Regular`, TeX 12 pt, approximately 11.955 PDF pt.
- Contact separators may use Latin Modern math symbols.
- A4 portrait, one page by default, black text on white.
- Margins: left/right 13.97 mm, top 9.8 mm, bottom 12 mm.
- Center the name and contact line; use thin 0.4 pt section rules.
- Section spacing: 6.1 pt before, 1 pt before the rule, 4 pt after it.
- Content indent: 10.8 pt left and 4.7 pt right.
- Bullet layout: 24.8 pt left margin within content, 5 pt label separation, 1.4 pt item separation, 2 pt top separation.
- Dates or durations align to the right of entry titles; supporting descriptions use italics.
- Omit portraits, page numbers, colors, charts, and sidebars unless requested.
- Disable font expansion, protrusion, and automatic word hyphenation.
- Keep text selectable and Unicode extraction usable, including ligatures.

Use the shared macros instead of maintaining a second layout implementation. Content length and role-specific section order may change. Preserve required approved content; never silently remove a competency or achievement or reduce body font size to force a page fit. Discuss an additional page when necessary.

## Tailoring workflow

1. Read the actual job description. Identify essential tasks, requirements, vocabulary, and the intended audience.
2. Review the candidate facts supplied for this application. Distinguish employment, independent projects, simulations, research, learning, and AI-assisted work.
3. Select about five competency groups relevant to the role. Make the strongest supported evidence easy to find.
4. Use compact action–method–result bullets. Keep quantified results tied to their actual measurement context and baseline.
5. Match claims to evidence. Do not invent employers, employment duration, degrees, credentials, client results, or production outcomes. An unfinished certification belongs under development, not earned qualifications.
6. Show soft skills through examples: direction and coordination for leadership, review steps for accuracy, delivery for reliability, and measurable process improvements for efficiency.
7. Use the language requested or appropriate to the employer. Repository documentation being English does not require every candidate CV to be English.
8. Remove irrelevant content while preserving explicitly approved requirements. Ask only for missing facts that materially affect the result.

A useful default order is Profile → Core Competencies → Relevant Projects → Experience → Education → Additional Skills. Adapt it to the candidate and role.

For accounting or finance, possible groups include Accuracy & Reconciliation; Closing & Reporting; Cash & Working Capital; Tax Documentation & Compliance; and Spreadsheets, Systems & Analysis. Select and label them according to the actual role and demonstrated capabilities. Do not carry this accounting list into unrelated roles automatically.

## Naming and candidate data

Use the current naming preference. A generic convention is folder **Candidate Name cv type 1** and file `candidate-name-cv-type-1.pdf`. Filenames for source and archives also use lowercase kebab-case.

Retain the type number for revisions of the same variant. Check existing variants before assigning another number. Do not overwrite an approved variant silently.

Store real candidate sources, contact information, employer documents, outputs, delivery settings, credentials, and signed upload URLs outside this reusable repository. Do not embed personal details in this skill, examples, tests, logs, commit messages, or release assets. Keep reference assets fictional and check PDF metadata, previews, and tracked files before a release.

## Rendering and review

Follow [README.md](README.md#dependencies) for dependencies and render/test commands. Use `assets/style.tex` as the first input of a new source; it includes the document class and preamble.

1. Create a candidate-specific `.tex` file using the shared layout.
2. Render the candidate source with the command documented in README.md.
3. Inspect the preview for hierarchy, line breaks, spacing, alignment, and legibility at normal size.
4. Read the extracted text and check names, qualifications, figures, dates, and required sections against the approved draft.
5. Review the report and fix compilation issues, unsupported characters, font substitution, clipping, or excess pages.
6. Confirm the PDF metadata describes the actual candidate rather than the reference.

Automated validation is evidence about the PDF format, not a substitute for visual and factual review. The renderer uses `-no-shell-escape`; that option does not make arbitrary TeX input a complete security sandbox.

## Delivery

Use the user's requested channel and existing authorization. Provide a stable final link when an external upload is requested.

### Optional Notion delivery

Use this workflow only when Notion is requested and its tools and an authorized destination are available. Discover current tool access and fetch the destination first. No workspace destination is bundled in the skill.

1. Prepare a file upload with the chosen lowercase PDF filename and `application/pdf`.
2. Send exactly one multipart/form-data POST to the returned upload URL with every required header and the `file` field. Python standard-library `urllib` is sufficient; an extra HTTP dependency is not required.
3. Attach the completed upload through the folder tool or the response's suggested PDF Markdown.
4. Create a new native folder through the folder tool when needed. New folders cannot be created by inserting a `<folder>` Markdown block.
5. Add a stable destination link to an authorized index if requested.
6. After a transient error, fetch the destination before retrying to avoid duplicate uploads.
7. Verify the exact folder title and filename; return a stable page or folder URL, not an expiring signed file URL.

Preserve unrelated content. Never print credentials, authorization headers, or signed upload URLs; keep the configured proxy and certificate trust.

## Completion

The CV matches the target role and supplied facts, preserves the selected visual design and required content, passes PDF checks and visual review, has the requested filename and variant, and is delivered through the authorized channel.

A saved repository is available when an agent can access or install it. Do not claim that it automatically loads in every future session.
