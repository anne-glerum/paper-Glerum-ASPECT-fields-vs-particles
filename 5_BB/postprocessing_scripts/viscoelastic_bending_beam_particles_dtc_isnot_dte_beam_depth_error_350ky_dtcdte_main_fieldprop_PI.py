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
base = r"/Users/acglerum/Documents/Postdoc/SB_CRYSTALS/HLRN/HLRN/fix_stresses_elasticity/paper_14072023/BM5/"

# Change file name modifiers as needed depending on your file structure
names = [
          'RL9_viscoelastic_bending_beam_htansmooth10m_particles_Newton_diffminmaxPPC_fieldpropRR_main_avegeometric_intcell_average_limTrue_dtc500_dte500_IGR2_IAR1_np4',
          'RL9_viscoelastic_bending_beam_htansmooth10m_particles_Newton_diffminmaxPPC_fieldpropRR_main_avegeometric_intnearest_neighbor_limTrue_dtc500_dte500_IGR2_IAR1_np4',
          'RL9_viscoelastic_bending_beam_htansmooth10m_particles_Newton_diffminmaxPPC_fieldpropRR_main_avegeometric_intdistance_weighted_average_limTrue_dtc500_dte500_IGR2_IAR1_np4',
          'RL9_viscoelastic_bending_beam_htansmooth10m_particles_Newton_diffminmaxPPC_fieldpropRR_main_avegeometric_intbilinear_least_squares_limTrue_dtc500_dte500_IGR2_IAR1_np4',
          'RL9_viscoelastic_bending_beam_htansmooth10m_particles_Newton_diffminmaxPPC_fieldpropRR_main_avegeometric_intquadratic_least_squares_limTrue_dtc500_dte500_IGR2_IAR1_np4',
        ]
tail = r"/statistics"

# The labels the graphs will get in the plot
labels = [
#          'dt = 500 yr, dh = 12.5 m, CA, htan10m, pw = 0',
#          'dt = 500 yr, dh = 12.5 m, NN, htan10m, pw = 0',
#          'dt = 500 yr, dh = 12.5 m, LLS, htan10m, pw = 0',
#          'dt = 500 yr, dh = 12.5 m, QLS, htan10m, pw = 0',
#          'dt = 500 yr, dh = 12.5 m, DWA, htan10m, pw = 0',
          'CA',
          'NN',
          'DWA',
          'LLS',
          'QLS',
         ]
# Set the colors available for plotting
color1=[0.0051932, 0.098238, 0.34984]
color2=[0.092304, 0.32922, 0.38504]
color3=[0.32701, 0.4579, 0.28638]
color4=[0.67824, 0.55071, 0.1778]
color5=[0.97584, 0.63801, 0.50183]
color6=[0.98447, 0.78462, 0.93553]
colors = [color1, color2, color3, color4, color5, color6, color5, color4, color5, 'black', 'blue', color3, color4, color5]
# Set the line styles
linestyles = ['solid', 'solid', 'solid', 'solid', 'solid', 'solid', 'solid', 'solid', 'solid', 'solid', 'solid', 'solid', 'solid', 'solid']
# Set the marker styles (no markers in this case)
markers = ['s', 'x', 'v', '.', '3', '*', 'd', '', '', '', '', '', '', ''] 

# Set up a row of two plots, one with the maximum beam depth
# at t = 350 ky and one with the error of that depth wrt the original max depth.
fig = plt.figure(figsize=(4, 6))
ax = [fig.add_subplot(2, 1, i) for i in range(1, 3)]

yr_in_secs = 3600. * 24. * 365.2425
counter = 0 

# Create file path
for name in names: 
  path = base+name+tail

  # Read in the time, the maximum beam depth and min/max/ave ve_stress_xx.
  # The correct columns are selected with usecols.
  time,beam_depth,ve_xx_min,ve_xx_max,ve_xx_ave = np.genfromtxt(path, comments='#', usecols=(1,23,24,25,26), unpack=True)
  print ("Max t: ", time[-1])
  print ("Max beam depth at t = 50 ky: ", beam_depth[np.where(time == 50000)])
  print ("Max beam depth at t = 350 ky: ", beam_depth[-1])

  # Plot the beam depth in m against counter
  # categorical batlow colors.
  ax[0].scatter(counter,beam_depth[-1],label=labels[counter],color=colors[counter],linestyle=linestyles[counter],marker=markers[counter])
  # Plot the absolute error
  ax[1].scatter(counter,beam_depth[-1] - 2800.,label=labels[counter],color=colors[counter],linestyle=linestyles[counter],marker=markers[counter])
  
  counter += 1

# Plot horizontal line at initial depth
ax[0].hlines(2800.,-50000,50000,color='black',linestyle='dashed',label=r"$\mathrm{z_{max}(t_{0})}$",linewidth=1)

# Plot horizontal line at initial depth + one cell height (100/2^3)
ax[0].hlines(2812.5,-50000,50000,color='black',linestyle='dotted',label=r"$\mathrm{z_{max}(t_{0})+dh}$",linewidth=1)

# Plot horizontal line at maximum analytical depth
# Equation 3.85 of Turcotte and Schubert 2002
# for G = 1e10 Pa
# L = 4800 m
# h = 600 m
# E 3G Pa
# D = 72e6 G
# q = 3e6 kg/(ms^2)
# The maximum deflection at x = 4800 is therefore 276.48 m.
#ax[0].hlines(3076.48,0,500000,color='black',label='analytical max depth',linestyle='dashdot',linewidth=1)

# Labelling of plot
ax[1].set_xlabel("Simulation [-]")
ax[0].set_ylabel(r"Beam depth [m] at t = 350 ky")
ax[1].set_ylabel(r"Abs. error beam depth [m] at t = 350 ky")
# Place legend
ax[0].legend(loc='lower right',ncol=2,handlelength=2,fontsize=8)
# Grid and tickes
ax[0].grid(axis='x',color='0.95')
ax[0].grid(axis='y',color='0.95')
ax[1].grid(axis='x',color='0.95')
ax[1].grid(axis='y',color='0.95')
ax[0].set_xticks([])
ax[0].set_yticks([2800,2820,2840,2860,2880])
ax[1].set_xticks([])
ax[1].set_yticks([0,10,20,30,40,50,60])
ax[0].set_title("Particles, htan10m, Newton, pw0, geometric, dt500, IGR2, IAR1, np4", fontsize=6)

# Ranges of the axes
ax[0].set_xlim(-0.5,4.5) # -
ax[0].set_ylim(2870,2790) # m
ax[1].set_xlim(-0.5,4.5) # -
ax[1].set_ylim(0,70) # m

# Add labels a) and b)
ax[0].text(-1.8,2790,"a)")
ax[1].text(-1.8,70,"b)")

plt.tight_layout()

# Save as pdf
filename = '5_viscoelastic_bending_beam_particles_dte_isnot_dtc_main_fieldprop_maxdeptherror_PI.png'
plt.savefig(filename, dpi=300)
print ('Plot in: ' + filename)
