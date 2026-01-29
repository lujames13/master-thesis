all: main.pdf

main.pdf: main.tex
	./build.sh

clean:
	find . -type f \( \
		-name "*.aux" -o \
		-name "*.log" -o \
		-name "*.bbl" -o \
		-name "*.blg" -o \
		-name "*.toc" -o \
		-name "*.out" -o \
		-name "*.lof" -o \
		-name "*.lot" -o \
		-name "*.run.xml" -o \
		-name "*.bcf" -o \
		-name "*-blx.bib" -o \
		-name "*.xdv" \
	\) -delete

.PHONY: main.pdf
