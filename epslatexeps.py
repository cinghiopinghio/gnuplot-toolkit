#!/usr/bin/env python2.7
########################################
# Transform epslatex files from gnuplot
# to eps files (with latex text included)
#########################################
from __future__ import print_function
import subprocess as sp
import os,shutil
import argparse
import random

def main(args=None):

  # arguments control

  file=os.path.realpath(args.file)
  if not os.path.isfile(file):
    print('ERR: no such file')
    exit(1)

  root,ext=os.path.splitext(file)
  if ext!='.tex':
    print('ERR: wrong file; need *.tex file')
    exit(2)

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

  with open(file,'r') as fl:
    buf=fl.readlines()
  for n,l in enumerate(buf):
    if l=='\\begin{document}\n':
      pos=n+1
      break

  ## Use sans serif fonts

  if args.sans:
    buf.insert(pos,'\\sffamily\n')

  ## create temporary file

  rand=random.randrange(100,1000)
  roottmp='/tmp/temporaryfilefromesplatexeps'+str(rand)
  while os.path.isfile(roottmp+'.tex'):
    rand=random.randrange(100,1000)
    roottmp='/tmp/temporaryfilefromesplatexeps'+str(rand)
  with open(roottmp+'.tex','w') as fl:
    fl.writelines(buf)


  ## Compile latex File
  CLargs=['-interaction=nonstopmode','-output-directory=/tmp/','-aux-directory=/tmp/']
  output=sp.call(['latex']+CLargs+[roottmp+'.tex'],stderr=sp.STDOUT,stdout=sp.PIPE)
  if output:
    print ('Error in LaTeX file:')
    print ('Take a look at log file?[y/n]')
    sel = raw_input()
    if sel.capitalize() == 'Y':
      print (roottmp+'.log')
      print (root+'epslatexeps.log')
      shutil.copy(roottmp+'.log',root+'epslatexeps.log')

    remove_tmp(roottmp)
    exit(3)
  output=sp.call(['dvips','-j0 -G0',roottmp+'.dvi'],stderr=sp.STDOUT,stdout=sp.PIPE)
  if output:
    print ('Error compiling *.dvi:')
    print ('Take a look at you file')
    remove_tmp(roottmp)
    exit(4)
  if args.pdf:
    output=sp.call(['ps2pdf','-f',roottmp+'.ps'],stderr=sp.STDOUT,stdout=sp.PIPE)
    if output:
      print ('Error compiling *.ps:')
      print ('Take a look at you file')
      remove_tmp(roottmp)
      exit(5)
  else:
    output=sp.call(['ps2eps','-f',roottmp+'.ps'],stderr=sp.STDOUT,stdout=sp.PIPE)
    if output:
      print ('Error compiling *.ps:')
      print ('Take a look at you file')
      remove_tmp(roottmp)
      exit(5)


  if args.o==None:
    if args.pdf:
      os.rename(roottmp+'.pdf',root+'.pdf')
    else:
      os.rename(roottmp+'.eps',root+'.eps')
  else:
    if args.pdf:
      os.rename(roottmp+'.pdf',args.o)
    else:
      os.rename(roottmp+'.eps',args.o)


def remove_tmp(roottmp):
  ## Delete temporary files

  remove_ext=['.tex','.dvi','.ps','.log','.aux']

  if args.remove:
    for e in remove_ext:
      if os.path.isfile(roottmp+e):
        os.remove(roottmp+e)


if __name__=='__main__':
  # parse arguments

  parser = argparse.ArgumentParser(description='Epslatex to eps')
  parser.add_argument('file', metavar='FILE',
                     help='epsLaTeX TeX file')
  parser.add_argument('-r','--remove',action='store_false',
                     help='do not remove building files')
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
