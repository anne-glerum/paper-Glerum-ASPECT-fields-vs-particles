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
base = r"/Users/acglerum/Documents/Postdoc/SB_CRYSTALS/HLRN/HLRN/fix_stresses_elasticity/paper_14072023/BM3/"

# Change file name modifiers as needed depending on your file structure
names = [
         "ve_build-up_simple_shear_dtc0.01_dte0.01_GR1_1",
         "ve_build-up_simple_shear_dtc0.01_dte0.01_GR2_1",
         "ve_build-up_simple_shear_dtc0.01_dte0.01_GR3_1",
         "ve_build-up_simple_shear_dtc0.01_dte0.01_GR4_1",
        ]
tail = r"/statistics"

# The labels the graphs will get in the plot
labels = [
          'dh = 0.5 m',
          'dh = 0.25 m',
          'dh = 0.125 m',
          'dh = 0.0625 m',
         ]
# Set the colors available for plotting
color1=[0.0051932, 0.098238, 0.34984]
color2=[0.092304, 0.32922, 0.38504]
color3=[0.32701, 0.4579, 0.28638]
color4=[0.67824, 0.55071, 0.1778]
color5=[0.97584, 0.63801, 0.50183]
color6=[0.98447, 0.78462, 0.93553]
colors = [color2, color3, color4, color5, color5, color6, color1, color2, color3, color5]
# Set the line styles
linestyles = ['solid', 'solid', 'solid', 'solid', 'solid', 'solid', 'solid', 'dashed', 'dotted'] 
# Set the marker styles (no markers in this case)
markers = ['|', '', 'x', '', 'o', '', '', '', ''] 
# Only plot every nth marker
dmark=5

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
def tau_xy_analytical(t):
    V=0.3
    mu=1e2
    eta_v=1e2
    h=1
    C1 = -(V*V*eta_v*eta_v*mu)/(mu*mu*h*h+V*V*eta_v*eta_v)
    C2 = -(V*h*eta_v*mu*mu)/(mu*mu*h*h+V*V*eta_v*eta_v)
    # at 0.5, shearing stops
    tmax=0.5
    return np.where(t<=tmax,(np.exp(-mu/eta_v*t)*(C2*np.cos(V*t/h)-C1*np.sin(V*t/h))-C2),(np.exp(-mu/eta_v*tmax)*(C2*np.cos(V*tmax/h)-C1*np.sin(V*tmax/h))-C2)*np.exp(-mu/eta_v*(t-tmax)))


for name in names: 
  # Create file path
  path = base+name+tail

  # Read in the time and the average value of the xy component of the viscoelastic stress,
  # which is stored on the field ve_stress_xy.
  # The correct columns are selected with usecols (counting starts from 0).
  time,stress_xy_ave = np.genfromtxt(path, comments='#', usecols=(1,28), unpack=True)

  # Plot the stress elements in Pa against time in s in
  # categorical batlow colors.
  ax[0].plot(time,stress_xy_ave,label=labels[counter],color=colors[counter],linestyle=linestyles[counter],marker=markers[counter],markevery=dmark)
  #axins.plot(time,stress_xy_ave,label=None,color=colors[counter],linestyle=linestyles[counter],marker=markers[counter],markevery=dmark)
  ax[1].plot(time,(stress_xy_ave-tau_xy_analytical(time))/tau_xy_analytical(time)*100.,label=None,color=colors[counter],linestyle=linestyles[counter],marker=markers[counter],markevery=dmark)

  for tau in stress_xy_ave:
    if tau > 15:
      print ("Too high tau: ", name)
  
  counter += 1

# Plot the analytical solution in Pa.
ax[0].plot(time,tau_xy_analytical(time),label='analytical',color='black',linestyle='dashed')
#axins.plot(time,1e-6*tau_xy_analytical(time),label='analytical',color='black',linestyle='dashed')

# Labelling of plot
ax[1].set_xlabel("Time [s]")
ax[0].set_ylabel(r"Viscoelastic stress $\tau0_{xy}$ [Pa]")
ax[1].set_ylabel(r"Error [%]")
# Manually place legend in lower right corner. 
ax[0].legend(loc='upper left',handlelength=4)
#ax[1].legend(loc='lower right',ncol=1,handlelength=4)
# Grid and tickes
ax[0].grid(axis='x',color='0.95')
ax[0].set_yticks([0,5,10,15])
ax[0].grid(axis='y',color='0.95')
ax[1].grid(axis='x',color='0.95')
ax[1].grid(axis='y',color='0.95')
ax[1].set_yticks([0,-0.2,-0.4,0.2])

# Ranges of the axes
ax[0].set_xlim(0,1.) # s
ax[0].set_ylim(0,15.5) # MPa
ax[1].set_xlim(0,1.) # s
ax[1].set_ylim(-0.55,0.22) # %

# Add labels a) and b)
ax[0].text(-0.055,15.5,"a)")
ax[1].text(-0.07,0.22,"b)")

# Add timestep labels
#ax[1].text(50,-0.77,"dt = 500 yr", rotation = 20)
#ax[1].text(50,-0.30,"dt = 250 yr", rotation = 6)
#ax[1].text(5,-0.1,"dt = 125 yr", rotation = 3)


plt.tight_layout()

# Save
plt.savefig('3_viscoelastic_build-up_simple_shear_dtc_isnot_dte_dh.png')    
