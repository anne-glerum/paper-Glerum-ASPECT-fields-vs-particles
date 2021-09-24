# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 by Anne Glerum
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
rc("pdf", fonttype=42)
# Scientific color maps
from cmcrameri import cm


# Change path as needed
base = r"/Applications/ASPECT/VisualStudioCode/aspect/benchmarks/viscoelastic_stress_build-up"

# Change file name modifiers as needed depending on your file structure
tail = r"/output-viscoelastic_stress_build-up/statistics"

# Create file path
paths = base+tail

# Read in the time and the minimum xx and yy components of the viscoelastic stress,
# which are stored on the fields ve_stress_xx and ve_stress_yy.
# The correct columns are selected with usecols.
time,stress_xx,stress_yy = np.genfromtxt(paths, comments='#', usecols=(1,14,17), unpack=True)

# Plot the stress elements in MPa against time in ky in
# categorical batlow colors.
# Multiply the stress_yy by -1 to get positive magnitudes.
plt.plot(time/1e3,stress_xx/1e6,label="$\sigma'_{xx}$",color=(0.005193,0.098238,0.349842))
plt.plot(time/1e3,-stress_yy/1e6,label="-$\sigma'_{yy}$",color=(0.985066,0.652522,0.547998))

# Also plot the analytical solution
# 2 * edot_ii * eta * (1 - e^(-mu*t/eta)), 
# with edot_ii = 0.03154/yr_in_secs/model_width 1/s, eta = 1e22 Pas, mu = 1e10 Pa.
yr_in_secs=3600.0*24.0*365.25
edot_ii=0.03154/yr_in_secs/100000.
plt.plot(time/1e3,1e-6*2*edot_ii*1e22*(1.-np.exp(-1e10*time*yr_in_secs/1e22)),label='analytical',color='black',linestyle='dashed')

# Labelling of plot
plt.xlabel("Time [ky]")
plt.ylabel("Deviatoric viscoelastic stress $\sigma'}$ components [MPa]")
# Manually place legend in lower right corner. 
plt.legend(loc='lower right')
# Title might not be needed/allowed.
#plt.title("Deviatoric viscoelastic stress over time")
plt.grid(axis='x',color='0.95')
plt.yticks([0,50,100,150,200,210])
plt.grid(axis='y',color='0.95')

# Ranges of the axes
plt.xlim(0,250) # kyr
plt.ylim(0,210) # MPa

plt.tight_layout()

# Name the pdf according to the plotted field
# Change as needed
field='deviatoric_stress'
plt.savefig(str(field) + '_over_time.pdf')    
