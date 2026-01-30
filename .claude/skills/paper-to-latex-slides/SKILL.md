---
name: paper-to-latex-slides
description: Read PDF research papers and generate professional LaTeX Beamer slides. Use when a user wants to summarize a paper into a presentation format with options for a standard 15-slide deck or a comprehensive long-slide deck.
---

# Paper to LaTeX Slides

This skill automates the process of transforming a research paper (PDF) into a structured LaTeX Beamer presentation.

## Usage Guidelines

When triggered, follow these steps to generate the slides:

1.  **Analyze the Paper**: Read the PDF file to identify the core sections (Introduction, Background, Method, Results, Conclusion).
2.  **Determine Slide Count**:
    -   **Standard (15 slides)**: Follow the 15-slide distribution (Intro: 2, Background: 2, Method: 3, Results: 4, etc.).
    -   **Long Slides**: Create a slide for every section and subsection in the paper for maximum detail.
3.  **Generate LaTeX**:
    -   Use the template located at `templates/latex/main.tex`.
    -   Populate the `\title`, `\author`, and `\institute` fields.
    -   Organize content into `\section` blocks.
    -   Use `itemize` for key points and `columns` for side-by-side content.
4.  **Reference Workflow**: For detailed slide distribution and formatting rules, refer to `references/workflow.md`.

## Key Sections to Include
-   **Introduction**: Motivation and problem statement.
-   **Background**: Context and related work.
-   **Methodology**: Technical approach and implementation.
-   **Results**: Key findings, data, and performance.
-   **Conclusion**: Summary and future directions.

## Resources
-   `templates/latex/main.tex`: The base Beamer template.
-   `references/workflow.md`: Detailed generation logic and quality checklist.
