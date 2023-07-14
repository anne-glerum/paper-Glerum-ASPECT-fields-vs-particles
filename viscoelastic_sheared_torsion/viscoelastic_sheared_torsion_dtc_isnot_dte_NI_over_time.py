# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 by Anne Glerum
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes 
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
rc("pdf", fonttype=42)
rc("lines", linewidth=3, markersize=8)

# Change path as needed
base = r"/Users/acglerum/Documents/Postdoc/SB_CRYSTALS/HLRN/HLRN/fix_stresses_elasticity/paper_11072022/BM4/"

# Change file name modifiers as needed depending on your file structure
names = [
         "ve_sheared_torsion_dtc0.01_dte0.01_GR1",
         "ve_sheared_torsion_JD_dtc0.01_dte0.01_GR1",
        ]
tail = r"/statistics"

# The labels the graphs will get in the plot
labels = [
          'dtc = dte = 0.01 s, dh = 0.5 m',
          'dtc = dte = 0.01 s, dh = 0.5 m, res fix',
         ]
# Set the colors available for plotting
color1=[0.0051932, 0.098238, 0.34984]
color2=[0.092304, 0.32922, 0.38504]
color3=[0.32701, 0.4579, 0.28638]
color4=[0.67824, 0.55071, 0.1778]
color5=[0.97584, 0.63801, 0.50183]
color6=[0.98447, 0.78462, 0.93553]
colors = [color2, color4, color5, color5, color6, color5, color1, color3, color5]
# Set the line styles
linestyles = ['solid', 'solid', 'solid', 'solid', 'solid', 'solid', 'dotted', 'dotted', 'dotted'] 
# Set the marker styles (no markers in this case)
markers = ['', '', '', '', '', '', '', '', ''] 
# Only plot every nth marker
dmark=35

# Set up a row of two plots, one with absolute stress values
# and one with the percentage difference to the analytical solution
fig = plt.figure(figsize=(10, 6))
ax = [fig.add_subplot(1, 1, i) for i in range(1, 2)]

# Also plot a zoom-in of the absolute stress values
zoom_x_min = 0.45
zoom_x_max = 0.65
zoom_y_min = 10
zoom_y_max = 13
#axins = zoomed_inset_axes(ax[0], 3, loc = "center") # zoom = 2
#axins.set_xlim(zoom_x_min, zoom_x_max)
#axins.set_ylim(zoom_y_min, zoom_y_max)
#mark_inset(ax[0], axins, loc1=1, loc2=4, fc="none", ec="0.5")

yr_in_secs = 3600. * 24. * 365.2425
counter = 0 


for name in names: 
  # Create file path
  path = base+name+tail

  # Read in the time and the minimum xx component of the viscoelastic stress,
  # which is stored on the field ve_stress_xz.
  # The correct columns are selected with usecols (counting starts from 0).
  if 'particle' in name:
    time,NI = np.genfromtxt(path, comments='#', usecols=(0,12), unpack=True)
  else:
    time,NI = np.genfromtxt(path, comments='#', usecols=(0,7), unpack=True)

  ax[0].plot(time,NI,label=labels[counter],color=colors[counter],linestyle=linestyles[counter],marker=markers[counter],markevery=dmark)

  counter += 1

# Labelling of plot
ax[0].set_xlabel("Time step number")
ax[0].set_ylabel(r"Total nr of nonlinear iterations")
# Legend
ax[0].legend(loc='upper right',handlelength=4)
#ax[1].legend(loc='lower right',ncol=1,handlelength=4)
# Grid and tickes
ax[0].grid(axis='x',color='0.95')
ax[0].set_yticks([0,10,20,30,40,50,60,70,80,90,100])
ax[0].grid(axis='y',color='0.95')

# Ranges of the axes
#ax[0].set_xlim(0,200)  
ax[0].set_ylim(0,102) 

# Add labels a) and b)
#ax[0].text(-0.055,15.5,"a)")
#ax[1].text(-0.07,0.25,"b)")

plt.tight_layout()

# Save
plt.savefig('4_viscoelastic_sheared_torsion_dtc_isnot_dte_dtcisdte_NI.png')    
