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
fig, (ax,ax1,ax2) = plt.subplots(1,3,figsize=(8,4), gridspec_kw={'width_ratios': [4,1.,1.],'wspace':0.07,'hspace':0.25},sharex=False, squeeze=True)

cmap = colors.ListedColormap(['lightsteelblue', 'pink','darkblue']) # Create customized discrete colormap
im=ax.imshow(M,extent=[x_left, x_right, z_bottom, z_surface], cmap=cmap)
ax.spines['top'].set_visible(False)
ax.set_yticks([z_surface,z_bottom])
ax.set_xticks([x_left,x_right])
ax.set_xlabel('Distance $[km]$',fontsize=13)
ax.set_ylabel('Depth $[km]$',fontsize=13)
ax.set_xlim(x_left,x_right)
ax.set_ylim(z_bottom,z_surface)
ax.text(0,-5,'(a)',fontsize=15)
plt.setp(ax.get_xticklabels(),fontsize=12, visible=True)
plt.setp(ax.get_yticklabels(),fontsize=12, visible=True)

# Annotations - Boundary Conditions
ax.text(3,50,'Free\n Slip',fontsize=9)
ax.text(70,50,'Prescribed $v_x$',fontsize=9)
ax.text(35,97,'Prescribed $v_y$',fontsize=9)
ax.text(40,-3,'Free Slip',fontsize=9)
# Bottom boundary
ax.arrow(20,108,0,-4,width=0.8, clip_on=False, fill=True, facecolor='black')
ax.arrow(40,108,0,-4,width=0.8, clip_on=False, fill=True, facecolor='black')
ax.arrow(60,108,0,-4,width=0.8, clip_on=False, fill=True, facecolor='black')
ax.arrow(80,108,0,-4,width=0.8, clip_on=False, fill=True, facecolor='black')
ax.text(5,117,'$v_y=3.154$\n $[cm/yr]$', fontsize=8)
# Right boundary
ax.arrow(100,20,4,0,width=0.8, clip_on=False, fill=True, facecolor='black')
ax.arrow(100,40,4,0,width=0.8, clip_on=False, fill=True, facecolor='black')
ax.arrow(100,60,4,0,width=0.8, clip_on=False, fill=True, facecolor='black')
ax.arrow(100,80,4,0,width=0.8, clip_on=False, fill=True, facecolor='black')
ax.text(100,90,'$v_x=3.154$\n  $[cm/yr]$', fontsize=8)
# Annotations material properties
ax.text(35,25,r'$\rho=2800$ $kg/m^3$', fontsize=9, ha='left')
ax.text(35,20,'$\eta_{\mathrm{viscous}}=10^{22} \,Pa \cdot s$\n$\mu=10^{10} \, Pa$', fontsize=9, ha='left')

# Density subplot
ax1.plot(density,zs,c='C0',linewidth=2)
ax1.set_xlabel(r'$\rho$ $[kg/m^3]$',fontsize=13)
ax1.set_ylim(z_surface,z_bottom)
ax1.set_xlim(2750,2850)
ax1.set_yticks([z_surface,z_bottom])
ax1.set_xticks([2750,2850])
ax1.text(2750,-5,'(b)',fontsize=15)
ax1.get_shared_y_axes().join(ax1, ax2) # Share y axis between subplots
plt.setp(ax1.get_xticklabels(),fontsize=12, visible=True)
plt.setp(ax1.get_yticklabels(),fontsize=12, visible=False)

# Viscosity subplot
ax2.plot(viscosity,zs,c='k',linewidth=2)
ax2.set_xscale('log')
ax2.set_xlabel(r'$\eta_{\mathrm{viscous}}$ $[Pa \cdot s]$',fontsize=13)
ax2.set_ylim(z_surface,z_bottom)
ax2.set_xlim(5e21,5e22)
ax2.set_yticks([z_surface,z_bottom])
ax2.set_xticks([1e22])
ax2.text(5e21,-5,'(c)',fontsize=15)
plt.setp(ax2.get_xticklabels(),fontsize=12, visible=True)
plt.setp(ax2.get_yticklabels(),fontsize=12, visible=False)
plt.minorticks_off()
plt.gca().invert_yaxis()

# Add Connection Patch
ax.add_patch(ConnectionPatch(xyA=(x_right,z_surface),coordsA='data',xyB=(2850,z_surface),coordsB='data',axesA=ax,axesB=ax1,clip_on=False))
ax.add_patch(ConnectionPatch(xyA=(x_right,z_bottom),coordsA='data',xyB=(2850,z_bottom),coordsB='data',axesA=ax,axesB=ax1,clip_on=False))

# Save Figure
plt.savefig('setup_viscoelastic_stress_build-up.pdf',bbox_inches="tight")
plt.close()
