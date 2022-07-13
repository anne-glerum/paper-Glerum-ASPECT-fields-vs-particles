# -*- coding: utf-8 -*-
"""
Created on Wed July 13 by Anne Glerum
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes 
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
rc("pdf", fonttype=42)
rc("lines", linewidth=5, markersize=15)

# Change path as needed
base = r"/Users/acglerum/Documents/Postdoc/SB_CRYSTALS/HLRN/HLRN/fix_stresses_elasticity/paper_11072022/"

# Change file name modifiers as needed depending on your file structure
names = [
         "surface_topo_diffusion_constant_h_dt0.0005_GR0",
        ]
tail = r"/statistics"

# The labels the graphs will get in the plot
labels = [
          'dt = 0.0005 s, dh = 1 m',
         ]
# Set the colors available for plotting
color1=[0.0051932, 0.098238, 0.34984]
color2=[0.092304, 0.32922, 0.38504]
color3=[0.32701, 0.4579, 0.28638]
color4=[0.67824, 0.55071, 0.1778]
color5=[0.97584, 0.63801, 0.50183]
color6=[0.98447, 0.78462, 0.93553]
colors = [color1, color2, color3, color4, color5, color5, color1, color3, color5]
# Set the line styles
linestyles = ['solid', 'solid', 'solid', 'solid', 'solid', 'dotted', 'dotted', 'dotted', 'dotted'] 
# Set the marker styles (no markers in this case)
markers = ['', '', '', '', '', '', '', '', ''] 
# Only plot every nth marker
dmark=35

# Set up a row of two plots, one with absolute stress values
# and one with the percentage difference to the analytical solution
fig = plt.figure(figsize=(10, 6))
ax = [fig.add_subplot(2, 1, i) for i in range(1, 3)]

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

# The analytical solution:
# Return stress in Pa.
def topo_analytical(x,time):
    amplitude = 0.075
    domain_width = 1
    nmax = 5000
    kappa = 0.25
    topo = amplitude * np.sin(x*np.PI/domain_width) * exp(-kappa*np.::PI*np.PI*time/(domain_width*domain_width));
    return topo


for name in names: 
  # Create file path
  path = base+name+tail

  # Read in the time and the minimum xx component of the viscoelastic stress,
  # which is stored on the field ve_stress_xx.
  # The correct columns are selected with usecols (counting starts from 0).
  if 'particle' in name:
    time,topo = np.genfromtxt(path, comments='#', usecols=(1,12), unpack=True)
  else:
    time,topo = np.genfromtxt(path, comments='#', usecols=(1,24), unpack=True)

  # Plot the stress elements in Pa against time in s in
  # categorical batlow colors.
  ax[0].plot(time,topo,label=None,color=colors[counter],linestyle=linestyles[counter],marker=markers[counter],markevery=dmark)
  #axins.plot(time,topo,label=None,color=colors[counter],linestyle=linestyles[counter],marker=markers[counter],markevery=dmark)
  ax[1].plot(time,(topo-topo_analytical(time))/topo_analytical(time)*100.,label=labels[counter],color=colors[counter],linestyle=linestyles[counter],marker=markers[counter],markevery=dmark)
  
  counter += 1

# Plot the analytical solution in Pa.
ax[0].plot(time,topo_analytical(time),label='analytical',color='black',linestyle='dashdot')
#axins.plot(time,1e-6*tau_xy_analytical(time),label='analytical',color='black',linestyle='dashdot')

# Labelling of plot
ax[1].set_xlabel("Time [s]")
ax[0].set_ylabel(r"Topography [m]")
ax[1].set_ylabel(r"Error [%]")
# Manually place legend in lower right corner. 
ax[0].legend(loc='lower right')
ax[1].legend(loc='lower right')
# Grid and tickes
ax[0].grid(axis='x',color='0.95')
ax[0].set_yticks([0,5,10,15])
ax[0].grid(axis='y',color='0.95')
ax[1].grid(axis='x',color='0.95')
ax[1].grid(axis='y',color='0.95')
#ax[1].set_yticks([0,0.1,0.2,0.3,0.4,0.5])

# Ranges of the axes
ax[0].set_xlim(0,0.1) # s
#ax[0].set_ylim(0,15.5) # MPa
ax[1].set_xlim(0,0.1) # s
#ax[1].set_ylim(-0.5,0.5) # %

# Add labels a) and b)
#ax[0].text(-16,208,"a)")
#ax[1].text(-16,-0.05,"b)")

# Add timestep labels
#ax[1].text(50,-0.77,"dt = 500 yr", rotation = 20)
#ax[1].text(50,-0.30,"dt = 250 yr", rotation = 6)
#ax[1].text(5,-0.1,"dt = 125 yr", rotation = 3)


plt.tight_layout()

# Save as pdf
plt.savefig('10_surface_topography_diffusion_zero_flux.pdf')    
