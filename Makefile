PYFILE=epslatex2eps
PATHDIR=~/.local/bin

install:
	ln -sf ${CURDIR}/${PYFILE}.py ${PATHDIR}/${PYFILE}
uninstall:
	rm -f ${PATHDIR}/${PYFILE}
