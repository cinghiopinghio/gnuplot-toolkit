# gnuplot-toolkit 

___

toolkit to transform epslatex plots to eps
___

Gnuplot can produce nice plots to add to your latex documents.
These plots can be prepared to use latex fonts thanks to its `epslatex`
terminal.

When you print to `epslatex` terminal you end up with some files:
- file.tex
- file-inc.eps

Latex-ing file.tex you obtain the wanted plot.

This ToolKit let you _transform_ your tex file to eps (pdf) without the huge
amount of log/data file printed out by latex.

## Install

from its folder:
 
`make install`

It make a link to `~/.local/bin/`, so make sure it exists and it is in you
`$PATH`!

## Usage

usage: `epslatexeps [-h] [-f] [-s] [-p] [-o OUTFILE] FILE`

Epslatex to eps

positional arguments:
- `FILE`         epsLaTeX TeX file

optional arguments:
-  `-h, --help`   show this help message and exit
-  `-f, --force`  force overwriting
-  `-s, --sans`   use sans serif fonts for text
-  `-p, --pdf`    output in pdf
-  `-o OUTFILE`   output file

