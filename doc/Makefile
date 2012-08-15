preview: build
	open thesis.pdf

build: thesis.tex thesis.bib
	rm -f thesis.bbl
	rm -f thesis.blg
	pdflatex thesis.tex
	bibtex thesis
	pdflatex thesis.tex
	pdflatex thesis.tex
