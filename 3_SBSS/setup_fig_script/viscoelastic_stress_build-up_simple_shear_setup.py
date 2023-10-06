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

z_surface=0 		# Depth of the surface [m]
z_bottom=1 		# Depth of the bottom boundary [m]
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
			density[i]=1
			viscosity[i]=1e2

#-----------------------------------------Plotting--------------------------------------------

# Create subplots
fig, (ax) = plt.subplots(1,1,figsize=(4,4),sharex=False, squeeze=True)

cmap = colors.ListedColormap(['lightsteelblue', 'pink','darkblue']) # Create customized discrete colormap
im=ax.imshow(M,extent=[x_left, x_right, z_surface, z_bottom], cmap=cmap)
#ax.spines['top'].set_visible(False)
ax.set_yticks([z_bottom/2, z_surface])
ax.set_xticks([x_left,x_right/2, x_right])
ax.set_xlabel('X [m]',fontsize=13)
ax.set_ylabel('Y [m]',fontsize=13)
ax.set_xlim(x_left,x_right)
ax.set_ylim(z_surface,z_bottom)
ax.text(0,1.05,'(a)',fontsize=15)
plt.setp(ax.get_xticklabels(),fontsize=12, visible=True)
plt.setp(ax.get_yticklabels(),fontsize=12, visible=True)

# Annotations - Boundary Conditions
ax.text(0.05,0.50,'Prescribed v',fontsize=9, rotation = 90, va = 'center', ha = 'center')
ax.text(0.95,0.50,'Prescribed v',fontsize=9, rotation = 90, va = 'center', ha = 'center')
ax.text(0.50,0.05,'Prescribed v',fontsize=9, va = 'center', ha = 'center')
ax.text(0.50,1.05,'Prescribed v',fontsize=9, va = 'center', ha = 'center')
# Left boundary
ax.arrow(-0.06,0.20,0.012,0,width=0.008, clip_on=False, fill=True, facecolor='black')
ax.arrow(-0.07,0.40,0.024,0,width=0.008, clip_on=False, fill=True, facecolor='black')
ax.arrow(-0.08,0.60,0.036,0,width=0.008, clip_on=False, fill=True, facecolor='black')
ax.arrow(-0.09,0.80,0.048,0,width=0.008, clip_on=False, fill=True, facecolor='black')
ax.arrow(-0.10,1.00,0.060,0,width=0.008, clip_on=False, fill=True, facecolor='black')
# Top boundary
ax.arrow(0.20,1.00,0.060,0,width=0.008, clip_on=False, fill=True, facecolor='black')
ax.arrow(0.50,1.00,0.060,0,width=0.008, clip_on=False, fill=True, facecolor='black')
ax.arrow(0.75,1.00,0.060,0,width=0.008, clip_on=False, fill=True, facecolor='black')
# Right boundary
ax.arrow(1,0.20,0.012,0,width=0.008, clip_on=False, fill=True, facecolor='black')
ax.arrow(1,0.40,0.024,0,width=0.008, clip_on=False, fill=True, facecolor='black')
ax.arrow(1,0.60,0.036,0,width=0.008, clip_on=False, fill=True, facecolor='black')
ax.arrow(1,0.80,0.048,0,width=0.008, clip_on=False, fill=True, facecolor='black')
ax.arrow(1,1.00,0.06,0,width=0.008, clip_on=False, fill=True, facecolor='black')
ax.text(1.01,0.34,'$\mathrm{if} \, (t <= 0.5)$', fontsize=8)
ax.text(1.01,0.30,'  $\mathrm{v_x}=0.3 y$ [m/s]', fontsize=8)
ax.text(1.01,0.26,'else', fontsize=8)
ax.text(1.01,0.22,'  $\mathrm{v_x}=0.0$ [m/s]', fontsize=8)
ax.text(1.01,0.15,'$\mathrm{v_y}=0.0$ [m/s]', fontsize=8)
# Annotations material properties
ax.text(0.35,0.75,r'$\rho=1$ $\mathrm{kg/m^3}$', fontsize=9, ha='left')
ax.text(0.35,0.80,'$\eta_{\mathrm{viscous}}=10^{2} \,\mathrm{Pa} \cdot s$\n$G=10^{2} \, \mathrm{Pa}$', fontsize=9, ha='left')

# Annotations material properties
ax.text(0.35,0.50,'$\mathrm{if} \, (t <= 0.5)$', fontsize=8)
ax.text(0.35,0.45,r'  $\dot{\epsilon} = \binom{0 \,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\, 0.15}{0.15 \,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\, 0}$ 1/s', fontsize=9, ha='left', va='center')
ax.text(0.35,0.38,r'  $\mathrm{W} = \binom{0 \,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\, 0.15}{-0.15 \,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\, 0}$ 1/s', fontsize=9, ha='left', va='center')
ax.text(0.35,0.33,'else', fontsize=8)
ax.text(0.35,0.28,r'  $\dot{\epsilon} = \binom{0 \,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\, 0}{0 \,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\, 0}$ 1/s', fontsize=9, ha='left', va='center')
ax.text(0.35,0.21,r'  $\mathrm{W} = \binom{0 \,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\, 0}{0 \,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\, 0}$ 1/s', fontsize=9, ha='left', va='center')

# Add Connection Patch
#ax.add_patch(ConnectionPatch(xyA=(x_right,z_surface),coordsA='data',xyB=(2850,z_surface),coordsB='data',axesA=ax,axesB=ax1,clip_on=False))
#ax.add_patch(ConnectionPatch(xyA=(x_right,z_bottom),coordsA='data',xyB=(2850,z_bottom),coordsB='data',axesA=ax,axesB=ax1,clip_on=False))

# Save Figure
plt.savefig('3_viscoelastic_build-up_simple_shear_setup.png',bbox_inches="tight")
plt.close()
