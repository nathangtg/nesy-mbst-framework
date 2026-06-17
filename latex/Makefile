# ============================================================================
# Makefile for LaTeX IEEE Paper Compilation
# ============================================================================
# Usage:
#   make          - Build the PDF (pdflatex + bibtex + pdflatex x2)
#   make clean    - Remove all auxiliary files
#   make distclean - Remove auxiliary files AND the PDF
#   make view     - Open the PDF (macOS)
# ============================================================================

MAIN = main
LATEX = pdflatex
BIBTEX = bibtex

.PHONY: all clean distclean view

all: $(MAIN).pdf

$(MAIN).pdf: $(MAIN).tex sections/*.tex references.bib
	$(LATEX) $(MAIN)
	$(BIBTEX) $(MAIN)
	$(LATEX) $(MAIN)
	$(LATEX) $(MAIN)

clean:
	rm -f $(MAIN).aux $(MAIN).bbl $(MAIN).blg $(MAIN).log $(MAIN).out \
	      $(MAIN).toc $(MAIN).lof $(MAIN).lot $(MAIN).fls $(MAIN).fdb_latexmk \
	      $(MAIN).synctex.gz sections/*.aux

distclean: clean
	rm -f $(MAIN).pdf

view: $(MAIN).pdf
	open $(MAIN).pdf
