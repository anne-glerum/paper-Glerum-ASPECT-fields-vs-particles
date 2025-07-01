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
rc("legend", fontsize=8)

# Change path as needed
base = r"/Users/acglerum/Documents/Postdoc/SB_CRYSTALS/Papers/Glerum_LD_ASPECT/repo/9_3D_loading/postprocessing_scripts/"

names = [
         "RL9_viscoelastic_3D_loading_particles_AMG_avegeometric_intbilinear_least_squares_limTrue_dtc2.5_dte2.5_IGR1_IAR2_np4",
        ]
tail = r"/topography"

# The labels the graphs will get in the plot
labels = [
          'AMG, geom, BLS, dtc = dte = 2.5 yr',
          'dtc = 250 yr, dte = 500 yr',
          'dtc = 125 yr, dte = 500 yr',
          'dtc = 250 yr, dte = 250 yr',
          'dtc = 125 yr, dte = 250 yr',
          'dtc = 62.5 yr, dte = 250 yr',
         ]
# Set the colors available for plotting
color1=[0.0051932, 0.098238, 0.34984]
color2=[0.092304, 0.32922, 0.38504]
color3=[0.32701, 0.4579, 0.28638]
color4=[0.67824, 0.55071, 0.1778]
color5=[0.97584, 0.63801, 0.50183]
color6=[0.98447, 0.78462, 0.93553]
colors = [color1, color2, color3, color4, color5, color6, 'black', 'blue', color3, color4, color5]
# Set the line styles
linestyles = ['solid', 'solid', 'solid', 'dashed', 'dashed', 'dashed', 'dashed','dashdot', 'dashdot', 'dotted',  'dotted','dotted'] 
# Set the marker styles (no markers in this case)
markers = ['', '', '', '', '', '', '', '', '', '', '', '', '', ''] 
dmark = 100

############# START TABOO #############

# Set parameters for loading analytical TABOO data
# For different pairs of (lon, colat), the radial
# displacement u_rad [m] is listed for each 2.5 yr 
# (0.0025 ky; 1st column) as the 2nd column.
R = 6371.0 # Earth radius analytical model [km]

t_start = 0.0 # start time [ka]
t_end   = 0.2 # end time [ka]
t_step  = 0.0025 # time step size [ka]
n_taboo_time = int(t_end / t_step + 1)
print ("Nr of TABOO timesteps: ", n_taboo_time)

# The center of the load is at (lon,colat) = (0,0).
colat_start = 0.0  # start observer locations co-latitude [degree]
colat_end   = 5.0  # end observer locations co-latitude [degree]
colat_step  = 0.01 # observer locations co-latitude step size

taboo_time = np.arange(t_start,t_end+t_step,t_step)
taboo_colat = np.arange(colat_start,colat_end+colat_step,colat_step) # observer locations co-latitude [degree]
taboo_loc = taboo_colat/360.*2.*np.pi*R # observer locations distance from pole [km]

# load analytical data TABOO
print ("Loading TABOO data")
taboo_dir = base + "ABAQUS_TABOO/taboo/"
taboo_displacement = np.genfromtxt(taboo_dir+"disp.his",comments='#', usecols=(0,1))
# Get the maximum deflection at each timestep,
# i.e. the deflection at (0,0) over time. 
# NB the max deflection of -0.7514 m at 200 yr is actually at
# (0,0.04). The deflection at (0,0) at that time is -0.7505. IGNORE.
taboo_max_deflection =  taboo_displacement[0:n_taboo_time]

############# END TABOO #############

############# START ABAQUS #############

# load numerical data ABAQUS
# There is a datafile for every 5 yr. The file consists of x y ? topo
# data columns. The domain is 4 times the ASPECT domain, as it is not
# axisymmetric, and therefore cannot be limited to a quarter of the domain.
# The horizontal dimensions run from 0 to 3000 km, so the center
# of the load is at (1500 km, 1500 km).
abaqus_t_end = 200 # yr
abaqus_dt = 5 # yr
abaqus_time = np.arange(0,abaqus_t_end+abaqus_dt,abaqus_dt)
abaqus_max_deflection = np.zeros(int(abaqus_t_end/abaqus_dt+1))
abaqus_dir = base + "ABAQUS_TABOO/abaqus/"
print ("Loading Abaqus data")
for i, time in enumerate(abaqus_time):
  abaqus_displacement = np.genfromtxt(abaqus_dir+"incomp_flat_FE_U3_E_"+str(time)+"yr.dat",usecols=(0,1,3))
  abaqus_max_deflection[i] = np.min(abaqus_displacement[:,2])
  # check that the maximum deflection is always in the center:
  #print("Index Abaqus min: ", i, np.argmin(abaqus_displacement[:,2]))

############# END ABAQUS #############

# Set up a row of two plots, one with the maximum beam depth
# and one with the min and max ve_stress_xx
fig = plt.figure(figsize=(10, 6))
ax = [fig.add_subplot(2, 1, i) for i in range(1, 3)]

counter = 0 
dtc = 2.5
end_time = 200
dt_output = 5

# Create file path
for model_index, name in enumerate(names): 
  path = base+name+tail

  print ("Model: ", base+name)

  if 'dtc5.0' in name:
    dtc = 5.0
  elif 'dtc10.0' in name:
    dtc = 10.0
  elif 'dtc15.0' in name:
    dtc = 15.0
  elif 'dtc20.0' in name:
    dtc = 20.0

  n_output = int(end_time / dt_output) + 1
  max_deflection = np.zeros(n_output)
  print ("N output steps: ", n_output)
  time = np.arange(0,end_time + dt_output, dt_output)

  # Loop over all topo files and get the max deflection at each output timestep
  # Topo file: x y z topo
  for i, j in enumerate(np.arange(0,int(end_time/dtc+1), int(dt_output/dtc))):
    if j < 10:
      file_path = path + ".0000" + str(j)
    else:
      file_path = path + ".000" + str(j)

    topography = np.genfromtxt(file_path, comments='#', usecols=(3), unpack=True)
    max_deflection[i] = np.min(topography)
  print ("Max ASPECT deflection: ", np.min(max_deflection))

  # Plot the maximum deflection in m against time in yr in
  # categorical batlow colors.
  ax[0].plot(time,max_deflection,label=labels[model_index],color=colors[model_index],linestyle=linestyles[model_index],marker=markers[model_index],markevery=dmark+model_index)

  # Plot the difference in maximum deflection between ASPECT and TABOO in % 
  # against time in yr in categorical batlow colors.
  # First get the TABOO deflection at the same timesteps (dt_output).
  sampled_taboo_max_deflection = taboo_max_deflection[0::int(dt_output/dtc)].copy()
  print ("Max TABOO deflection: ", np.min(sampled_taboo_max_deflection[:,1]))
  ax[1].plot(time,(max_deflection - sampled_taboo_max_deflection[:,1])/sampled_taboo_max_deflection[:,1]*100,label=labels[model_index],color=colors[model_index],linestyle=linestyles[model_index],marker=markers[model_index],markevery=dmark+model_index)

# Plot horizontal line at initial depth
ax[0].hlines(0,-100,500,color='black',linestyle='dashed',label='surface t = 0 yr',linewidth=1)

# Plot vertical line at t=50 ky, when gravity is switched off.
ax[0].vlines(100,-10,10,color='black',linestyle='dotted',label='end increase load',linewidth=1)

# Plot TABOO max deflection over time.
ax[0].plot(1000*taboo_max_deflection[:,0],taboo_max_deflection[:,1],label="TABOO",color="blue",linestyle="dashed",marker='^',markevery=10,markersize=6,linewidth=1)

# Plot Abaqus max deflection over time.
ax[0].plot(abaqus_time,abaqus_max_deflection,label="Abaqus",color="green",linestyle="dashed",marker='+',markevery=10,markersize=6,linewidth=1)

# Labelling of plot
ax[0].set_xlabel("Time [yr]")
ax[1].set_xlabel("Time [yr]")
ax[0].set_ylabel(r"Maximum deflection [m]")
ax[1].set_ylabel(r"Error maximum deflection")
# Place legend
ax[0].legend(loc='center right',ncol=2,handlelength=4)
# Grid and tickes
ax[0].grid(which='major')
ax[0].grid(axis='x',color='0.95')
#ax[0].set_yticks([0,1000,2000,3000,4000])
ax[0].grid(axis='y',color='0.95')
ax[1].grid(axis='x',color='0.95')
ax[1].grid(axis='y',color='0.95')
#ax[1].set_yticks([0,2,4,6,8,10])

# # Ranges of the axes
ax[0].set_xlim(-5,205) # yr
ax[0].set_ylim(-0.85,0.05) # m
ax[1].set_xlim(-5,205) # yr
ax[1].set_ylim(-0.3,5) # %

# Add labels a) and b)
ax[0].text(-20,0.05,"a)")
ax[1].text(-20,3,"b)")

plt.tight_layout()

# Save as png
filename = base + '9_3D_loading_max_deflection.png'
plt.savefig(filename, dpi=300)
print ('Plot in: ' + filename)