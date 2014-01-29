all: edurepo.pdf edutree.pdf

clean:
	rm -f *.log *.dvi *.aux *.pdf

.SUFFIXES:

%.pdf : %.dvi
	dvipdf $< $@

%.dvi : %.tex
	latex $<
