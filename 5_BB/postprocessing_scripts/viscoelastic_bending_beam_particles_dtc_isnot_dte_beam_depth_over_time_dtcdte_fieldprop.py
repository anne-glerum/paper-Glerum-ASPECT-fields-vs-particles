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
         'RL9_viscoelastic_bending_beam_htansmooth10m_particles_Newton_avegeometric_intdistance_weighted_average_limTrue_dtc125_dte125_IGR2_IAR0_np4',
         #'RL9_viscoelastic_bending_beam_htansmooth20m_particles_Newton_diffminmaxPPC_fieldprop_avegeometric_intbilinear_least_squares_limTrue_dtc62.5_dte62.5_IGR2_IAR0_np4',
         #'RL9_viscoelastic_bending_beam_htansmooth20m_particles_Newton_diffminmaxPPC_fieldprop_avegeometric_intdistance_weighted_average_limTrue_dtc62.5_dte62.5_IGR2_IAR0_np4',
#         'RL9_viscoelastic_bending_beam_htansmooth20m_particles_Newton_diffminmaxPPC_fieldprop_avegeometric_intquadratic_least_squares_limTrue_dtc62.5_dte62.5_IGR2_IAR0_np4',
         #'RL9_viscoelastic_bending_beam_htansmooth20m_particles_Newton_diffminmaxPPC_fieldprop_avegeometric_intcell_average_limTrue_dtc62.5_dte62.5_IGR2_IAR0_np4',
#
#         'RL9_viscoelastic_bending_beam_htansmooth20m_particles_Newton_diffminmaxPPC_fieldpropMMI_avegeometric_intcell_average_limTrue_dtc62.5_dte62.5_IGR2_IAR0_np4',
#         'RL9_viscoelastic_bending_beam_htansmooth20m_particles_Newton_diffminmaxPPC_fieldpropMMI_avegeometric_intquadratic_least_squares_limTrue_dtc62.5_dte62.5_IGR2_IAR0_np4',
#         'RL9_viscoelastic_bending_beam_htansmooth20m_particles_Newton_diffminmaxPPC_fieldpropMMI_avegeometric_intdistance_weighted_average_limTrue_dtc62.5_dte62.5_IGR2_IAR0_np4',
#         'RL9_viscoelastic_bending_beam_htansmooth20m_particles_Newton_diffminmaxPPC_fieldpropMMI_avegeometric_intbilinear_least_squares_limTrue_dtc62.5_dte62.5_IGR2_IAR0_np4',
#
#          'RL9_viscoelastic_bending_beam_htansmooth20m_particles_Newton_diffminmaxPPC_fieldpropupdate_avegeometric_intquadratic_least_squares_limTrue_dtc62.5_dte62.5_IGR2_IAR0_np4',
#          'RL9_viscoelastic_bending_beam_htansmooth20m_particles_Newton_diffminmaxPPC_fieldpropupdate_avegeometric_intdistance_weighted_average_limTrue_dtc62.5_dte62.5_IGR2_IAR0_np4',
#          'RL9_viscoelastic_bending_beam_htansmooth20m_particles_Newton_diffminmaxPPC_fieldpropupdate_avegeometric_intcell_average_limTrue_dtc62.5_dte62.5_IGR2_IAR0_np4',
#          'RL9_viscoelastic_bending_beam_htansmooth20m_particles_Newton_diffminmaxPPC_fieldpropupdate_avegeometric_intbilinear_least_squares_limTrue_dtc62.5_dte62.5_IGR2_IAR0_np4',
#
#          'RL9_viscoelastic_bending_beam_htansmooth20m_particles_Newton_diffminmaxPPC_fieldpropRRupdate_avegeometric_intquadratic_least_squares_limTrue_dtc62.5_dte62.5_IGR2_IAR0_np4',
#          'RL9_viscoelastic_bending_beam_htansmooth20m_particles_Newton_diffminmaxPPC_fieldpropRRupdate_avegeometric_intdistance_weighted_average_limTrue_dtc62.5_dte62.5_IGR2_IAR0_np4',
#          'RL9_viscoelastic_bending_beam_htansmooth20m_particles_Newton_diffminmaxPPC_fieldpropRRupdate_avegeometric_intcell_average_limTrue_dtc62.5_dte62.5_IGR2_IAR0_np4',
#          'RL9_viscoelastic_bending_beam_htansmooth20m_particles_Newton_diffminmaxPPC_fieldpropRRupdate_avegeometric_intbilinear_least_squares_limTrue_dtc62.5_dte62.5_IGR2_IAR0_np4',
#
#          'RL9_viscoelastic_bending_beam_htansmooth20m_particles_Newton_diffminmaxPPC_fieldpropRTupdate_avegeometric_intquadratic_least_squares_limTrue_dtc62.5_dte62.5_IGR2_IAR0_np4',
#          'RL9_viscoelastic_bending_beam_htansmooth20m_particles_Newton_diffminmaxPPC_fieldpropRTupdate_avegeometric_intdistance_weighted_average_limTrue_dtc62.5_dte62.5_IGR2_IAR0_np4',
#          'RL9_viscoelastic_bending_beam_htansmooth20m_particles_Newton_diffminmaxPPC_fieldpropRTupdate_avegeometric_intcell_average_limTrue_dtc62.5_dte62.5_IGR2_IAR0_np4',
#          'RL9_viscoelastic_bending_beam_htansmooth20m_particles_Newton_diffminmaxPPC_fieldpropRTupdate_avegeometric_intbilinear_least_squares_limTrue_dtc62.5_dte62.5_IGR2_IAR0_np4',
#
#          'RL9_viscoelastic_bending_beam_htansmooth20m_particles_Newton_diffminmaxPPC_fieldpropRRavegeometric_intbilinear_least_squares_limTrue_dtc62.5_dte62.5_IGR2_IAR0_np4',
#          'RL9_viscoelastic_bending_beam_htansmooth20m_particles_Newton_diffminmaxPPC_fieldpropRRavegeometric_intcell_average_limTrue_dtc62.5_dte62.5_IGR2_IAR0_np4',
#          'RL9_viscoelastic_bending_beam_htansmooth20m_particles_Newton_diffminmaxPPC_fieldpropRRavegeometric_intdistance_weighted_average_limTrue_dtc62.5_dte62.5_IGR2_IAR0_np4',
#          'RL9_viscoelastic_bending_beam_htansmooth20m_particles_Newton_diffminmaxPPC_fieldpropRRavegeometric_intquadratic_least_squares_limTrue_dtc62.5_dte62.5_IGR2_IAR0_np4',
#          'RL9_viscoelastic_bending_beam_htansmooth20m_particles_Newton_diffminmaxPPC_fieldpropRR_avegeometric_intdistance_weighted_average_limTrue_dtc62.5_dte62.5_IGR2_IAR1_np8',
#          'RL9_viscoelastic_bending_beam_htansmooth10m_particles_Newton_diffminmaxPPC_fieldpropRR_avegeometric_intcell_average_limTrue_dtc62.5_dte62.5_IGR2_IAR1_np16',
#          'RL9_viscoelastic_bending_beam_htansmooth10m_particles_Newton_diffminmaxPPC_fieldpropRR_avegeometric_intdistance_weighted_average_limTrue_dtc62.5_dte62.5_IGR2_IAR1_np16',
#          'RL9_viscoelastic_bending_beam_htansmooth10m_particles_Newton_diffminmaxPPC_fieldpropRR_avegeometric_intnearest_neighbor_limTrue_dtc62.5_dte62.5_IGR2_IAR1_np16',
          'RL9_viscoelastic_bending_beam_htansmooth10m_particles_Newton_diffminmaxPPC_fieldpropRR_main_avegeometric_intbilinear_least_squares_limTrue_dtc250_dte250_IGR2_IAR1_np4',
#
#'RL9_viscoelastic_bending_beam_htansmooth20m_particles_Newton_diffminmaxPPC_fieldpropRRMMI_avegeometric_intbilinear_least_squares_limTrue_dtc62.5_dte62.5_IGR2_IAR0_np4',
#'RL9_viscoelastic_bending_beam_htansmooth20m_particles_Newton_diffminmaxPPC_fieldpropRRMMI_avegeometric_intcell_average_limTrue_dtc62.5_dte62.5_IGR2_IAR0_np4',
#'RL9_viscoelastic_bending_beam_htansmooth20m_particles_Newton_diffminmaxPPC_fieldpropRRMMI_avegeometric_intdistance_weighted_average_limTrue_dtc62.5_dte62.5_IGR2_IAR0_np4',
#'RL9_viscoelastic_bending_beam_htansmooth20m_particles_Newton_diffminmaxPPC_fieldpropRRMMI_avegeometric_intquadratic_least_squares_limTrue_dtc62.5_dte62.5_IGR2_IAR0_np4', 
#
#'RL9_viscoelastic_bending_beam_htansmooth20m_particles_Newton_diffminmaxPPC_fieldpropRT_avegeometric_intbilinear_least_squares_limTrue_dtc62.5_dte62.5_IGR2_IAR0_np4',
#'RL9_viscoelastic_bending_beam_htansmooth20m_particles_Newton_diffminmaxPPC_fieldpropRT_avegeometric_intcell_average_limTrue_dtc62.5_dte62.5_IGR2_IAR0_np4',
#'RL9_viscoelastic_bending_beam_htansmooth20m_particles_Newton_diffminmaxPPC_fieldpropRT_avegeometric_intdistance_weighted_average_limTrue_dtc62.5_dte62.5_IGR2_IAR0_np4',
#'RL9_viscoelastic_bending_beam_htansmooth20m_particles_Newton_diffminmaxPPC_fieldpropRT_avegeometric_intquadratic_least_squares_limTrue_dtc62.5_dte62.5_IGR2_IAR0_np4',
#
#'RL9_viscoelastic_bending_beam_htansmooth20m_particles_Newton_diffminmaxPPC_fieldpropRTMMI_avegeometric_intbilinear_least_squares_limTrue_dtc62.5_dte62.5_IGR2_IAR0_np4',
#'RL9_viscoelastic_bending_beam_htansmooth20m_particles_Newton_diffminmaxPPC_fieldpropRTMMI_avegeometric_intcell_average_limTrue_dtc62.5_dte62.5_IGR2_IAR0_np4',
#'RL9_viscoelastic_bending_beam_htansmooth20m_particles_Newton_diffminmaxPPC_fieldpropRTMMI_avegeometric_intdistance_weighted_average_limTrue_dtc62.5_dte62.5_IGR2_IAR0_np4',
#'RL9_viscoelastic_bending_beam_htansmooth20m_particles_Newton_diffminmaxPPC_fieldpropRTMMI_avegeometric_intquadratic_least_squares_limTrue_dtc62.5_dte62.5_IGR2_IAR0_np4',
        ]
tail = r"/statistics"

# The labels the graphs will get in the plot
labels = [
          'dtc = dte = 125 yr, htan10m, DWA',
#          'dtc = dte = 62.5 yr, BLS, htan20m, min!=max PPC, field prop.',
#          'dtc = dte = 62.5 yr, DWA, htan20m, min!=max PPC, field prop.',
#          'dtc = dte = 62.5 yr, QLS, htan20m, min!=max PPC, field prop.',
#          'dtc = dte = 62.5 yr, CA, htan20m, min!=max PPC, field prop.',
#
#          'dtc = dte = 62.5 yr, CA, htan20m, min!=max PPC, field prop. MMI',
#          'dtc = dte = 62.5 yr, QLS, htan20m, min!=max PPC, field prop. MMI',
#          'dtc = dte = 62.5 yr, DWA, htan20m, min!=max PPC, field prop. MMI',
#          'dtc = dte = 62.5 yr, BLS, htan20m, min!=max PPC, field prop. MMI',
#
#          'dtc = dte = 62.5 yr, QLS, htan20m, min!=max PPC, field prop. update',
#          'dtc = dte = 62.5 yr, DWA, htan20m, min!=max PPC, field prop. update',
#          'dtc = dte = 62.5 yr, CA, htan20m, min!=max PPC, field prop. update',
#          'dtc = dte = 62.5 yr, BLS, htan20m, min!=max PPC, field prop. update',
#
#          'dtc = dte = 62.5 yr, QLS, htan20m, min!=max PPC, field prop. RR update',
#          'dtc = dte = 62.5 yr, DWA, htan20m, min!=max PPC, field prop. RR update',
#          'dtc = dte = 62.5 yr, CA, htan20m, min!=max PPC, field prop. RR update',
#          'dtc = dte = 62.5 yr, BLS, htan20m, min!=max PPC, field prop. RR update',
#
#          'dtc = dte = 62.5 yr, QLS, htan20m, min!=max PPC, field prop. RT update',
#          'dtc = dte = 62.5 yr, DWA, htan20m, min!=max PPC, field prop. RT update',
#          'dtc = dte = 62.5 yr, CA, htan20m, min!=max PPC, field prop. RT update',
#          'dtc = dte = 62.5 yr, BLS, htan20m, min!=max PPC, field prop. RT update',
#
#          'dtc = dte = 62.5 yr, BLS, htan20m, min!=max PPC, field prop. RR',
#          'dtc = dte = 62.5 yr, CA, htan20m, min!=max PPC, field prop. RR',
#          'dtc = dte = 62.5 yr, DWA, htan20m, min!=max PPC, field prop. RR',
#          'dtc = dte = 62.5 yr, QLS, htan20m, min!=max PPC, field prop. RR',
#          'dtc = dte = 62.5 yr, DWA, htan20m, min!=max PPC, field prop. RR, IAR=1, PPC=8x8',
#          'dtc = dte = 62.5 yr, BLS, field prop. RR',
#          'dtc = dte = 62.5 yr, CA, field prop. RR',
#          'dtc = dte = 62.5 yr, DWA, field prop. RR',
#          'dtc = dte = 62.5 yr, QLS, field prop. RR',
#          'dtc = dte = 62.5 yr, DWA, field prop. RR, IAR=1, PPC=8x8',
#          'dtc = dte = 62.5 yr, CA, field prop. RR, IAR=1, PPC=16x16, htan10m',
#          'dtc = dte = 62.5 yr, DWA, field prop. RR, IAR=1, PPC=16x16, htan10m',
#          'dtc = dte = 62.5 yr, NN, field prop. RR, IAR=1, PPC=16x16, htan10m',
#
#          'dtc = dte = 62.5 yr, BLS, htan20m, min!=max PPC, field prop. RR MMI',
#          'dtc = dte = 62.5 yr, CA, htan20m, min!=max PPC, field prop. RR MMI',
#          'dtc = dte = 62.5 yr, DWA, htan20m, min!=max PPC, field prop. RR MMI',
#          'dtc = dte = 62.5 yr, QLS, htan20m, min!=max PPC, field prop. RR MMI',
#
#          'dtc = dte = 62.5 yr, BLS, htan20m, min!=max PPC, field prop. RT',
#          'dtc = dte = 62.5 yr, CA, htan20m, min!=max PPC, field prop. RT',
#          'dtc = dte = 62.5 yr, DWA, htan20m, min!=max PPC, field prop. RT',
#          'dtc = dte = 62.5 yr, QLS, htan20m, min!=max PPC, field prop. RT',
#
#          'dtc = dte = 62.5 yr, BLS, htan20m, min!=max PPC, field prop. RT MMI',
#          'dtc = dte = 62.5 yr, CA, htan20m, min!=max PPC, field prop. RT MMI',
#          'dtc = dte = 62.5 yr, DWA, htan20m, min!=max PPC, field prop. RT MMI',
#          'dtc = dte = 62.5 yr, QLS, htan20m, min!=max PPC, field prop. RT MMI',

          'dtc = dte = 250 yr, BLS, htan10m, field prop. RT MMI',
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
linestyles = ['dashed', 'solid', 'solid', 'solid', 'solid', 'solid', 'solid', 'dashed', 'dashed', 'dashdot', 'dashed','dashed', 'dashdot', 'dotted',  'dotted','dotted'] 
# Set the marker styles (no markers in this case)
markers = ['', '', '', '', '', '', '', '', '', '', '', '', '', ''] 
dmark = 100

# Set up a row of two plots, one with the maximum beam depth
# and one with the min and max ve_stress_xx
fig = plt.figure(figsize=(10, 6))
ax = [fig.add_subplot(2, 1, i) for i in range(1, 3)]

yr_in_secs = 3600. * 24. * 365.2425
counter = 0 

# Create file path
for name in names: 
  path = base+name+tail

  # Read in the time, the maximum beam depth and min/max/ave ve_stress_xx.
  # The correct columns are selected with usecols.
  time,beam_depth,ve_xx_min,ve_xx_max,ve_xx_ave = np.genfromtxt(path, comments='#', usecols=(1,23,24,25,26), unpack=True)

  # Plot the beam depth in m against time in ky in
  # categorical batlow colors.
  ax[0].plot(time/1e3,beam_depth,label=labels[counter],color=colors[counter],linestyle=linestyles[counter],marker=markers[counter],markevery=dmark+counter)
  # Plot min and max stress (Pa) against time (ky).
  ax[1].plot(time/1e3,ve_xx_min,label=labels[counter],color=colors[counter],linestyle=linestyles[counter],marker=None)
  ax[1].plot(time/1e3,ve_xx_max,label=None,color=colors[counter],linestyle=linestyles[counter],marker=None)
  
  counter += 1

# Plot horizontal line at initial depth
ax[0].hlines(2812.5,0,50000,color='black',linestyle='dashed',label='original max depth',linewidth=1)

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

# Plot vertical line at t=50 ky, when gravity is switched off.
ax[0].vlines(50,4000,2000,color='black',linestyle='dotted',linewidth=1)

# Labelling of plot
ax[1].set_xlabel("Time [ky]")
ax[0].set_ylabel(r"Maximum beam depth [m]")
ax[1].set_ylabel(r"$\tau^0_{cxx}$ min/max [Pa]")
# Place legend
ax[0].legend(loc='lower right',ncol=1,handlelength=4)
# Grid and tickes
ax[0].grid(axis='x',color='0.95')
#ax[0].set_yticks([0,1000,2000,3000,4000])
ax[0].grid(axis='y',color='0.95')
ax[1].grid(axis='x',color='0.95')
ax[1].grid(axis='y',color='0.95')
#ax[1].set_yticks([0,2,4,6,8,10])

# Ranges of the axes
ax[0].set_xlim(0,350) # kyr
ax[0].set_ylim(3250,2750) # m
ax[1].set_xlim(0,350) # kyr
ax[1].set_ylim(-0.75e9,0.75e9) # %

# Add labels a) and b)
ax[0].text(-25,2750,"a)")
ax[1].text(-25,0.75e9,"b)")

plt.tight_layout()

# Save as pdf
filename = '5_viscoelastic_bending_beam_dte_particles_isnot_dtc_depth_dtcisdte_smoothing_250_250_fieldpropRR_main.png'
plt.savefig(filename, dpi=300)
print ('Plot in: ' + filename)
