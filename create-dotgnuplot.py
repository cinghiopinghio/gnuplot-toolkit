from __future__ import print_function

colors=['\'#000000\'', 
        '\'#ff181f\'', 
        '\'#2e8b57\'', 
        '\'#0060ad\'', 
        '\'#ff8c00\'', 
        '\'#9400d3\'', 
        '\'#b22222\'', 
        '\'#556b2f\'', 
        '\'#dc143c\'', 
        '\'#6495ed\'']

styles=range(10)

print ('set terminal wxt dash')

border='''
#set borders
set style line 101 lc rgb \'#303030\' lt 1 lw 1.5
set border 3 back ls 101
set tics nomirror out scale 0.75
'''

grid='''
#set grid
set style line 102 lc rgb \'#808080\' lt 0 lw 1
set grid back ls 102
'''


arrows='''
# add arrows to the graph
#set arrow from graph 1,0 to graph 1.05,0 size screen 0.025,15,60 \
#    filled ls 100
#set arrow from graph 0,1 to graph 0,1.05 size screen 0.025,15,60 \
#    filled ls 100
'''

histo='''
# function to plot histograms:
# usage:
# p "filename" u (BIN($1,width)):(1.0) smooth freq with boxes
BIN(X,WIDTH)=WIDTH*floor(X/WIDTH)+WIDTH/2
'''

print(border)
print(grid)
print(arrows)
print(histo)


for nc,c in enumerate(colors):
  for s in styles:
    tag=nc*len(styles)+s
    if tag==0:
      tag=100
    print('set style line',str(tag),'lc rgb',c,'pt' ,s+1,\
          'ps 2 lt',s+1,'lw 2')



