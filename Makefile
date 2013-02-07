SHFILE=epslatexeps
PYFILE=epslatex2eps
PATHDIR=~/.local/bin

install:
	ln -sf ${CURDIR}/${SHFILE}.sh ${PATHDIR}/${SHFILE}
	ln -sf ${CURDIR}/${PYFILE}.py ${PATHDIR}/${PYFILE}
uninstall:
	rm -f ${PATHDIR}/${SHFILE}
	rm -f ${PATHDIR}/${PYFILE}
