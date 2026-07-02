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
rc("lines", linewidth=3, markersize=10)

# Change path as needed
base = r"/Users/acglerum/Documents/Postdoc/SB_CRYSTALS/HLRN/HLRN/fix_stresses_elasticity/paper_14072023/BM4/"

# Always start with largest dt
names = [
         "ve_sheared_torsion_particles_interpolatorcell_average_dtc0.02_dte0.02_GR2_np4",
         "ve_sheared_torsion_particles_interpolatorcell_average_dtc0.01_dte0.01_GR2_np4",
         "ve_sheared_torsion_particles_interpolatorcell_average_dtc0.005_dte0.005_GR2_np4",
         "ve_sheared_torsion_particles_interpolatorcell_average_dtc0.0025_dte0.0025_GR2_np4",
        ]
tail = r"/statistics"

# The labels the graphs will get in the plot
labels = [
          't = 0.1 s',
          't = 0.4 s',
          't = 0.8 s',
          't = 0.1 s, dt = 250 yr',
          't = 0.4 s, dt = 250 yr',
          't = 0.8 s, dt = 250 yr',
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
# Set the marker styles
markers = ['o', 'v', 's', 'o', 'v', 's', '', '', '', '', '', '', '', ''] 

# Set up a row of one plot
fig = plt.figure(figsize=(10, 3.9))
ax = [fig.add_subplot(1, 1, i) for i in range(1, 2)]

yr_in_secs = 3600. * 24. * 365.2425
counter = 0 

# The analytical solution:
# Return stress in Pa.
def tau_xz_analytical(t):
    V=0.3
    mu=1e2
    eta_v=1e2
    h=1
    C1 = -(V*V*eta_v*eta_v*mu)/(mu*mu*h*h+V*V*eta_v*eta_v)
    C2 = -(V*h*eta_v*mu*mu)/(mu*mu*h*h+V*V*eta_v*eta_v)
    # at 0.5, shearing stops
    tmax=0.5
    return np.where(t<=tmax, \
    np.exp(-mu/eta_v*t)   *(C2*np.cos(V*t/h)   -C1*np.sin(V*t/h))-C2, \
    (np.exp(-mu/eta_v*tmax)*(C2*np.cos(V*tmax/h)-C1*np.sin(V*tmax/h))-C2)*np.exp(-mu/eta_v*(t-tmax)))


# Create list for error per timestep size for each timestep
errors_01 = []
errors_04 = []
errors_08 = []
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

  # Read in the time and the average xz component of the viscoelastic stress,
  # which is stored on the field ve_stress_xz.
  # The correct columns are selected with usecols (counting starts from 0).
  time,stress_xz_ave = np.genfromtxt(path, comments='#', usecols=(1,29), unpack=True)

  # Error at t = 0.1 s
  index_01 = np.where(time == 0.1)[0]
  errors_01.append(abs(stress_xz_ave[index_01]-tau_xz_analytical(time[index_01]))/tau_xz_analytical(time[index_01])*100.)

  # Error at t = 0.4 s
  index_04 = np.where(time == 0.4)[0]
  errors_04.append(abs(stress_xz_ave[index_04]-tau_xz_analytical(time[index_04]))/tau_xz_analytical(time[index_04])*100.)

  # Error at t = 0.8 s
  index_08 = np.where(time == 0.8)[0]
  errors_08.append(abs(stress_xz_ave[index_08]-tau_xz_analytical(time[index_08]))/tau_xz_analytical(time[index_08])*100.)

nr_dtes = len(set(dtes)) 
unique_dtes = set(dtes)
counter = 0
prev_dte = dtes[0]
n_dte002 = dtes.count(0.02)
n_dte001 = dtes.count(0.01)
n_dte0005 = dtes.count(0.005)
n_dte00025 = dtes.count(0.0025)
print ("dtes", dtes)
print ("Occurrences of dte = 0.02", n_dte002)
print ("Occurrences of dte = 0.01", n_dte001)
   
x = np.array([0.02,0.01,0.005,0.0025])
def y(a,b):
  return a+b*x

# Labelling of plot
ax[0].set_xlabel("Time step size [s]")
ax[0].set_ylabel(r"Error E [%]")
#ax[0].set_title(r"BM2: Error per computational timestep size for different elastic timestep sizes and at different timesteps")
# Place legend
ax[0].legend(loc='upper right',ncol=1,handlelength=4)
# Grid and tickes
ax[0].grid(axis='x',color='0.95')
ax[0].grid(axis='y',color='0.95')
#ax[0].set_xticks([500,400,300,250,200,125,100,62.5,0])
##ax[0].set_yticks([0,0.5,1])

# Ranges of the axes
##ax[0].set_xlim(550,0) # yr
##ax[0].set_ylim(-0.1,0.8) # %

# Add labels
#ax[0].text(-15,21,"a)")

#plt.tight_layout()

# Also plot on normal scale instead of loglog
ax[0].plot(x,errors_01,label=labels[0],color=colors[0],linestyle=linestyles[0],marker=markers[0])
ax[0].plot(x,errors_04,label=labels[1],color=colors[1],linestyle=linestyles[1],marker=markers[1])
ax[0].plot(x,errors_08,label=labels[2],color=colors[2],linestyle=linestyles[2],marker=markers[2])

# Place legend
##ax[0].legend(loc='upper right',ncol=1,handlelength=4)
# Save as png
##plt.savefig('2_viscoelastic_build-up_dte_isnot_dtc_fields_dtcisdte_error_per_timestep.png', dpi=300)

# Plot on loglog scale
# B = order
# A = y0/x0^B
def f(x, A, B):
    return A*x**B
x2 = np.array([0.05,0.01,0.005,0.001,0.0001])
ax[0].plot(x2,f(x2,4,0.5),label="0.5 order",color="black",linestyle="dotted",linewidth=1)
ax[0].plot(x2,f(x2,40,1),label="1st order",color="black",linestyle="dashed",linewidth=1)
#ax[0].plot(x2,f(x2,2200,2),label="2nd order",color="black",linestyle="dashdot",linewidth=1)
plt.semilogx()
plt.semilogy()
# Place legend
ax[0].set_xticks([0.02,0.01,0.005,0.0025,0.001],[r"$2\cdot10^{-2}$",r"$10^{-2}$",r"$5\cdot10^{-3}$",r"$2.5\cdot10^{-3}$",r"$10^{-3}$"])
ax[0].set_yticks([1e-3,1e-2,1e-1,1e0,1e1])
ax[0].legend(loc='lower right',ncol=1,handlelength=4)
# Ranges of the axes
ax[0].set_xlim(9e-4,4e-2) # yr
ax[0].set_ylim(1e-2,3) # %
# Add labels
ax[0].text(2950,2,"c)")

# Save as png
plt.savefig('4_viscoelastic_sheared_torsion_particles_dtc_isnot_dte_error_per_timestep_loglog.png', dpi=300)
