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
rc("lines", linewidth=5, markersize=15)

# Change path as needed
base = r"/Users/acglerum/Documents/Postdoc/SB_CRYSTALS/HLRN/HLRN/fix_stresses_elasticity/paper_11072022/"

# Change file name modifiers as needed depending on your file structure
names = [
         "ve_build-up_dt500_GR0",
         "ve_build-up_dt500_GR1",
         "ve_build-up_dt500_GR2",
         "ve_build-up_dt250_dh10km",
         "ve_build-up_dt250_dh5km",
         "ve_build-up_dt250_dh2-5km",
         "ve_build-up_dt125_dh10km",
         "ve_build-up_dt125_dh5km",
         "ve_build-up_dt125_dh2-5km",
        ]
tail = r"/statistics"

# The labels the graphs will get in the plot
labels = [
          'dt = 500 yr, dh = 10 km',
          'dt = 500 yr, dh = 5 km',
          'dt = 500 yr, dh = 2.5 km',
          'dt = 250 yr, dh = 10 km',
          'dt = 250 yr, dh = 5 km',
          'dt = 250 yr, dh = 2.5 km',
          'dt = 125 yr, dh = 10 km',
          'dt = 125 yr, dh = 5 km',
          'dt = 125 yr, dh = 2.5 km'
         ]
# Set the colors available for plotting
color1=[0.0051932, 0.098238, 0.34984]
color2=[0.092304, 0.32922, 0.38504]
color3=[0.32701, 0.4579, 0.28638]
color4=[0.67824, 0.55071, 0.1778]
color5=[0.97584, 0.63801, 0.50183]
color6=[0.98447, 0.78462, 0.93553]
colors = [color1, color3, color5, color1, color3, color5, color1, color3, color5]
# Set the line styles
linestyles = ['solid', 'solid', 'solid', 'dashed', 'dashed', 'dashed', 'dotted', 'dotted', 'dotted'] 
# Set the marker styles (no markers in this case)
markers = ['|', '', '', 'x', '', '', '', '', ''] 

# Only plot every nth marker
dmark=35

# Set up a row of two plots, one with absolute stress values
# and one with the percentage difference to the analytical solution
fig = plt.figure(figsize=(10, 6))
ax = [fig.add_subplot(2, 1, i) for i in range(1, 3)]

# Also plot a zoom-in of the absolute stress values
zoom_x_min = 40
zoom_x_max = 70
zoom_y_min = 140
zoom_y_max = 180
axins = zoomed_inset_axes(ax[0], 3, loc = "center") # zoom = 2
axins.set_xlim(zoom_x_min, zoom_x_max)
axins.set_ylim(zoom_y_min, zoom_y_max)
mark_inset(ax[0], axins, loc1=2, loc2=3, fc="none", ec="0.5")

yr_in_secs = 3600. * 24. * 365.2425
counter = 0 

# The analytical solution:
# 2 * edot_ii * eta * (1 - e^(-mu*t/eta)), 
# with edot_ii = 0.03154/yr_in_secs/model_width 1/s, eta = 1e22 Pas, mu = 1e10 Pa.
# Return stress in Pa.
def tau_xx_analytical(time):
  yr_in_secs=3600.0*24.0*365.25
  edot_ii=0.03154/yr_in_secs/100000.
  eta=1e22
  mu=1e10
  return 2.*edot_ii*eta*(1.-np.exp(-time*yr_in_secs*mu/eta))


for name in names: 
  # Create file path
  path = base+name+tail

  # Read in the time and the minimum xx component of the viscoelastic stress,
  # which is stored on the field ve_stress_xx.
  # The correct columns are selected with usecols (counting starts from 0).
  time,stress_xx_min = np.genfromtxt(path, comments='#', usecols=(1,15), unpack=True)

  # Plot the stress elements in MPa against time in ky in
  # categorical batlow colors.
  ax[0].plot(time/1e3,stress_xx_min/1e6,label=labels[counter],color=colors[counter],linestyle=linestyles[counter],marker=markers[counter],markevery=dmark)
  axins.plot(time/1e3,stress_xx_min/1e6,label=labels[counter],color=colors[counter],linestyle=linestyles[counter],marker=markers[counter],markevery=dmark)
  ax[1].plot(time/1e3,(stress_xx_min-tau_xx_analytical(time))/tau_xx_analytical(time)*100.,label=labels[counter],color=colors[counter],linestyle=linestyles[counter],marker=markers[counter],markevery=dmark)
  
  counter += 1

# Plot the analytical solution in MPa.
ax[0].plot(time/1e3,1e-6*tau_xx_analytical(time),label='analytical',color='black',linestyle='dashed')
axins.plot(time/1e3,1e-6*tau_xx_analytical(time),label='analytical',color='black',linestyle='dashed')

# Labelling of plot
ax[1].set_xlabel("Time [ky]")
ax[0].set_ylabel(r"Viscoelastic stress $\tau0_{xx}$ [MPa]")
ax[1].set_ylabel(r"Error [%]")
# Manually place legend in lower right corner. 
ax[0].legend(loc='lower right')
# Grid and tickes
ax[0].grid(axis='x',color='0.95')
ax[0].set_yticks([0,50,100,150,200])
ax[0].grid(axis='y',color='0.95')
ax[1].grid(axis='x',color='0.95')
ax[1].grid(axis='y',color='0.95')
#ax[1].set_yticks([0,0.1,0.2,0.3,0.4,0.5])

# Ranges of the axes
ax[0].set_xlim(0,250) # kyr
ax[0].set_ylim(0,210) # MPa
ax[1].set_xlim(0,250) # kyr
#ax[1].set_ylim(0,0.05) # %

# Add labels a) and b)
ax[0].text(-16,208,"a)")
ax[1].text(-16,-0.05,"b)")

# Add timestep labels
ax[1].text(5,-0.78,"dt = 500 yr", rotation = 39)
ax[1].text(5,-0.29,"dt = 250 yr", rotation = 19)
ax[1].text(5,-0.13,"dt = 125 yr", rotation = 10)


plt.tight_layout()

# Save as pdf
plt.savefig('2_viscoelastic_build-up.pdf')    
