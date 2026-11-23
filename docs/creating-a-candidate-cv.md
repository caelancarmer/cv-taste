# Create a candidate CV

Moved verbatim from `README.md` during the README trim to 100 lines or fewer; the README now links here. The render command it mentions lives in [rendering.md](rendering.md).

## Create a candidate CV

The source filename should use lowercase kebab-case, for example `candidate-cv-type-1.tex`.

Use `assets/style.tex` as the first input. It contains the document class and full preamble; do not add another `\documentclass`. Resolve its path relative to the candidate source directory, or use an absolute path in that local file.

```tex
\input{/path/to/cv-taste/assets/style.tex}
\hypersetup{pdftitle={Candidate CV},pdfauthor={Candidate Name}}
\begin{document}
\begin{center}
{\Huge\bfseries Candidate Name}\par
City, Region\enspace$\|$\enspace candidate@example.com
\end{center}
\cvsection{Profile}
\begin{cvbody}
Write a concise, factual profile tailored to the target role.
\end{cvbody}
\end{document}
```

Replace the placeholder facts and metadata before delivery. Use the fictional reference for layout and section structure. Use the render command above with the absolute candidate source path and an output directory outside this repository.
