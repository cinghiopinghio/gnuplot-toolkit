from __future__ import print_function

colors=['#000000', 
        '#ff181f', 
        '#2e8b57', 
        '#0060ad', 
        '#ff8c00', 
        '#9400d3', 
        '#b22222', 
        '#556b2f', 
        '#dc143c', 
        '#6495ed']

styles=range(10)

print ('set terminal wxt dash')

for nc,c in enumerate(colors):
  for s in styles:
    print('set style line',str(nc*len(styles)+s),'lc rgb',c,'pt' ,s,\
          'ps 2 lt',s,'lw 2')

print ('\n# set borders\n\
set style line 21 lc rgb \'#303030\' lt 1 lw 1.5\n\
set border 3 back ls 21\n\
set tics nomirror out scale 0.75\n\
\n\
# set grid\n\
set style line 22 lc rgb \'#808080\' lt 0 lw 1\n\
set grid back ls 22\n')

# add arrows to the graph
#set arrow from graph 1,0 to graph 1.05,0 size screen 0.025,15,60 \
#    filled ls 21
#set arrow from graph 0,1 to graph 0,1.05 size screen 0.025,15,60 \
#    filled ls 21


print('\
# function to plot histograms:\n\
# usage:\n\
# p "filename" u (BIN($1,width)):(1.0) smooth freq with boxes\n\
BIN(X,WIDTH)=WIDTH*floor(X/WIDTH)+WIDTH/2')


