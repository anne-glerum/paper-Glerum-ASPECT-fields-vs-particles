# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 by Anne Glerum
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes 
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
marker_size = 8
rc("pdf", fonttype=42)
rc("lines", linewidth=3, markersize=marker_size)

# Change path as needed
base = r"/Users/acglerum/Documents/Postdoc/SB_CRYSTALS/HLRN/HLRN/fix_stresses_elasticity/paper_14072023/BM5/"

# Change file name modifiers as needed depending on your file structure
names = [
          'RL9_viscoelastic_bending_beam_htansmooth10m_particles_Newton_diffminmaxPPC_fieldpropRR_main_avegeometric_intbilinear_least_squares_limTrue_dtc500_dte500_IGR2_IAR1_np4',
          'RL9_viscoelastic_bending_beam_htansmooth10m_particles_Newton_diffminmaxPPC_fieldpropRR_main_avegeometric_intbilinear_least_squares_limTrue_dtc500_dte500_IGR2_IAR1_np8',
#          'RL9_viscoelastic_bending_beam_htansmooth10m_particles_Newton_diffminmaxPPC_fieldpropRR_main_avegeometric_intbilinear_least_squares_limTrue_dtc500_dte500_IGR2_IAR1_np16',
          'RL9_VE_BB_htansmooth10m_particles_Newton_diffminmaxPPC_pw0_main_avegeometric_intbilinear_least_squares_limTrue_dtc500_dte500_IGR2_IAR1_np16',
          #'RL9_VE_BB_htansmooth10m_particles_Newton_diffminmaxPPC_pw0_main_avegeometric_intbilinear_least_squares_limFalse_dtc500_dte500_IGR2_IAR2_np16',
          'RL9_viscoelastic_bending_beam_htansmooth10m_particles_Newton_diffminmaxPPC_fieldpropRR_main_avegeometric_intquadratic_least_squares_limTrue_dtc500_dte500_IGR2_IAR1_np4',
          'RL9_viscoelastic_bending_beam_htansmooth10m_particles_Newton_diffminmaxPPC_fieldpropRR_main_avegeometric_intquadratic_least_squares_limTrue_dtc500_dte500_IGR2_IAR1_np8',
          #'RL9_viscoelastic_bending_beam_htansmooth10m_particles_Newton_diffminmaxPPC_fieldpropRR_main_avegeometric_intquadratic_least_squares_limTrue_dtc500_dte500_IGR2_IAR1_np16',
          'RL9_VE_BB_htansmooth10m_particles_Newton_diffminmaxPPC_pw0_main_avegeometric_intquadratic_least_squares_limTrue_dtc500_dte500_IGR2_IAR1_np16',
#          'RL9_VE_BB_htansmooth10m_particles_Newton_diffminmaxPPC_pw0_main_avegeometric_intquadratic_least_squares_limFalse_dtc500_dte500_IGR2_IAR2_np16',
        ]
tail = r"/statistics"

# The labels the graphs will get in the plot
labels = [
          '4x4, LLS',
          '8x8, LLS',
          '16x16, LLS',
          #'16x16, LLS, 6.25 m',
          '4x4, QLS',
          '8x8, QLS',
          '16x16, QLS',
          '16x16, QLS, 6.25 m',
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
markers = ['s', 'x', 'v', 'd', '3', '*', '.', '_', '1', '2', '', '', '', ''] 

# Set up a row of two plots, one with the maximum beam depth
# at t = 350 ky and one with the error of that depth wrt the original max depth.
#fig = plt.figure(figsize=(4, 6))
#ax = [fig.add_subplot(2, 1, i, sharex=True) for i in range(1, 3)]
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True,figsize=(4,4))
fig.subplots_adjust(hspace=0.01)  # adjust space between Axes

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
  id_sim = counter
  sym_size = marker_size
  ax1.scatter(id_sim,beam_depth[-1],label=None,color=colors[counter],linestyle=linestyles[counter],marker=markers[counter],s=sym_size**2)
  ax1.text(id_sim,beam_depth[-1]-4,r'{0:.0f}'.format(beam_depth[-1]),fontsize=9,color=colors[counter],bbox=dict(facecolor='white', edgecolor='none',boxstyle='square,pad=0.'))
  beam_depth_50ky = beam_depth[np.where(time == 50000)][0]
  ax2.scatter(id_sim,beam_depth_50ky,label=labels[counter],color=colors[counter],linestyle=linestyles[counter],marker=markers[counter],s=sym_size**2)
  ax2.text(id_sim,beam_depth_50ky-4,r'{0:.0f}'.format(beam_depth_50ky),fontsize=9,color=colors[counter],bbox=dict(facecolor='white', edgecolor='none',boxstyle='square,pad=0.'))
  
  counter += 1

# Plot horizontal line at initial depth
# For the tanh beam, this is 2800 m.
#ax1.hlines(2800,-50000,50000,color='black',linestyle='dashed',label=r"$\mathrm{z_{max}(t_{0})}$",linewidth=1)
ax1.hlines(2800,-50000,50000,color='black',linestyle='dashed',label=None,linewidth=1)

# Plot horizontal line at initial depth + one cell height (100/2^3)
#ax1.hlines(2812.5,-50000,50000,color='black',linestyle='dotted',label=r"$\mathrm{z_{max}(t_{0})+dh}$",linewidth=1)
ax1.hlines(2812.5,-50000,50000,color='black',linestyle='dotted',label=None,linewidth=1)

# Plot horizontal line at maximum analytical depth
# Equation 3.85 of Turcotte and Schubert 2002
# for G = 1e10 Pa
# L = 4800 m
# h = 600 m
# E 3G Pa
# D = 72e6 G
# q = 3e6 kg/(ms^2)
# The maximum deflection at x = 4800 is therefore 276.48 m.
#ax1.hlines(3076.48,0,500000,color='black',label='analytical max depth',linestyle='dashdot',linewidth=1)

# Labelling of plot
ax2.set_xlabel("Simulation [-]")
ax1.set_ylabel(r"Max. beam depth [m]")
ax1.annotate("t = 350 ky", xytext=(5.35,2825), xy=(1.5, 2815),ha='right',va='center')
ax1.text(-0.1,2800,r"$\mathrm{z_{max}(t_{0})}$",va='center',ha='left',bbox=dict(boxstyle='square,pad=0',facecolor='white', edgecolor='none'))
ax2.annotate("t = 50 ky", xytext=(5.35,3037.5), xy=(1, 3055),ha='right',va='center')
ax1.annotate(r"", xytext=(-0.4,2812.5), xy=(-0.4, 2800),
            arrowprops=dict(arrowstyle="<->",relpos=(0,1)))
ax1.text(-0.35,2806.25,r"dh",va='center',ha='left',bbox=dict(facecolor='white', edgecolor='none',boxstyle='square,pad=0.'))
ax2.legend(loc='lower left',ncol=2,handlelength=1,fontsize=7,markerscale=0.9)
# Grid and tickes
ax1.set_axisbelow(True)
ax2.set_axisbelow(True)
ax1.grid(axis='x',color='0.95')
ax1.grid(axis='y',color='0.95')
ax2.grid(axis='x',color='0.95')
ax2.grid(axis='y',color='0.95')
ax2.set_xticks([0,1,2,3,4,5],['','','','','',''])
ax1.set_title("Particles, htan10m, Newton, pw0, geometric, LLS/QLS, dt500, IGR2, IAR1", fontsize=6)

# hide the spines between ax and ax2
ax1.spines.bottom.set_visible(False)
ax2.spines.top.set_visible(False)
ax1.xaxis.tick_top()
ax1.tick_params(labeltop=False)  # don't put tick labels at the top
ax2.xaxis.tick_bottom()

# Ranges of the axes
ax1.set_xlim(-0.5,5.5) # -
ax1.set_ylim(2835,2795) # m
ax2.set_xlim(-0.5,5.5) # -
ax2.set_ylim(3075,3035) # m

# Now, let's turn towards the cut-out slanted lines.
# We create line objects in axes coordinates, in which (0,0), (0,1),
# (1,0), and (1,1) are the four corners of the Axes.
# The slanted lines themselves are markers at those locations, such that the
# lines keep their angle and position, independent of the Axes size or scale
# Finally, we need to disable clipping.

d = .5  # proportion of vertical to horizontal extent of the slanted line
kwargs = dict(marker=[(-1, -d), (1, d)], markersize=12,
              linestyle="none", color='k', mec='k', mew=1, clip_on=False)
ax1.plot([0, 1], [0, 0], transform=ax1.transAxes, **kwargs)
ax2.plot([0, 1], [1, 1], transform=ax2.transAxes, **kwargs)

# Add labels a) and b)
#ax1.text(-1.8,2790,"a)")
#ax2.text(-1.8,140,"b)")

plt.tight_layout()

# Save as pdf
filename = '5_viscoelastic_bending_beam_particles_dte_isnot_dtc_main_fieldprop_maxdeptherror_np.png'
plt.savefig(filename, dpi=300)
print ('Plot in: ' + filename)
