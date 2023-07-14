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
base = r"/Users/acglerum/Documents/Postdoc/SB_CRYSTALS/HLRN/HLRN/fix_stresses_elasticity/paper_11072022/BM2/"

# Change file name modifiers as needed depending on your file structure
# Always start with largest dte, largest dtc
names = [
         "ve_build-up_dtc2500_dte2500_GR0",
         "ve_build-up_dtc500_dte500_GR0",
         "ve_build-up_dtc250_dte250_GR0",
         "ve_build-up_dtc125_dte125_GR0",
         "ve_build-up_dtc25_dte25_GR0",
        ]
tail = r"/statistics"

# The labels the graphs will get in the plot
labels = [
          't = 10 ky',
          't = 100 ky',
          't = 150 ky',
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

# Create list for error per timestep size for each timestep
errors_10000 = []
errors_100000 = []
errors_200000 = []
dtes = []
dtcs = []

# Create file path
for name in names: 
  path = base+name+tail
  # find the elastic timestep
  dte = name.split("dte")[-1].split("_")[0]
  dtes.append(float(dte))
  # find the computational timestep
  dtc = name.split("dtc")[-1].split("_")[0]
  dtcs.append(float(dtc))

  # Read in the time and the minimum xx and yy components of the viscoelastic stress,
  # which are stored on the fields ve_stress_xx and ve_stress_yy.
  # The correct columns are selected with usecols.
  time,stress_xx_min = np.genfromtxt(path, comments='#', usecols=(1,18), unpack=True)

  # Error at t = 10000 yr
  index_10000 = np.where(time == 10000)[0]
  errors_10000.append(abs(stress_xx_min[index_10000]-tau_xx_analytical(time[index_10000]))/tau_xx_analytical(time[index_10000])*100.)

  # Error at t = 100000 yr
  index_100000 = np.where(time == 100000)[0]
  errors_100000.append(abs(stress_xx_min[index_100000]-tau_xx_analytical(time[index_100000]))/tau_xx_analytical(time[index_100000])*100.)

  # Error at t = 150000 yr
  index_200000 = np.where(time == 150000)[0]
  errors_200000.append(abs(stress_xx_min[index_200000]-tau_xx_analytical(time[index_200000]))/tau_xx_analytical(time[index_200000])*100.)

nr_dtes = len(set(dtes)) 
unique_dtes = set(dtes)
counter = 0
prev_dte = dtes[0]
n_dte500 = dtes.count(500)
n_dte250 = dtes.count(250)
print ("dtes", dtes)
print ("Occurrences of dte500", n_dte500)
print ("Occurrences of dte250", n_dte250)
dte500_dtc = []
dte500_error10000 = []
dte500_error100000 = []
dte500_error200000 = []
dte250_dtc = []
dte250_error10000 = []
dte250_error100000 = []
dte250_error200000 = []
for i in np.arange(0,n_dte500):
  dte500_dtc.append(dtcs[i])
  dte500_error10000.append(errors_10000[i])
  dte500_error100000.append(errors_100000[i])
  dte500_error200000.append(errors_200000[i])
for i in np.arange(n_dte500,n_dte500+n_dte250):
  dte250_dtc.append(dtcs[i])
  dte250_error10000.append(errors_10000[i])
  dte250_error100000.append(errors_100000[i])
  dte250_error200000.append(errors_200000[i])
   
x = np.array([2500,500,250,125,62.5])
def y(a,b):
  return a+b*x

# Labelling of plot
ax[0].set_xlabel("Computational = elastic timestep size [yr]")
ax[0].set_ylabel(r"Error [%]")
ax[0].set_title(r"BM2: Error per computational timestep size for different elastic timestep sizes and at different timesteps")
# Place legend
ax[0].legend(loc='upper right',ncol=1,handlelength=4)
# Grid and tickes
ax[0].grid(axis='x',color='0.95')
ax[0].grid(axis='y',color='0.95')
ax[0].set_yticks([0,1,2,3,4,5])

# Ranges of the axes
ax[0].set_xlim(2550,0) # yr
ax[0].set_ylim(-0.1,4.0) # %

# Add labels
#ax[0].text(-15,21,"a)")

#plt.tight_layout()

# Also plot on normal scale instead of loglog
ax[0].plot(x,errors_10000,label=labels[0],color=colors[0],linestyle=linestyles[0],marker=markers[0])
ax[0].plot(x,errors_100000,label=labels[1],color=colors[1],linestyle=linestyles[1],marker=markers[1])
ax[0].plot(x,errors_200000,label=labels[2],color=colors[2],linestyle=linestyles[2],marker=markers[2])

# Place legend
ax[0].legend(loc='upper right',ncol=1,handlelength=4)
# Save as png
plt.savefig('2_viscoelastic_build-up_dte_isnot_dtc_fields_dtcisdte_error_per_timestep.png')    

# Plot on loglog scale
# B = order
# A = y0/x0^B
def f(x, A, B):
    return A*x**B
x2 = np.array([5000,2500,500,250,125,62.5,1])
ax[0].plot(x2,f(x2,0.002,0.5),label="0.5 order",color="black",linestyle="dotted",linewidth=1)
ax[0].plot(x2,f(x2,4e-5,1),label="1st order",color="black",linestyle="dashed",linewidth=1)
ax[0].plot(x2,f(x2,1.6e-8,2),label="2nd order",color="black",linestyle="dashdot",linewidth=1)
plt.semilogx()
plt.semilogy()
# Place legend
ax[0].set_yticks([1e-4,1e-3,1e-2,1e-1,1e0,1e1])
ax[0].legend(loc='upper right',ncol=1,handlelength=4)
# Ranges of the axes
ax[0].set_xlim(3e3,3e1) # yr
ax[0].set_ylim(1e-4,5e1) # %
# Save as png
plt.savefig('2_viscoelastic_build-up_dte_isnot_dtc_fields_dtcisdte_error_per_timestep_loglog.png')    
