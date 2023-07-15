python texextract.py
pdflatex -synctex=1 -interaction=nonstopmode "out".tex
evince out.pdf
