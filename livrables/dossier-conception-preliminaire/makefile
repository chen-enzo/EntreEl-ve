help:
	@echo
	@echo "make dossier   <-- génère le pdf"
	@echo "make clean     <-- efface tous les fichiers annexes produits par latex."
	@echo

dossier: dossier-conception-preliminaire.pdf
	@echo
	@echo dossier-conception-preliminaire.pdf généré.

TEX_SOURCES = $(wildcard *.tex)
dossier-conception-preliminaire.pdf: $(TEX_SOURCES)
	pdflatex dossier-conception-preliminaire
	pdflatex dossier-conception-preliminaire

clean:
	@rm -rf *~ *.log *.out *.toc *.aux

