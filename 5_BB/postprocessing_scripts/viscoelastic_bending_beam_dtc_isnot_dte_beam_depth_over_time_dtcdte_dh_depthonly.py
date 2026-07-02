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
rc("lines", linewidth=2, markersize=8)

# Change path as needed
base = r"/Users/acglerum/Documents/Postdoc/SB_CRYSTALS/HLRN/HLRN/fix_stresses_elasticity/paper_14072023/BM5/"

# Change file name modifiers as needed depending on your file structure
names = [
         #"RL9_viscoelastic_bending_beam_smooth25m_DGlimiter_Newton_dtc500_dte500_averaginggeometric_IGR1_IAR0",
         #"RL9_viscoelastic_bending_beam_smooth25m_DGlimiter_Newton_dtc500_dte500_averaginggeometric_IGR2_IAR0",
         #"RL9_viscoelastic_bending_beam_smooth25m_DGlimiter_Newton_dtc500_dte500_averaginggeometric_IGR2_IAR1",
          'RL9_viscoelastic_bending_beam_htansmooth10m_Newton_AMG_main_dtc500_dte500_averaginggeometric_IGR2_IAR0',
          'RL9_viscoelastic_bending_beam_htansmooth10m_Newton_AMG_main_dtc500_dte500_averaginggeometric_IGR2_IAR1',
#          'RL9_viscoelastic_bending_beam_htansmooth10m_Newton_AMG_main_dtc500_dte500_averaginggeometric_IGR2_IAR2',
          'RL9_viscoelastic_bending_beam_htansmooth10m_Newton_AMG_main_dtc250_dte250_averaginggeometric_IGR2_IAR2',
        ]
tail = r"/statistics"

# The labels the graphs will get in the plot
labels = [
          #'dh = 50 m',
          'dh = 25 m',
          'dh = 12.5 m',
          'dh = 6.25 m',
#          'dh = 6.25 m, dt = 250 ky',
         ]
# Set the colors available for plotting
color1=[0.0051932, 0.098238, 0.34984]
color2=[0.092304, 0.32922, 0.38504]
color3=[0.32701, 0.4579, 0.28638]
color4=[0.67824, 0.55071, 0.1778]
color5=[0.97584, 0.63801, 0.50183]
color6=[0.98447, 0.78462, 0.93553]
colors = [color1, color3, color4, color6, color5, color6, 'black', 'blue', color3, color4, color5]
# Set the line styles
linestyles = ['solid', 'solid', 'solid', 'solid', 'solid', 'solid', 'solid','dashdot', 'dashdot', 'dotted',  'dotted','dotted'] 
# Set the marker styles (no markers in this case)
markers = ['', '', '', '', '', '', '', '', '', '', '', '', '', ''] 
dmark = 100

# Set up a row of two plots, one with the maximum beam depth
# and one with the min and max ve_stress_xx
#fig = plt.figure(figsize=(10, 6))
fig = plt.figure(figsize=(4, 4))
ax = [fig.add_subplot(2, 1, i) for i in range(1, 2)]

yr_in_secs = 3600. * 24. * 365.2425
counter = 0 

# Create file path
for name in names: 
  path = base+name+tail

  # Read in the time, the maximum beam depth and min/max/ave ve_stress_xx.
  # The correct columns are selected with usecols.
  time,beam_depth,ve_xx_min,ve_xx_max,ve_xx_ave = np.genfromtxt(path, comments='#', usecols=(1,49,22,23,24), unpack=True)

  # Plot the beam depth in m against time in ky in
  # categorical batlow colors.
  ax[0].plot(time/1e3,beam_depth,label=labels[counter],color=colors[counter],linestyle=linestyles[counter],marker=markers[counter],markevery=dmark+counter)
  
  counter += 1

# Plot horizontal line at initial depth
ax[0].hlines(2800,0,50000,color='black',linestyle='dashed',label=None,linewidth=1)
ax[0].text(100,2805,r"$\mathrm{z_{max}(t_{0})}$",va='bottom',ha='center',bbox=dict(facecolor='white', edgecolor='none',boxstyle='square,pad=0.'),fontsize=8)
ax[0].hlines(2812.5,0,50000,color='black',linestyle='dotted',label=None,linewidth=1)
#ax[0].text(100,2817.5,r"$\mathrm{z_{max}(t_{0})}+12.5$",va='top',ha='center',bbox=dict(facecolor='white', edgecolor='none',boxstyle='square,pad=0.'),fontsize=8)

# Plot horizontal line at maximum analytical depth
# Equation 3.85 of Turcotte and Schubert 2002
# for G = 1e10 Pa
# L = 4800 m
# h = 600 m
# E 3G Pa
# D = 72e6 G
# q = 3e6 kg/(ms^2)
# The maximum deflection at x = 4800 is therefore 276.48 m.
#ax[0].hlines(3076.48,0,500000,color='black',linestyle='dashdot',label='analytical max depth',linewidth=1)

# Plot vertical line at t=50 ky, when gravity is switched off.
ax[0].vlines(50,4000,2000,color='black',linestyle='solid',label=None,linewidth=1)
ax[0].text(50,2925,r"gravity off",va='center',ha='center',bbox=dict(facecolor='white', edgecolor='none',boxstyle='square,pad=0.1'), rotation='vertical',fontsize=8)

# Labelling of plot
ax[0].set_xlabel("Time [ky]")
ax[0].set_ylabel(r"Max. beam depth [m]")
# Place legend
ax[0].legend(loc='lower right',ncol=1,handlelength=2,fontsize=8)
# Grid and tickes
ax[0].grid(axis='x',color='0.95')
#ax[0].set_yticks([0,1000,2000,3000,4000])
ax[0].grid(axis='y',color='0.95')

# Ranges of the axes
ax[0].set_xlim(0,350) # kyr
ax[0].set_ylim(3100,2750) # m

# Add labels a) and b)
#ax[0].text(-25,2750,"a)")

plt.tight_layout()

# Save as pdf
filename = '5_viscoelastic_bending_beam_htansmooth10_dte_isnot_dtc_depth_dh_depthonly.png'
plt.savefig(filename, dpi=300)
print ('Plot in: ' + filename)
