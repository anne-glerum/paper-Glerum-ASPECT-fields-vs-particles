# -*- coding: utf-8 -*-
"""
Created on Wed July 13 by Anne Glerum
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes 
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
rc("pdf", fonttype=42)
rc("lines", linewidth=5, markersize=15)

# Change path as needed
base = r"/Users/acglerum/Documents/Postdoc/SB_CRYSTALS/HLRN/HLRN/fix_stresses_elasticity/paper_11072022/"

# Change file name modifiers as needed depending on your file structure
names = [
         "surface_topography_diffusion_zero_flux_dt0.002_GR4",
         "surface_topography_diffusion_zero_flux_dt0.002_GR5",
         "surface_topography_diffusion_zero_flux_dt0.002_GR6",
         "surface_topography_diffusion_zero_flux_dt0.001_GR4",
         "surface_topography_diffusion_zero_flux_dt0.001_GR5",
         "surface_topography_diffusion_zero_flux_dt0.001_GR6",
         "surface_topography_diffusion_zero_flux_dt0.0005_GR4",
         "surface_topography_diffusion_zero_flux_dt0.0005_GR5",
         "surface_topography_diffusion_zero_flux_dt0.0005_GR6",
        ]
tail = r"/statistics"
tail_topo = r"/topography"

# The labels the graphs will get in the plot
labels = [
          'dt = 0.002 s, dh = 0.0625 m',
          'dt = 0.002 s, dh = 0.03125 m',
          'dt = 0.002 s, dh = 0.015625 m',
          'dt = 0.001 s, dh = 0.0625 m',
          '',
          '',
          'dt = 0.0005 s, dh = 0.0625 m',
          '',
          '',
         ]
labels_error = [
          '',
          '',
          '',
          '',
          'dt = 0.001 s, dh = 0.03125 m',
          'dt = 0.001 s, dh = 0.015625 m',
          '',
          'dt = 0.0005 s, dh = 0.03125 m',
          'dt = 0.0005 s, dh = 0.015625 m',
         ]
# Set the colors available for plotting
color1=[0.0051932, 0.098238, 0.34984]
color2=[0.092304, 0.32922, 0.38504]
color3=[0.32701, 0.4579, 0.28638]
color4=[0.67824, 0.55071, 0.1778]
color5=[0.97584, 0.63801, 0.50183]
color6=[0.98447, 0.78462, 0.93553]
colors = [color1, color3, color5, color1, color3, color5, color1, color3, color5]
# Set the line styles
linestyles = ['solid', 'solid', 'solid', 'dashed', 'dashed', 'dashed', 'dotted', 'dotted', 'dotted'] 
# Set the marker styles (no markers in this case)
markers = ['', '', '', '', '', '', '', '', ''] 
# Only plot every nth marker
dmark=15

# Set up a column of three plots, one with the full topography over time,
# one with the maximum topography over time (i.e. the topography at x = 0.5)
# and one with the percentage difference to the analytical solution for the maximum topography at x = 0.5.
fig = plt.figure(figsize=(10, 9))
ax = [fig.add_subplot(3, 1, i) for i in range(1, 4)]

# Also plot a zoom-in of the topography
zoom_x_min = 0.45
zoom_x_max = 0.50
zoom_y_min = 0.057
zoom_y_max = 0.061
axins = zoomed_inset_axes(ax[0], 4, loc = "upper right") # zoom = 4
axins.set_xlim(zoom_x_min, zoom_x_max)
axins.set_ylim(zoom_y_min, zoom_y_max)
mark_inset(ax[0], axins, loc1=1, loc2=4, fc="none", ec="0.5")

counter = 0 

# The analytical solution.
# Return topography at the center x-coordinate in m.
def topo_analytical(xc,time):
    topo = 0
    amplitude = 0.075
    domain_width = 1
    n_max = 5000
    kappa = 0.25
    # Fill another array of the size of time
    # with the x-coordinate so that x and time
    # have the same dimension.
    x = np.full((np.size(time)), xc)
    sum = 0.
    for n in range(1, n_max+1):
      sum += np.cos(2.*n*np.pi*x/domain_width) * np.exp(-kappa*4.*n*n*np.pi*np.pi*time/(domain_width*domain_width)) / ((4.*n*n)-1.) * (-4.*amplitude/np.pi);
      # a0=4A/pi --> a0/2=2A/pi
    topo = 2. * amplitude / np.pi + sum;

    return topo


for name in names: 
  # Create file path
  path = base+name+tail
  path_topo = base+name+tail_topo

  # Read in the time and the maximum topography.
  # The correct columns are selected with usecols (counting starts from 0).
  if 'particle' in name:
    time,max_topo = np.genfromtxt(path, comments='#', usecols=(1,19), unpack=True)
  else:
    time,max_topo = np.genfromtxt(path, comments='#', usecols=(1,19), unpack=True)

  # Plot the topography at the center of the domain against time in s in
  # categorical batlow colors.
  ax[1].plot(time,max_topo,label=None,color=colors[counter],linestyle=linestyles[counter],marker=markers[counter],markevery=dmark)
  ax[2].plot(time,(max_topo-topo_analytical(0.5,time))/topo_analytical(0.5,time)*100.,label=labels_error[counter],color=colors[counter],linestyle=linestyles[counter],marker=markers[counter],markevery=dmark)
 
  if '0.002' in name:
    x,topo = np.genfromtxt(path_topo+".00000", comments='#', usecols=(0,1), unpack=True)
    # Plot the topography along the surface of the domain, subtract domain height
    ax[0].plot(x,topo-1,label=labels[counter],color=colors[counter],linestyle=linestyles[counter],marker=markers[counter],markevery=dmark)

    x,topo = np.genfromtxt(path_topo+".00025", comments='#', usecols=(0,1), unpack=True)
    # Plot the topography along the surface of the domain, subtract domain height
    ax[0].plot(x,topo-1,label=None,color=colors[counter],linestyle=linestyles[counter],marker=markers[counter],markevery=dmark)

    x,topo = np.genfromtxt(path_topo+".00050", comments='#', usecols=(0,1), unpack=True)
    # Plot the topography along the surface of the domain 
    ax[0].plot(x,topo-1,label=None,color=colors[counter],linestyle=linestyles[counter],marker=markers[counter],markevery=dmark)
    axins.plot(x,topo-1,label=None,color=colors[counter],linestyle=linestyles[counter],marker=markers[counter],markevery=dmark)
  elif '0.001' in name:
    x,topo = np.genfromtxt(path_topo+".00000", comments='#', usecols=(0,1), unpack=True)
    # Plot the topography along the surface of the domain 
    ax[0].plot(x,topo-1,label=labels[counter],color=colors[counter],linestyle=linestyles[counter],marker=markers[counter],markevery=dmark)

    x,topo = np.genfromtxt(path_topo+".00050", comments='#', usecols=(0,1), unpack=True)
    # Plot the topography along the surface of the domain 
    ax[0].plot(x,topo-1,label=None,color=colors[counter],linestyle=linestyles[counter],marker=markers[counter],markevery=dmark)

    x,topo = np.genfromtxt(path_topo+".00100", comments='#', usecols=(0,1), unpack=True)
    # Plot the topography along the surface of the domain 
    ax[0].plot(x,topo-1,label=None,color=colors[counter],linestyle=linestyles[counter],marker=markers[counter],markevery=dmark)
    axins.plot(x,topo-1,label=None,color=colors[counter],linestyle=linestyles[counter],marker=markers[counter],markevery=dmark)
  elif '0.0005' in name:
    x,topo = np.genfromtxt(path_topo+".00000", comments='#', usecols=(0,1), unpack=True)
    # Plot the topography along the surface of the domain 
    ax[0].plot(x,topo-1,label=labels[counter],color=colors[counter],linestyle=linestyles[counter],marker=markers[counter],markevery=dmark)

    x,topo = np.genfromtxt(path_topo+".00100", comments='#', usecols=(0,1), unpack=True)
    # Plot the topography along the surface of the domain 
    ax[0].plot(x,topo-1,label=None,color=colors[counter],linestyle=linestyles[counter],marker=markers[counter],markevery=dmark)

    x,topo = np.genfromtxt(path_topo+".00200", comments='#', usecols=(0,1), unpack=True)
    # Plot the topography along the surface of the domain 
    ax[0].plot(x,topo-1,label=None,color=colors[counter],linestyle=linestyles[counter],marker=markers[counter],markevery=dmark)
    axins.plot(x,topo-1,label=None,color=colors[counter],linestyle=linestyles[counter],marker=markers[counter],markevery=dmark)
  else:
    print ("Timestep not accounted for")

  counter += 1

# Plot the analytical solution in Pa.
ax[1].plot(time,topo_analytical(0.5,time),label='analytical',color='black',linestyle='dashdot')
#axins.plot(time,topo_analytical(0.5,time),label='analytical',color='black',linestyle='dashdot')

# Labelling of plot
ax[0].set_xlabel("X [m]")
ax[0].xaxis.set_label_coords(.5,-0.1)
ax[0].set_ylabel(r"Topography [m]")
ax[2].set_xlabel("Time [s]")
ax[1].set_ylabel(r"Topography at x = 0.5 [m]")
ax[2].set_ylabel(r"Error at x = 0.5 [%]")
# Manually place legend 
ax[0].legend(loc='lower center')
ax[1].legend(loc='lower right')
ax[2].legend(loc='upper left')
# Grid and tickes
ax[0].grid(axis='x',color='0.95')
ax[0].grid(axis='y',color='0.95')
ax[0].set_yticks([0,0.02,0.04,0.06,0.08])
ax[1].grid(axis='x',color='0.95')
ax[1].grid(axis='y',color='0.95')
ax[2].grid(axis='x',color='0.95')
ax[2].grid(axis='y',color='0.95')
#ax[2].set_yticks([0,0.1,0.2,0.3,0.4,0.5])

# Ranges of the axes
ax[0].set_xlim(0,1) # s
ax[0].set_ylim(0.0,0.08) # m
ax[1].set_xlim(0,0.1) # s
ax[1].set_ylim(0.05,0.08) # m
ax[2].set_xlim(0,0.1) # s
#ax[2].set_ylim(-0.5,0.5) # %

# Add labels a) and b)
ax[0].text(-0.07,0.078,"a)")
ax[1].text(-0.0078,0.08,"b)")
ax[2].text(-0.007,0.3,"c)")

# Add timestep labels
ax[0].text(0.027,0.001,"t = 0 s", rotation = 37)
ax[0].text(0.021,0.021,"t = 0.5 s", rotation = 8)
ax[0].text(0.025,0.039,"t = 1 s", rotation = 3)


plt.tight_layout()

# Save as pdf
plt.savefig('10_surface_topography_diffusion_zero_flux.pdf')    
