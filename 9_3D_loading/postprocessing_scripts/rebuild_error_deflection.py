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
rc("legend", fontsize=8)

# Change path as needed
base = r"/Users/acglerum/Documents/Postdoc/SB_CRYSTALS/Papers/Glerum_LD_ASPECT/repo/9_3D_loading/postprocessing_scripts/"

names = [
         "RL9_viscoelastic_3D_loading_particles_AMG_avegeometric_intbilinear_least_squares_limTrue_dtc2.5_dte2.5_IGR1_IAR2_np4",
        ]
tail = r"/topography"

# The labels the graphs will get in the plot
labels = [
          'dtc = 500 yr, dte = 500 yr',
          'dtc = 250 yr, dte = 500 yr',
          'dtc = 125 yr, dte = 500 yr',
          'dtc = 250 yr, dte = 250 yr',
          'dtc = 125 yr, dte = 250 yr',
          'dtc = 62.5 yr, dte = 250 yr',
         ]
# Set the colors available for plotting
color1=[0.0051932, 0.098238, 0.34984]
color2=[0.092304, 0.32922, 0.38504]
color3=[0.32701, 0.4579, 0.28638]
color4=[0.67824, 0.55071, 0.1778]
color5=[0.97584, 0.63801, 0.50183]
color6=[0.98447, 0.78462, 0.93553]
colors = [color1, color2, color3, color4, color5, color6, 'black', 'blue', color3, color4, color5]
# Set the line styles
linestyles = ['solid', 'solid', 'solid', 'dashed', 'dashed', 'dashed', 'dashed','dashdot', 'dashdot', 'dotted',  'dotted','dotted'] 
# Set the marker styles (no markers in this case)
markers = ['', '', '', '', '', '', '', '', '', '', '', '', '', ''] 
dmark = 100

# Set up a row of two plots, one with the maximum beam depth
# and one with the min and max ve_stress_xx
fig = plt.figure(figsize=(10, 6))
ax = [fig.add_subplot(2, 1, i) for i in range(1, 3)]

counter = 0 
dtc = 2.5
end_time = 200
dt_output = 5

# Create file path
for name in names: 
  path = base+name+tail

  print ("Model: ", base+name)

  if 'dtc5.0' in name:
    dtc = 5.0
  elif 'dtc10.0' in name:
    dtc = 10.0
  elif 'dtc15.0' in name:
    dtc = 15.0
  elif 'dtc20.0' in name:
    dtc = 20.0

  n_output = int(end_time / dt_output) + 1
  max_deflection = np.zeros(n_output)
  print ("N output steps: ", n_output)
  time = np.arange(0,end_time + dt_output, dt_output)

  # Loop over all topo files and get the max deflection at each output timestep
  # Topo file: x y z topo
  #for i in np.arange(0,int(end_time + dtc), int(dtc)):
  counter = 0
  for i, j in enumerate(np.arange(0,int(end_time/dtc+1), int(dt_output/dtc))):
    print ("Index, value: ", i, j)
    if j < 10:
      file_path = path + ".0000" + str(j)
    else:
      file_path = path + ".000" + str(j)

    topography = np.genfromtxt(file_path, comments='#', usecols=(3), unpack=True)
    max_deflection[i] = np.min(topography)

    counter += 1

  # Plot the maximum deflection in m against time in yr in
  # categorical batlow colors.
  ax[0].plot(time,max_deflection,label=labels[counter],color=colors[counter],linestyle=linestyles[counter],marker=markers[counter],markevery=dmark+counter)
#   # Plot min and max stress (Pa) against time (ky).
#   ax[1].plot(time/1e3,ve_xx_min,label=labels[counter],color=colors[counter],linestyle=linestyles[counter],marker=None)
#   ax[1].plot(time/1e3,ve_xx_max,label=None,color=colors[counter],linestyle=linestyles[counter],marker=None)
  
#   counter += 1

# # Plot horizontal line at initial depth
# ax[0].hlines(2812.5,0,50000,color='black',linestyle='dashed',label='original max depth',linewidth=1)

# # Plot vertical line at t=50 ky, when gravity is switched off.
# ax[0].vlines(50,4000,2000,color='black',linestyle='dotted',label='gravity off',linewidth=1)

# Labelling of plot
ax[0].set_xlabel("Time [yr]")
ax[1].set_xlabel("Time [yr]")
ax[0].set_ylabel(r"Maximum deflection [m]")
ax[1].set_ylabel(r"Error maximum deflection")
# Place legend
ax[0].legend(loc='lower right',ncol=3,handlelength=4)
# Grid and tickes
ax[0].grid(which='major')
ax[0].grid(axis='x',color='0.95')
#ax[0].set_yticks([0,1000,2000,3000,4000])
ax[0].grid(axis='y',color='0.95')
ax[1].grid(axis='x',color='0.95')
ax[1].grid(axis='y',color='0.95')
#ax[1].set_yticks([0,2,4,6,8,10])

# # Ranges of the axes
# ax[0].set_xlim(0,350) # kyr
# ax[0].set_ylim(3150,2750) # m
# ax[1].set_xlim(0,350) # kyr
# ax[1].set_ylim(-0.75e9,0.75e9) # %

# # Add labels a) and b)
# ax[0].text(-25,2750,"a)")
# ax[1].text(-25,0.75e9,"b)")

plt.tight_layout()

# Save as png
filename = base + '9_3D_loading_max_deflection.png'
plt.savefig(filename, dpi=300)
print ('Plot in: ' + filename)