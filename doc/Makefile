preview: build
	open thesis.pdf

build: thesis.tex thesis.bib
	rm thesis.bbl
	rm thesis.blg
	pdflatex thesis.tex
	bibtex thesis
	pdflatex thesis.tex
	pdflatex thesis.tex
