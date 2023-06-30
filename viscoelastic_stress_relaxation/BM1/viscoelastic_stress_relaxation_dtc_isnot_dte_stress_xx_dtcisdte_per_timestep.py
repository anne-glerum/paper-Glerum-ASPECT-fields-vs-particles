# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 by Anne Glerum
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes 
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
#import scipy.optimize as sio
rc("pdf", fonttype=42)
rc("lines", linewidth=3, markersize=8)

# Change path as needed
base = r"/Users/acglerum/Documents/Postdoc/SB_CRYSTALS/HLRN/HLRN/fix_stresses_elasticity/paper_11072022/BM1/"

# Change file name modifiers as needed depending on your file structure
# Always start with largest dte, largest dtc
names = [
         "ve_relaxation_dtc25_dte25_GR0_g0",
         "ve_relaxation_dtc125_dte125_GR0_g0",
         "ve_relaxation_dtc250_dte250_GR0_g0",
         "ve_relaxation_dtc500_dte500_GR0_g0",
         "ve_relaxation_dtc2500_dte2500_GR0_g0",
        ]
tail = r"/statistics"

# The labels the graphs will get in the plot
labels = [
          't = 10 ky',
          't = 100 ky',
          't = 200 ky',
          't = 10 ky, dte = 250 yr',
          't = 100 ky, dte = 250 yr',
          't = 200 ky, dte = 250 yr',
         ]

# Set the colors available for plotting
color1=[0.0051932, 0.098238, 0.34984]
color2=[0.092304, 0.32922, 0.38504]
color3=[0.32701, 0.4579, 0.28638]
color4=[0.67824, 0.55071, 0.1778]
color5=[0.97584, 0.63801, 0.50183]
color6=[0.98447, 0.78462, 0.93553]
colors = [color2, color4, color5, color6, color6, color6, color5, color3, color4, color5]
# Set the line styles
linestyles = ['solid', 'solid', 'solid', 'solid', 'solid', 'solid', 'dashdot', 'dotted',  'dotted','dotted'] 
# Set the marker styles (no markers in this case)
markers = ['o', 'v', 's', 'o', 'v', 's', '', '', '', '', '', '', '', ''] 

# Set up a row of two plots, one with absolute stress values
# and one with the percentage difference to the analytical solution
fig = plt.figure(figsize=(10, 6))
ax = [fig.add_subplot(1, 1, i) for i in range(1, 2)]

yr_in_secs = 3600. * 24. * 365.2425
counter = 0 

# Create list for error per timestep size for each timestep
errors_10000 = []
errors_100000 = []
errors_200000 = []

# Create file path
for name in names: 
  path = base+name+tail

  # Read in the time and the minimum xx and yy components of the viscoelastic stress,
  # which are stored on the fields ve_stress_xx and ve_stress_yy.
  # The correct columns are selected with usecols.
  time,stress_xx_min = np.genfromtxt(path, comments='#', usecols=(1,18), unpack=True)

  # Error at t = 10000 yr
  index_10000 = np.where(time == 10000)[0]
  errors_10000.append( (stress_xx_min[index_10000]-(20e6*np.exp(-1e10*time[index_10000]*yr_in_secs/1e22)))/(20e6*np.exp(-1e10*time[index_10000]*yr_in_secs/1e22))*100.)

  # Error at t = 100000 yr
  index_100000 = np.where(time == 100000)[0]
  errors_100000.append((stress_xx_min[index_100000]-(20e6*np.exp(-1e10*time[index_100000]*yr_in_secs/1e22)))/(20e6*np.exp(-1e10*time[index_100000]*yr_in_secs/1e22))*100.)

  # Error at t = 200000 yr
  index_200000 = np.where(time == 200000)[0]
  errors_200000.append((stress_xx_min[index_200000]-(20e6*np.exp(-1e10*time[index_200000]*yr_in_secs/1e22)))/(20e6*np.exp(-1e10*time[index_200000]*yr_in_secs/1e22))*100.)

x = np.array([25,125,250,500,2500])
def y(a,b):
  return a-b*x

def exp_lines(a,x,b):
  return a * x ** b

# Labelling of plot
ax[0].set_xlabel("Computational = elastic time step size [yr]")
ax[0].set_ylabel(r"Error [%]")
ax[0].set_title(r"BM1: Error per timestep size at different time steps")
# Grid and tickes
ax[0].grid(axis='x',color='0.95')
ax[0].grid(axis='y',color='0.95')
ax[0].set_xticks([25,125,250,500,1000,1500,2000,2500])
ax[0].set_yticks([0,5,10,15,20,25])

# Ranges of the axes
ax[0].set_xlim(2550,0) # yr
ax[0].set_ylim(0,30) # %

# Add labels
#ax[0].text(-15,21,"a)")

#plt.tight_layout()

# Plot on normal scale
ax[0].plot(x,errors_10000,label=labels[0],color=colors[0],linestyle=linestyles[0],marker=markers[0])
ax[0].plot(x,errors_100000,label=labels[1],color=colors[1],linestyle=linestyles[1],marker=markers[1])
ax[0].plot(x,errors_200000,label=labels[2],color=colors[2],linestyle=linestyles[2],marker=markers[2])
# Compute best fits for the dte500 lines & plot
theta_10000 = np.polyfit(x,errors_10000,2)
theta_100000 = np.polyfit(x,errors_100000,3)
theta_200000 = np.polyfit(x,errors_200000,4)
#ax[0].plot(x,y(theta_10000[1],theta_10000[0]),label="y="+str(theta_10000[1])+"+"+str(theta_10000[0])+"x",color="black",linestyle="dashed",linewidth=1,marker=markers[0])
#ax[0].plot(x,y(theta_100000[1],theta_100000[0]),label="y="+str(theta_100000[1])+"+"+str(theta_100000[0])+"x",color="black",linestyle="dashed",linewidth=1,marker=markers[1])
#ax[0].plot(x,y(theta_200000[1],theta_200000[0]),label="y="+str(theta_200000[1])+"+"+str(theta_200000[0])+"x",color="black",linestyle="dashed",linewidth=1,marker=markers[2])
#ax[0].plot(x,exp_lines(0,x,2),label="exp(2)",color="black",linestyle="dashed")
def f(x, A, B):
    return A*x**B
def logf(x, m, B):
    return m*np.log(x)+np.log(B)
#ax[0].plot(x,f(x,0.0001,2),label="2",color="black",linestyle="dashed",linewidth=1,marker=markers[0])
# Place legend
ax[0].legend(loc='upper right',ncol=1,handlelength=4)
# Save as png
plt.savefig('1_viscoelastic_relaxation_dte_isnot_dtc_fields_error_dtcisdte_per_timestep.png')    

# Plot on loglog scale
ax[0].plot(x,f(x,0.01,1),label="1st order",color="black",linestyle="dashed",linewidth=1)
plt.semilogx()
plt.semilogy()
# Place legend
ax[0].legend(loc='upper right',ncol=1,handlelength=4)
ax[0].set_yticks([1e-1,1e0,1e1])
# Ranges of the axes
ax[0].set_xlim(3e3,2e1) # yr
ax[0].set_ylim(1e-2,5e1) # %
# Save as png
plt.savefig('1_viscoelastic_relaxation_dte_isnot_dtc_fields_error_dtcisdte_per_timestep_loglog.png')    

