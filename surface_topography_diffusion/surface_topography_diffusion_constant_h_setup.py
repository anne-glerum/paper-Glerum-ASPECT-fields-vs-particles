# -*- coding: utf-8 -*-
"""
Created on Thur Oct 7 by David Quiroga
Modified on Tues Oct 19 by Anne Glerum
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

#----------------------------General plotting parameters------------------------------

z_surface=0 		# Depth of the surface [km]
z_bottom=10.1 		# Depth of the bottom boundary [km]
x_left=0 		# Distance of left lateral boundary [km]
x_right=10 		# Distance of right lateral boundary [km]

# -------------------------------------Setup-------------------------------------------

#  Array definitions
M=np.ones((100,100))				# Array for material model 
x=np.linspace(x_left,x_right,len(M[0,:]))	# Distance array [km]
zs=np.linspace(z_surface,z_bottom,len(M[:,0]))	# Depth array [km]
density=np.ones(len(zs))			# Density Array [km]
viscosity=np.ones(len(zs))			# Viscosity Array [km]

# Create setup structure; only one material fills the domain
for i in range(len(M[:,0])):
	for j in range(len(M[0,:])):
			M[i,j]=1
			density[i]=2800
			viscosity[i]=1e22

#-----------------------------------------Plotting--------------------------------------------

# Create subplots
#fig, (ax,ax1,ax2) = plt.subplots(1,3,figsize=(8,4), gridspec_kw={'width_ratios': [4,1.,1.],'wspace':0.07,'hspace':0.25},sharex=False, squeeze=True)
fig, (ax) = plt.subplots(1,1,figsize=(4,4),sharex=False, squeeze=True)

# Color the whole domain, including the topography above y = 1
ax.spines['top'].set_visible(False)
def hill_polygon(): 
  hill_x = np.empty(11)
  for i in range(len(hill_x)):
    hill_x[i] = i * 1
  hill_y = 10 + 0.100 * np.sin(np.pi*hill_x/10)
  hill_x = np.append(hill_x, 10.)
  hill_y = np.append(hill_y, 0.)
  hill_x = np.append(hill_x, 0.)
  hill_y = np.append(hill_y, 0.)
  return hill_x,hill_y

x, y = hill_polygon()
ax.fill(x,y, color = 'lightsteelblue', edgecolor = 'black')

ax.set_yticks([z_bottom,3, 7, z_surface])
ax.yaxis.set_minor_locator(MultipleLocator(1))
ax.set_xticks([x_left,x_right])
ax.set_xlabel('X [km]',fontsize=13)
ax.set_ylabel('Y [km]',fontsize=13)
ax.set_xlim(x_left,x_right)
ax.set_ylim(z_surface,z_bottom)
ax.text(0,11.25,'(a)',fontsize=15)
plt.setp(ax.get_xticklabels(),fontsize=12, visible=True)
plt.setp(ax.get_yticklabels(),fontsize=12, visible=True)

# Annotations - Boundary Conditions
ax.text(-0.5,5.0,'No slip',fontsize=9, rotation = 90, va = 'center', ha = 'center')
ax.text(10.5,5,'No slip',fontsize=9, rotation = -90, va = 'center', ha = 'center')
ax.text(5,-0.5,'Free slip',fontsize=9, va = 'center', ha = 'center')
ax.text(5,10.6,'Free slip',fontsize=9, va = 'center', ha = 'center')
# Annotations material properties
ax.text(3.5,7.5,r'$\rho=3300$ $\mathrm{kg/m^3}$', fontsize=9, ha='left')
ax.text(3.5,7.0,r'$g=10$ $\mathrm{m/s^2}$', fontsize=9, ha='left')
ax.text(3.5,8.0,'$\eta_{\mathrm{viscous}}=10^{20} \,\mathrm{Pa} \cdot s$', fontsize=9, ha='left')

# Save Figure
plt.savefig('setup_surface_topography_diffusion_constant_h_setup.pdf',bbox_inches="tight")
plt.close()
