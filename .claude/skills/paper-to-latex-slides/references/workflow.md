# LaTeX Slide Generation Workflow

This reference describes the detailed workflow for converting a PDF paper into LaTeX Beamer slides.

## 1. Content Extraction
- Read the PDF paper using the `file` tool.
- Identify key sections: Title, Authors, Abstract, Introduction, Background/Related Work, Methodology, Results, and Conclusion.
- Extract key points, figures (if possible), and tables.

## 2. Slide Structure Planning
Based on the user's choice:

### Option A: 15 Slides (Standard)
1. Title Page (1)
2. Outline (1)
3. Introduction (2)
4. Background (2)
5. Methodology (3)
6. Results (4)
7. Conclusion & Future Work (1)
8. References (1)

### Option B: Long Slides (Comprehensive)
- Cover every section and subsection of the paper.
- Allocate slides proportionally to the depth of each section.
- Ensure all major findings and methodological details are captured.

## 3. LaTeX Generation Rules
- Use the provided template in `templates/latex/main.tex`.
- Use `\section{}` to organize the presentation.
- Use `itemize` for bullet points (limit to 3-5 points per slide).
- Use `columns` for text-heavy or comparison slides.
- Ensure all LaTeX special characters (%, $, &, etc.) are properly escaped.
- Include `\bibliographystyle{apalike}` and `\bibliography{references}` if citations are present.

## 4. Quality Checklist
- [ ] Title and authors match the paper.
- [ ] No overflow of text on slides.
- [ ] Logical flow from introduction to conclusion.
- [ ] Consistent formatting.
