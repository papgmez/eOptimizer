all:
	make compile
	make clean
	evince uclmTFGesi.pdf

compile:
	python compile.py uclmTFGesi
release:
	make clean
	cp uclmTFGesi.pdf ../TFG_PalominoGomezPablo.pdf
clean:
	$(RM) -rf *.log
	$(RM) -rf *~
	$(RM) -rf *.toc
	$(RM) -rf *.out
	$(RM) -rf *.aux
	$(RM) -rf *.lof
	$(RM) -rf *.lol
	$(RM) -rf *.lot
	$(RM) -rf *.loa
	$(RM) -rf *.bcf
	$(RM) -rf *.bbl
	$(RM) -rf *.blg
	$(RM) -rf *.idx
	$(RM) -rf *.gz
	$(RM) -rf *.xml
