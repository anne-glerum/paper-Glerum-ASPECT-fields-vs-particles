# -*- coding: utf-8 -*-
"""
Created on Thur Oct 7 by David Quiroga
Modified on Tues Oct 19 by Anne Glerum
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

#----------------------------General plotting parameters------------------------------

z_surface=0 		# Depth of the surface [m]
z_bottom=1.075 		# Depth of the bottom boundary [m]
x_left=0 		# Distance of left lateral boundary [m]
x_right=1 		# Distance of right lateral boundary [m]

# -------------------------------------Setup-------------------------------------------

#  Array definitions
M=np.ones((100,100))				# Array for material model 
x=np.linspace(x_left,x_right,len(M[0,:]))	# Distance array [m]
zs=np.linspace(z_surface,z_bottom,len(M[:,0]))	# Depth array [m]
density=np.ones(len(zs))			# Density Array [m]
viscosity=np.ones(len(zs))			# Viscosity Array [m]

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
    hill_x[i] = i * 0.1
  hill_y = 1 + 0.075 * np.sin(np.pi*hill_x)
  hill_x = np.append(hill_x, 1.)
  hill_y = np.append(hill_y, 0.)
  hill_x = np.append(hill_x, 0.)
  hill_y = np.append(hill_y, 0.)
  return hill_x,hill_y

x, y = hill_polygon()
ax.fill(x,y, color = 'lightsteelblue', edgecolor = 'black')

ax.set_yticks([z_bottom,1,z_surface])
ax.set_xticks([x_left,x_right])
ax.set_xlabel('X [m]',fontsize=13)
ax.set_ylabel('Y [m]',fontsize=13)
ax.set_xlim(x_left,x_right)
ax.set_ylim(z_surface,z_bottom)
ax.text(0,1.125,'(a)',fontsize=15)
plt.setp(ax.get_xticklabels(),fontsize=12, visible=True)
plt.setp(ax.get_yticklabels(),fontsize=12, visible=True)

# Annotations - Boundary Conditions
ax.text(-0.05,0.50,'Free slip',fontsize=9, rotation = 90, va = 'center', ha = 'center')
ax.text(1.05,0.50,'Free slip',fontsize=9, rotation = -90, va = 'center', ha = 'center')
ax.text(0.50,-0.05,'Free slip',fontsize=9, va = 'center', ha = 'center')
ax.text(0.50,1.125,'Free slip',fontsize=9, va = 'center', ha = 'center')
# Annotations material properties
ax.text(0.35,0.75,r'$\rho=1$ $\mathrm{kg/m^3}$', fontsize=9, ha='left')
ax.text(0.35,0.70,r'$g=1$ $\mathrm{m/s^2}$', fontsize=9, ha='left')
ax.text(0.35,0.80,'$\eta_{\mathrm{viscous}}=1 \,\mathrm{Pa} \cdot s$', fontsize=9, ha='left')

# Save Figure
plt.savefig('setup_surface_topography_diffusion_zero_flux_setup.pdf',bbox_inches="tight")
plt.close()
