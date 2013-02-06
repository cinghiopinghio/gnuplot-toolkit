#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################
# Transform epslatex files from gnuplot
# to eps files (with latex text included)
#########################################
from __future__ import print_function
import subprocess as sp
import os,shutil
import argparse
import tempfile as tmp

def main(args=None):
# arguments control
  file=os.path.realpath(args.file)
  root,ext = check_file(file)

  if not args.force:
    if args.pdf:
      if os.path.isfile(root+'.pdf'):
        print(root+'.pdf Already exist; overwrite?[y/n]')
        choice = raw_input().lower()
        if not choice=='y':
          exit(6)
    else:
      if os.path.isfile(root+'.eps'):
        print(root+'.eps Already exist; overwrite?[y/n]')
        choice = raw_input().lower()
        if not choice=='y':
          exit(6)

  buf,pos = file_to_buffer(file)
  if pos == None:
    'The file is not standalone'
    'not implemented yet'
    print('The file is not standalone')
    box = get_bounding_box(file)
    buf = modify_buffer(buf,box)
    pos=1 ## set \sffamily after \begin{document}

## Use sans serif fonts

  if args.sans:
    buf.insert(pos,'\\sffamily\n')

## create temporary folder

  rootdtmp=tmp.mkdtemp('-epslatexeps')

## Compile latex File
  with tmp.NamedTemporaryFile(mode='w',suffix='.tex',dir=rootdtmp,delete=False) as fin:
    fin.writelines(buf)
    fin.flush()
    rootftmp = fin.name[:-4]
    CLargs=['-interaction=nonstopmode','-output-directory='+rootdtmp,'-aux-directory='+rootdtmp]
    output=sp.call(['latex']+CLargs+[rootftmp+'.tex'],stderr=sp.STDOUT,stdout=sp.PIPE)
  if output: 
    ## if errors on compile time:
    print ('Error in LaTeX file:')
    print ('Take a look at log file?[y/n]')
    sel = raw_input()
    if sel.capitalize() == 'Y':
      print (root+'epslatexeps.log')
      sp.call(['cat',rootftmp+'.log'])

    shutil.rmtree(rootdtmp)
    exit(3)
## DVI to PS
  output=sp.call(['dvips','-j0 -G0',rootftmp+'.dvi','-o',rootftmp+'.ps'],stderr=sp.STDOUT,stdout=sp.PIPE)
  if output:
    print ('Error compiling *.dvi:')
    print ('Take a look at you file')
    shutil.rmtree(rootdtmp)
    exit(4)
  if args.pdf:
## PS to PDF
    output=sp.call(['ps2pdf','-f',rootftmp+'.ps',rootftmp+'.pdf'],stderr=sp.STDOUT,stdout=sp.PIPE)
    if output:
      print ('Error compiling *.ps:')
      print ('Take a look at you file')
      shutil.rmtree(rootdtmp)
      exit(5)
  else:
## PS to EPS
    output=sp.call(['ps2eps','-f',rootftmp+'.ps'],stderr=sp.STDOUT,stdout=sp.PIPE)
    if output:
      print ('Error compiling *.ps:')
      print ('Take a look at you file')
      shutil.rmtree(rootdtmp)
      exit(5)

#temporary outfile name (pdf of eps)
  tmpfile = rootftmp + '.pdf' if args.pdf else rootftmp + '.eps'
#outfile name (pdf of eps)
  outfile = root   +   '.pdf' if args.pdf else root   +   '.eps'
#if given, use user specified outfile name
  if args.o != None: outfile = args.o
  shutil.move(tmpfile,outfile)
  
  shutil.rmtree(rootdtmp)

def get_bounding_box(filename):
  eps_filename = filename[:-4]+'.eps'
  with open(eps_filename,'r') as epsin:
    for line in epsin:
      if line[:13] == '%%BoundingBox':
        box = line.split()[-4:]
  return box

def modify_buffer(buffer,box):
  pre,post = set_wrap(box)
  buffer.insert(0,pre)
  buffer.insert(len(buffer),post)
  return buffer

def check_file(filename):
  '''
  check existence and extension of given file
  '''
  if not os.path.isfile(filename):
    print('ERR: no such file')
    exit(1)

  root,ext=os.path.splitext(filename)
  if ext!='.tex':
    print('ERR: wrong file; need *.tex file')
    exit(2)
  return root,ext

def file_to_buffer(filename):
  with open(filename,'r') as fl:
    buffer = fl.readlines()
  pos = None
  for n,l in enumerate(buffer):
    if l == '\\begin{document}\n':
      pos = n+1
      break
  return buffer,pos

def set_wrap (box):
  pre ='''
  \\documentclass{minimal}
  \\makeatletter
  \\def\\@ptsize{1}
  \\InputIfFileExists{size11.clo}{}{%
     \\GenericError{(gnuplot) \\space\\space\\space\\@spaces}{%
        Gnuplot Error: File `size11.clo' not found! Could not set font size%
     }{See the gnuplot documentation for explanation.%
     }{For using a font size a file `size<fontsize>.clo' has to exist.
          Falling back to default fontsize 10pt.}%
    \\def\\@ptsize{0}
    \\input{size10.clo}%
  }%
  \\makeatother
  \\usepackage{graphicx}
  \\usepackage{color}
  \\makeatletter
  \\begingroup
    \\chardef\\x=0 %
    \\@ifundefined{pdfoutput}{}{%
      \\ifcase\\pdfoutput
      \\else
        \\chardef\\x=1 %
      \\fi
    }%
    \\@ifundefined{OpMode}{}{%
      \\chardef\\x=2 %
    }
  \\expandafter\\endgroup
  \\ifcase\\x
    \\PassOptionsToPackage{dvips}{geometry}
  \\or
    \\PassOptionsToPackage{pdftex}{geometry}
  \\else
    \\PassOptionsToPackage{vtex}{geometry}
  \\fi
  \\makeatother
  \\usepackage[papersize={'''+box[2]+'bp,'+box[3]+'bp},text={'+box[2]+'bp,'+box[3]+'''bp}]{geometry}
  \\pagestyle{empty}
  \\setlength{\\parindent}{0bp}%
  \\InputIfFileExists{gnuplot.cfg}{%
    \\typeout{Using configuration file gnuplot.cfg}%
  }{
   \\typeout{No configuration file gnuplot.cfg found.}%
  }
  \\begin{document}
  '''
  post = '''
  \\end{document}
  '''
  return pre,post

if __name__=='__main__':
  # parse arguments
  parser = argparse.ArgumentParser(description='Epslatex to eps')
  parser.add_argument('file', metavar='FILE',
                     help='epsLaTeX TeX file')
  parser.add_argument('-f','--force',action='store_true',
                     help='force overwriting')
  parser.add_argument('-s','--sans',action='store_true',
                     help='use sans serif fonts for text')
  parser.add_argument('-p','--pdf',action='store_true',
                     help='output in pdf')
  parser.add_argument('-o',metavar='OUTFILE',
                     help='output file')
  args = parser.parse_args()
  main(args)
