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
         "surface_topography_diffusion_constant_h_dt6311520000.0_GR4",
         "surface_topography_diffusion_constant_h_dt6311520000.0_GR5",
         "surface_topography_diffusion_constant_h_dt6311520000.0_GR6",
         "surface_topography_diffusion_constant_h_dt3155760000.0_GR4",
         "surface_topography_diffusion_constant_h_dt3155760000.0_GR5",
         "surface_topography_diffusion_constant_h_dt3155760000.0_GR6",
         "surface_topography_diffusion_constant_h_dt1577880000.0_GR4",
         "surface_topography_diffusion_constant_h_dt1577880000.0_GR5",
         "surface_topography_diffusion_constant_h_dt1577880000.0_GR6",
        ]
tail = r"/statistics"
tail_topo = r"/topography"

# The labels the graphs will get in the plot
labels = [
          'dt = 200 yr, dh = 62.5 m',
          'dt = 200 yr, dh = 31.25 m',
          'dt = 200 yr, dh = 15.625 m',
          'dt = 100 yr, dh = 62.5 m',
          'dt = 100 yr, dh = 31.25 m',
          'dt = 100 yr, dh = 15.625 m',
          'dt = 50 yr, dh = 62.5 m',
          'dt = 50 yr, dh = 31.25 m',
          'dt = 50 yr, dh = 15.625 m',
         ]
labels_error = [
          '',
          '',
          '',
          '',
          'dt = 100 yr, dh = 31.25 m',
          'dt = 100 yr, dh = 15.625 m',
          '',
          'dt = 50 yr, dh = 31.25 m',
          'dt = 50 yr, dh = 15.625 m',
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
linestyles = ['solid', 'solid', 'solid', 'dashed', 'dashed', 'dashed', 'dotted', 'dotted','dotted'] 
# Set the marker styles (no markers in this case)
markers = ['', '', '', '', '', '', '', '', '', '', '', ''] 
# Only plot every nth marker
dmark=15

# Set up a column of three plots, one with the full topography over time,
# one with the maximum topography over time (i.e. the topography at x = 0.5)
# and one with the percentage difference to the analytical solution for the maximum topography at x = 0.5.
fig = plt.figure(figsize=(10, 9))
ax = [fig.add_subplot(3, 1, i) for i in range(1, 4)]

# Also plot a zoom-in of the topography
zoom_x_min = 1.57788e12
zoom_x_max = 1.57988e12
zoom_y_min = 5
zoom_y_max = 70
#axins = zoomed_inset_axes(ax[0], 4, loc = "upper right") # zoom = 4
#axins.set_xlim(zoom_x_min, zoom_x_max)
#axins.set_ylim(zoom_y_min, zoom_y_max)
#mark_inset(ax[0], axins, loc1=1, loc2=4, fc="none", ec="0.5")

counter = 0 

# The analytical solution.
# Return topography at the center x-coordinate in m.
def topo_analytical(xc,time):
    amplitude = 100
    domain_width = 10000
    kappa = 0.0001
    # Fill another array of the size of time
    # with the x-coordinate so that x and time
    # have the same dimension.
    x = np.full((np.size(time)), xc)
    topo = amplitude * np.sin(x*np.pi/domain_width) * np.exp(-kappa*np.pi*np.pi*time/(domain_width*domain_width));
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
  ax[1].plot(time/(1000*3600*24*365.25),max_topo,label=labels[counter],color=colors[counter],linestyle=linestyles[counter],marker=markers[counter],markevery=dmark)
  ax[2].plot(time/(1000*3600*24*365.25),(max_topo-topo_analytical(5000,time))/topo_analytical(5000,time)*100.,label=None,color=colors[counter],linestyle=linestyles[counter],marker=markers[counter],markevery=dmark)
 
  if '631152' in name:
    x,topo = np.genfromtxt(path_topo+".00000", comments='#', usecols=(0,1), unpack=True)
    # Plot the topography along the surface of the domain, subtract domain height
    ax[0].plot(x/1000,topo-10000,label=None,color=colors[counter],linestyle=linestyles[counter],marker=markers[counter],markevery=dmark)

    x,topo = np.genfromtxt(path_topo+".00025", comments='#', usecols=(0,1), unpack=True)
    # Plot the topography along the surface of the domain, subtract domain height
    ax[0].plot(x/1000,topo-10000,label=None,color=colors[counter],linestyle=linestyles[counter],marker=markers[counter],markevery=dmark)

    x,topo = np.genfromtxt(path_topo+".00050", comments='#', usecols=(0,1), unpack=True)
    # Plot the topography along the surface of the domain 
    ax[0].plot(x/1000,topo-10000,label=None,color=colors[counter],linestyle=linestyles[counter],marker=markers[counter],markevery=dmark)
    #axins.plot(x/1000,topo-10000,label=None,color=colors[counter],linestyle=linestyles[counter],marker=markers[counter],markevery=dmark)
  elif '315576' in name:
    x,topo = np.genfromtxt(path_topo+".00000", comments='#', usecols=(0,1), unpack=True)
    # Plot the topography along the surface of the domain 
    ax[0].plot(x/1000,topo-10000,label=None,color=colors[counter],linestyle=linestyles[counter],marker=markers[counter],markevery=dmark)

    x,topo = np.genfromtxt(path_topo+".00050", comments='#', usecols=(0,1), unpack=True)
    # Plot the topography along the surface of the domain 
    ax[0].plot(x/1000,topo-10000,label=None,color=colors[counter],linestyle=linestyles[counter],marker=markers[counter],markevery=dmark)

    x,topo = np.genfromtxt(path_topo+".00100", comments='#', usecols=(0,1), unpack=True)
    # Plot the topography along the surface of the domain 
    ax[0].plot(x/1000,topo-1,label=None,color=colors[counter],linestyle=linestyles[counter],marker=markers[counter],markevery=dmark)
    #axins.plot(x/1000,topo-10000,label=None,color=colors[counter],linestyle=linestyles[counter],marker=markers[counter],markevery=dmark)
  elif '157788' in name:
    x,topo = np.genfromtxt(path_topo+".00000", comments='#', usecols=(0,1), unpack=True)
    # Plot the topography along the surface of the domain 
    ax[0].plot(x/1000,topo-10000,label=None,color=colors[counter],linestyle=linestyles[counter],marker=markers[counter],markevery=dmark)

    x,topo = np.genfromtxt(path_topo+".00100", comments='#', usecols=(0,1), unpack=True)
    # Plot the topography along the surface of the domain 
    ax[0].plot(x/1000,topo-10000,label=None,color=colors[counter],linestyle=linestyles[counter],marker=markers[counter],markevery=dmark)

    x,topo = np.genfromtxt(path_topo+".00200", comments='#', usecols=(0,1), unpack=True)
    # Plot the topography along the surface of the domain 
    ax[0].plot(x/1000,topo-10000,label=None,color=colors[counter],linestyle=linestyles[counter],marker=markers[counter],markevery=dmark)
    #axins.plot(x,topo-10000,label=None,color=colors[counter],linestyle=linestyles[counter],marker=markers[counter],markevery=dmark)
  else:
    print ("Timestep not accounted for")

  counter += 1

# Plot the analytical solution in Pa.
ax[1].plot(time/(1000*3600*24*365.25),topo_analytical(5000,time),label='analytical',color='black',linestyle='dashdot')

# Labelling of plot
ax[0].set_xlabel("X [km]")
ax[0].xaxis.set_label_coords(.5,-0.1)
ax[0].set_ylabel(r"Topography [m]")
ax[2].set_xlabel("Time [ky]")
ax[1].set_ylabel(r"Topography at x = 5 [km]")
ax[2].set_ylabel(r"Error at x = 5 km [%]")
# Manually place legend 
#ax[0].legend(loc='center')
ax[1].legend(loc='upper right')
#ax[2].legend(loc='upper left')
# Grid and tickes
ax[0].grid(axis='x',color='0.95')
ax[0].grid(axis='y',color='0.95')
ax[0].set_yticks([0,20,40,60,80,100])
ax[1].grid(axis='x',color='0.95')
ax[1].grid(axis='y',color='0.95')
ax[2].grid(axis='x',color='0.95')
ax[2].grid(axis='y',color='0.95')
#ax[2].set_yticks([0,0.1,0.2,0.3,0.4,0.5])

# Ranges of the axes
ax[0].set_xlim(0,10) # km
ax[0].set_ylim(0.0,105) # m
ax[1].set_xlim(0,10) # ky
ax[1].set_ylim(0.,105) # m
ax[2].set_xlim(0,10) # ky
#ax[2].set_ylim(-0.5,0.5) # %

# Add labels a) and b)
ax[0].text(-0.6,100,"a)")
ax[1].text(-0.600,98,"b)")
ax[2].text(-0.500,9.7,"c)")

# Add timestep labels
ax[0].text(2,65,"t = 0 ky", rotation = 37)
ax[0].text(2,18,"t = 5 ky", rotation = 8)
ax[0].text(2,6,"t = 10 ky", rotation = 3)


plt.tight_layout()

# Save as pdf
plt.savefig('11_surface_topography_diffusion_constant_h.pdf')    
