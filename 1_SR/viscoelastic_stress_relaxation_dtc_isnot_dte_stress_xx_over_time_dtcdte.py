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
rc("lines", linewidth=3, markersize=3)

# Change path as needed
base = r"/Users/acglerum/Documents/Postdoc/SB_CRYSTALS/HLRN/HLRN/fix_stresses_elasticity/paper_14072023/BM1/"

# Change file name modifiers as needed depending on your file structure
names = [
         "ve_relaxation_dtc500_dte500_GR2_g0",
         "ve_relaxation_dtc250_dte250_GR2_g0",
         "ve_relaxation_dtc125_dte125_GR2_g0",
         "ve_relaxation_dtc62.5_dte62.5_GR2_g0",
        ]
tail = r"/statistics"

# The labels the graphs will get in the plot
labels = [
          'dtc = dte = 500 yr, dh = 25 km',
          'dtc = dte = 250 yr, dh = 25 km',
          'dtc = dte = 125 yr, dh = 25 km',
          'dtc = dte = 62.5 yr, dh = 25 km',
         ]
# Set the colors available for plotting
color1=[0.0051932, 0.098238, 0.34984]
color2=[0.092304, 0.32922, 0.38504]
color3=[0.32701, 0.4579, 0.28638]
color4=[0.67824, 0.55071, 0.1778]
color5=[0.97584, 0.63801, 0.50183]
color6=[0.98447, 0.78462, 0.93553]
colors = [color2, color3, color4, color5, color6, color4, color5, color3, color4, color5]
# Set the line styles
linestyles = ['solid', 'solid', 'solid', 'solid', 'solid', 'dashdot', 'dashdot', 'dotted',  'dotted','dotted'] 
# Set the marker styles (no markers in this case)
markers = ['', '', '', '', '', '', '', '', '', '', '', '', '', ''] 

# Set up a row of two plots, one with absolute stress values
# and one with the percentage difference to the analytical solution
fig = plt.figure(figsize=(10, 6))
ax = [fig.add_subplot(2, 1, i) for i in range(1, 3)]

# Also plot a zoom-in of the absolute stress values
zoom_x_min = 20
zoom_x_max = 25
zoom_y_min = 9
zoom_y_max = 11
#axins = zoomed_inset_axes(ax[0], 6, loc="upper center") 
#axins.set_xlim(zoom_x_min, zoom_x_max)
#axins.set_ylim(zoom_y_min, zoom_y_max)
#mark_inset(ax[0], axins, loc1=2, loc2=3, fc="none", ec="0.5")

yr_in_secs = 3600. * 24. * 365.2425
counter = 0 

# Create file path
for name in names: 
  path = base+name+tail

  # Read in the time and the minimum xx and yy components of the viscoelastic stress,
  # which are stored on the fields ve_stress_xx and ve_stress_yy.
  # The correct columns are selected with usecols.
#  if counter == 0:
#    time,stress_xx_min = np.genfromtxt(path, comments='#', usecols=(1,15), unpack=True)
#  else:
  time,stress_xx_min = np.genfromtxt(path, comments='#', usecols=(1,18), unpack=True)

  # Plot the stress elements in MPa against time in ky in
  # categorical batlow colors.
  ax[0].plot(time/1e3,stress_xx_min/1e6,label=labels[counter],color=colors[counter],linestyle=linestyles[counter],marker=markers[counter])
#  axins.plot(time/1e3,stress_xx_min/1e6,label=None,color=colors[counter],linestyle=linestyles[counter],marker=markers[counter])
  ax[1].plot(time/1e3,(stress_xx_min-(20e6*np.exp(-1e10*time*yr_in_secs/1e22)))/(20e6*np.exp(-1e10*time*yr_in_secs/1e22))*100.,label=labels[counter],color=colors[counter],linestyle=linestyles[counter],marker=markers[counter])
  
  counter += 1

# Plot the analytical solution
# tau_xx(t) = tau_xx_t0 * exp(-mu*t/eta_viscous), 
# with tau_xx_t0 = 20 MPa, eta_viscous = 1e22 Pas, mu = 1e10 Pa.
ax[0].plot(time/1e3,20*np.exp(-1e10*time*yr_in_secs/1e22),label='analytical',color='black',linestyle="dashed")

# Labelling of plot
ax[1].set_xlabel("Time [ky]")
ax[0].set_ylabel(r"Viscoelastic stress $\tau_{xx}$ [MPa]")
ax[1].set_ylabel(r"Error [%]")
# Manually place legend in lower right corner. 
ax[0].legend(loc='upper right',ncol=1,handlelength=4)
#ax[1].legend(loc='lower right',ncol=2,handlelength=5)
# Grid and tickes
ax[0].grid(axis='x',color='0.95')
ax[0].set_yticks([0,5,10,15,20])
ax[0].grid(axis='y',color='0.95')
ax[1].grid(axis='x',color='0.95')
ax[1].grid(axis='y',color='0.95')
ax[1].set_yticks([0,2,4,6,8,10])

# Ranges of the axes
ax[0].set_xlim(0,250) # kyr
ax[0].set_ylim(0,21) # MPa
ax[1].set_xlim(0,250) # kyr
ax[1].set_ylim(0,10) # %

# Add labels a) and b)
ax[0].text(-15,21,"a)")
ax[1].text(-15,10,"b)")

# Add timestep labels
#ax[1].text(150,4.1,"dt = 500 yr", rotation = 13)
#ax[1].text(150,2.2,"dt = 250 yr", rotation = 6)
#ax[1].text(150,0.4,"dt = 125 yr", rotation = 3)


#plt.tight_layout()

# Save as pdf
plt.savefig('1_viscoelastic_relaxation_dte_isnot_dtc_fields_dtcdte.png')    
