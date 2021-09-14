# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 11:20:09 2021
@author: dyvas

Adapted on Tue Sep  7 by Anne Glerum
"""
import vtk_plot as vp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
rc("pdf", fonttype=42)
# Scientific color maps
from cmcrameri import cm


# Change path as needed
base = r"/Applications/ASPECT/VisualStudioCode/aspect/benchmarks/viscoelastic_stress_build-up/"

# Change file name modifiers as needed depending on your file structure
date = '070921_'
versions = ['a', 'b']
models = ['default t0', 'default t5']
labels = ['a)', 'b)', 'c)', 'd)', 'e)', 'f)']
tail = r'/viscoelastic_stress_build-up/solution'
#paths = [base+date+x+tail for x in versions]
paths = [base+tail]

print('Looking for pvtu files in ' +  str(paths))

# The timestep number of the timesteps that will be evaluated for each model
timesteps = np.array([0,1,2,3,4,5])

print('These timesteps will be evaluated ' + str(timesteps))

files = []

# Get all files to plot
for path in paths:
    fileset = vp.get_pvtu(path,timesteps)
    files = files+fileset

print('These files will be evaluated ' + str(files))

# Specify the number of subplots by stating the number of rows and columns.
# sharex and sharey indicate whether x and y axies labels are repeated for each subplot,
# or shared. Set shared x and y labels. Min resolution is 300 dpi.
fig,axs = plt.subplots(3,2,sharex=True,sharey=True,dpi=300,figsize=(8.5,13))
plt.xlabel("X [km]")
plt.ylabel("Y [km]")

# Model domain is 100x100 km2
# so place the camera focal point in the center
focal_point = (50000,50000,0)
position = (50000,50000,-300000)
viewup = (0,1,0)
camera = [position,focal_point,viewup]

# List of bounds to clip model:
# [xmin,xmax,ymin,ymax] for 2D and
# [xmin,xmax,ymin,ymax,zmin,zmax] for 3D.
# Note that 0 indicates bottom.
bounds = [0,100000,0,100000]

# We plot the xx element of the stress tensor.
field = 've_stress_xx'

# Loop over all solution files
# and create the subplots.
# Subplot lables include the timestep number in the top left corner.
# Use plot_scalar_bar=False to not plot the color bar.
for x in range(len(axs.flat)):
    vp.plot(files[x],field=field,
            bounds=bounds,
            ax=axs.flat[x],
            plot_scalar_bar=False)
    axs.flat[x].annotate(labels[x]+' t'+str(x),xy=(0.1,0.9),xycoords='axes fraction')
    # Maybe set separate titles for each subplot
    #axs.flat[x].set_title(f'Name {x}')

plt.tight_layout()

# Name the pdf according to the plotted field
# Change as needed
fig.savefig(str(field) + '.pdf')    
