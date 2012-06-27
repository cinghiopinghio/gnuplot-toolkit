shfile=epslates2eps
pyfile=epslatexeps

install:
	ln -sf ${CURDIR}/epslatex2eps.sh ~/bin/epslatex2eps
	ln -sf ${CURDIR}/epslatexeps.py ~/bin/epslatexeps
uninstall:
	rm -f ~/bin/epslatex2eps
	rm -f ~/bin/epslatexeps
