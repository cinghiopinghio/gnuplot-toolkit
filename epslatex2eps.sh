#!/bin/bash
########################################
# Transform epslatex files from gnuplot
# to eps files (with latex text included)
# Usage:
# epslatex2ps path/to/file[.tex] append
# append: trailing string ("text": defaults)
#########################################

if [[ $1 == "" ]]
then
	echo epslatex2esp file append_text
	echo convert esplatex graphs from gnuplot
	echo in eps file with text included
	echo Usage:
	echo 'file[.tex] = file to convert'
	echo append_text = text to append to the file name
	exit
fi


input=$1
dir=${input%/*}
[[ ${dir} == ${input} ]] && dir='.'
file=${input##*/}
# take away the extension from the input file name
[[ ${file##*.} != "" ]] && input=$dir/${file%.*}
append=$2
[[ $append == "" ]] &&	append="text"


# original dimensions xy
let x=$(grep BoundingBox ${input}.eps | awk '{print $(NF-1)}')
let y=$(grep BoundingBox ${input}.eps | awk '{print $(NF)}')
let x1=${x}-1
let y1=${y}-1

tmp='tmp'

cat > ${tmp}.tex << EOF
\documentclass[12pt]{article}
\usepackage{graphicx}
\usepackage{color}
\usepackage[english]{babel}
\usepackage{amstext,amsmath,amssymb,amsfonts,bm}
\usepackage[textwidth=${x1}pt,textheight=${y1}pt,paperwidth=${x}pt,paperheight=${y}pt]{geometry}
\usepackage{epsfig}
\begin{document}
\thispagestyle{empty}
\centering
\resizebox{\textwidth}{!}{\sffamily\input{${input}}}
\end{document}
EOF

latex ${tmp}.tex
dvips ${tmp}.dvi
ps2eps -f ${tmp}.ps

rm ${tmp}.tex ${tmp}.dvi ${tmp}.ps
rm ${tmp}.log ${tmp}.aux

mv ${tmp}.eps ${file%.*}_$append.eps


