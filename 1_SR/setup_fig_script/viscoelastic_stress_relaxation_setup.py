# -*- coding: utf-8 -*-
"""
Created on Thur Oct 7 by David Quiroga
Modified on Tues Oct 19 by Anne Glerum
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.patches import ConnectionPatch

#----------------------------General plotting parameters------------------------------

z_surface=0 		# Depth of the surface [km]
z_bottom=100 		# Depth of the bottom boundary [km]
x_left=0 		# Distance of left lateral boundary [km]
x_right=100 		# Distance of right lateral boundary [km]

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

cmap = colors.ListedColormap(['lightsteelblue', 'pink','darkblue']) # Create customized discrete colormap
im=ax.imshow(M,extent=[x_left, x_right, z_surface, z_bottom], cmap=cmap)
#ax.spines['top'].set_visible(False)
ax.set_yticks([z_bottom,z_surface])
ax.set_xticks([x_left,x_right])
ax.set_xlabel('X [km]',fontsize=13)
ax.set_ylabel('Y [km]',fontsize=13)
ax.set_xlim(x_left,x_right)
ax.set_ylim(z_surface,z_bottom)
#ax.text(0,105,'(a)',fontsize=15)
plt.setp(ax.get_xticklabels(),fontsize=12, visible=True)
plt.setp(ax.get_yticklabels(),fontsize=12, visible=True)

# Annotations - Boundary Conditions
ax.text(-5,50,'Free slip',fontsize=9, rotation = 90, va = 'center', ha = 'center')
ax.text(105,50,'Free slip',fontsize=9, rotation = -90, va = 'center', ha = 'center')
ax.text(50,-5,'Free slip',fontsize=9, va = 'center', ha = 'center')
ax.text(50,105,'Free slip',fontsize=9, va = 'center', ha = 'center')
# Annotations material properties
ax.text(35,75,r'$\rho=2800$ $\mathrm{kg/m^3}$', fontsize=9, ha='left')
ax.text(35,70,r'$g=0$ $\mathrm{m/s^2}$', fontsize=9, ha='left')
ax.text(35,80,'$\eta_{\mathrm{viscous}}=10^{22} \,\mathrm{Pa} \cdot \mathrm{s}$\n$G=10^{10} \, \mathrm{Pa}$', fontsize=9, ha='left')
# Annotations material properties
ax.text(35,45,r'$\dot{\epsilon} = \binom{0 \,\,  0}{0 \,\, 0} \, \mathrm{1/s}$', fontsize=9, ha='left', va='center')
ax.text(35,35,r'$\mathrm{W} = \binom{0 \,\, 0}{0 \,\, 0} \, \mathrm{1/s}$', fontsize=9, ha='left', va='center')
ax.text(35,25,r'$\tau^{0}_{\mathrm{c}}(t=0) = \binom{20 \,\,\,\,\,\,\,\,\,\,\,\, 0}{0 \,\,\,\, -20} \, \mathrm{MPa}$', fontsize=9, ha='left', va='center')

# Save Figure
plt.savefig('1_viscoelastic_relaxation_setup.png',bbox_inches="tight")
plt.close()
